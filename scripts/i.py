import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()
db_path = os.getenv("DB_PATH")

st.set_page_config(page_title="Coinbase Data Viewer", page_icon="📊", layout="wide")
st.title("📊 Coinbase Spot Market Data Viewer")

# Sidebar
with st.sidebar:
    st.header("ℹ️ Database Info")
    db_file = Path(db_path)
    if db_file.exists():
        st.success(f"✅ Database found: {db_file.name}")
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            if tables:
                st.subheader("📁 Available Tables")
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                    row_count = cursor.fetchone()[0]
                    st.write(f"- `{table[0]}` ({row_count} rows)")
            conn.close()
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error(f"❌ Database not found at: {db_path}")
    
    st.divider()
    
    # Chart type selector
    st.subheader("Chart Settings")
    chart_type = st.selectbox(
        "Select Chart Type",
        ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Area Chart", "Histogram"]
    )
    
    color_theme = st.color_picker("Pick Chart Color", "#00f3ff")

# Connect to database
@st.cache_data
def load_data():
    conn = sqlite3.connect(db_path)
    data = pd.read_sql_query("SELECT * FROM spot WHERE product_id != '' AND price > 0", conn)
    conn.close()
    return data

try:
    df = load_data()
    
    # Create tabs for different chart views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Price Charts", 
        "💰 Volume Analysis", 
        "📈 Price Changes",
        "🎨 Custom Charts",
        "🔍 SQL + Chart"
    ])
    
    # ============ TAB 1: PRICE CHARTS ============
    with tab1:
        st.header("Price Analysis Charts")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top 10 highest prices - Bar Chart
            st.subheader("Top 10 Highest Prices")
            top_prices = df.nlargest(10, 'price')[['product_id', 'price', 'volume_24h']]
            
            fig1 = px.bar(
                top_prices, 
                x='product_id', 
                y='price',
                title="Highest Priced Products",
                labels={'product_id': 'Product', 'price': 'Price (USD)'},
                color='price',
                color_continuous_scale='Viridis'
            )
            fig1.update_layout(height=400)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Bottom 10 lowest prices - Bar Chart
            st.subheader("10 Lowest Prices")
            low_prices = df.nsmallest(10, 'price')[['product_id', 'price']]
            
            fig2 = px.bar(
                low_prices, 
                x='product_id', 
                y='price',
                title="Lowest Priced Products",
                labels={'product_id': 'Product', 'price': 'Price (USD)'},
                color='price',
                color_continuous_scale='Hot'
            )
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
        
        # Price Distribution Histogram
        st.subheader("Price Distribution")
        fig3 = px.histogram(
            df, 
            x='price', 
            nbins=50,
            title="Distribution of Product Prices",
            labels={'price': 'Price (USD)', 'count': 'Number of Products'},
            color_discrete_sequence=[color_theme]
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    # ============ TAB 2: VOLUME ANALYSIS ============
    with tab2:
        st.header("Volume Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top volumes - Horizontal Bar Chart
            st.subheader("Top 15 Products by Volume")
            top_volume = df.nlargest(15, 'volume_24h')[['product_id', 'volume_24h']]
            
            fig4 = px.bar(
                top_volume,
                x='volume_24h',
                y='product_id',
                orientation='h',
                title="24h Trading Volume",
                labels={'volume_24h': 'Volume (USD)', 'product_id': 'Product'},
                color='volume_24h',
                color_continuous_scale='Blues'
            )
            fig4.update_layout(height=500)
            st.plotly_chart(fig4, use_container_width=True)
        
        with col2:
            # Volume Pie Chart
            st.subheader("Volume Distribution (Top 10)")
            top_10_volume = df.nlargest(10, 'volume_24h')[['product_id', 'volume_24h']]
            
            fig5 = px.pie(
                top_10_volume,
                values='volume_24h',
                names='product_id',
                title="Volume Share by Product",
                hole=0.3
            )
            st.plotly_chart(fig5, use_container_width=True)
        
        # Scatter plot: Price vs Volume
        st.subheader("Price vs Volume Relationship")
        fig6 = px.scatter(
            df.head(100),  # Limit for performance
            x='price',
            y='volume_24h',
            text='product_id',
            title="Price vs Trading Volume",
            labels={'price': 'Price (USD)', 'volume_24h': '24h Volume'},
            color='volume_24h',
            size='volume_24h',
            color_continuous_scale='Plasma'
        )
        fig6.update_traces(textposition='top center')
        st.plotly_chart(fig6, use_container_width=True)
    
    # ============ TAB 3: PRICE CHANGES ============
    with tab3:
        st.header("Price Change Analysis")
        
        # Filter for products with price change data
        price_change_df = df[df['price_percentage_change_24h'].notna()]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Biggest gainers
            st.subheader("Top Gainers (+24h)")
            gainers = price_change_df.nlargest(10, 'price_percentage_change_24h')
            
            fig7 = px.bar(
                gainers,
                x='product_id',
                y='price_percentage_change_24h',
                title="Biggest Price Increases",
                labels={'product_id': 'Product', 'price_percentage_change_24h': '24h Change (%)'},
                color='price_percentage_change_24h',
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig7, use_container_width=True)
        
        with col2:
            # Biggest losers
            st.subheader("Top Losers (-24h)")
            losers = price_change_df.nsmallest(10, 'price_percentage_change_24h')
            
            fig8 = px.bar(
                losers,
                x='product_id',
                y='price_percentage_change_24h',
                title="Biggest Price Decreases",
                labels={'product_id': 'Product', 'price_percentage_change_24h': '24h Change (%)'},
                color='price_percentage_change_24h',
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig8, use_container_width=True)
        
        # Price change distribution
        st.subheader("Price Change Distribution")
        fig9 = px.histogram(
            price_change_df,
            x='price_percentage_change_24h',
            nbins=30,
            title="Distribution of 24h Price Changes",
            labels={'price_percentage_change_24h': '24h Change (%)', 'count': 'Number of Products'},
            color_discrete_sequence=[color_theme]
        )
        fig9.add_vline(x=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig9, use_container_width=True)
    
    # ============ TAB 4: CUSTOM CHARTS ============
    with tab4:
        st.header("Custom Chart Builder")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Chart controls
            x_axis = st.selectbox("X-Axis", df.columns)
            y_axis = st.selectbox("Y-Axis", df.columns)
            chart_color = st.selectbox("Color By", ['None'] + list(df.columns))
            chart_size = st.slider("Chart Height", 400, 800, 500)
            
            limit = st.number_input("Number of records", min_value=10, max_value=500, value=50)
        
        with col2:
            if chart_color == 'None':
                fig10 = px.scatter(
                    df.head(limit),
                    x=x_axis,
                    y=y_axis,
                    title=f"{y_axis} vs {x_axis}",
                    labels={x_axis: x_axis.replace('_', ' ').title(), 
                           y_axis: y_axis.replace('_', ' ').title()},
                    trendline="ols" if st.checkbox("Show Trendline") else None
                )
            else:
                fig10 = px.scatter(
                    df.head(limit),
                    x=x_axis,
                    y=y_axis,
                    color=chart_color,
                    title=f"{y_axis} vs {x_axis} (colored by {chart_color})",
                    labels={x_axis: x_axis.replace('_', ' ').title(), 
                           y_axis: y_axis.replace('_', ' ').title()}
                )
            
            fig10.update_layout(height=chart_size)
            st.plotly_chart(fig10, use_container_width=True)
    
    # ============ TAB 5: SQL + CHART ============
    with tab5:
        st.header("Run SQL Query and Visualize Results")
        
        query = st.text_area(
            "SQL Query:",
            value="SELECT product_id, price, volume_24h, price_percentage_change_24h FROM spot WHERE product_id != '' ORDER BY volume_24h DESC LIMIT 20",
            height=100
        )
        
        if st.button("Run Query & Create Chart", type="primary"):
            try:
                conn = sqlite3.connect(db_path)
                result_df = pd.read_sql_query(query, conn)
                conn.close()
                
                if not result_df.empty:
                    st.success(f"Query returned {len(result_df)} rows")
                    
                    # Display data
                    st.dataframe(result_df, use_container_width=True)
                    
                    # Choose chart type
                    chart_type_choice = st.selectbox(
                        "Select Chart Type",
                        ["Bar Chart", "Line Chart", "Scatter Plot", "Area Chart", "Pie Chart"]
                    )
                    
                    # Dynamically create chart based on available columns
                    numeric_cols = result_df.select_dtypes(include=['number']).columns
                    
                    if chart_type_choice == "Bar Chart" and len(numeric_cols) >= 1:
                        x_col = st.selectbox("X-axis", result_df.columns)
                        y_col = st.selectbox("Y-axis", numeric_cols)
                        fig = px.bar(result_df, x=x_col, y=y_col, title="Bar Chart")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    elif chart_type_choice == "Scatter Plot" and len(numeric_cols) >= 2:
                        x_col = st.selectbox("X-axis", numeric_cols)
                        y_col = st.selectbox("Y-axis", numeric_cols)
                        fig = px.scatter(result_df, x=x_col, y=y_col, title="Scatter Plot")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    elif chart_type_choice == "Line Chart" and len(numeric_cols) >= 1:
                        x_col = st.selectbox("X-axis", result_df.columns)
                        y_col = st.selectbox("Y-axis", numeric_cols)
                        fig = px.line(result_df, x=x_col, y=y_col, title="Line Chart")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    elif chart_type_choice == "Pie Chart":
                        names_col = st.selectbox("Labels", result_df.columns)
                        values_col = st.selectbox("Values", numeric_cols)
                        fig = px.pie(result_df, values=values_col, names=names_col, title="Pie Chart")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    elif chart_type_choice == "Area Chart" and len(numeric_cols) >= 1:
                        x_col = st.selectbox("X-axis", result_df.columns)
                        y_col = st.selectbox("Y-axis", numeric_cols)
                        fig = px.area(result_df, x=x_col, y=y_col, title="Area Chart")
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Query returned no results")
            except Exception as e:
                st.error(f"Error: {e}")

except Exception as e:
    st.error(f"Error loading data: {e}")

# Footer
st.divider()
st.markdown("💡 **Tip:** Interactive charts - hover, zoom, and select data points!")