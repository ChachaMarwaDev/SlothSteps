import streamlit as st
import sqlite3
import pandas as pd
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

# Main area
st.header("🔍 Run SQL Query")

# Default query
default_query = """SELECT 
    product_id, 
    price, 
    price_percentage_change_24h,
    volume_24h
FROM spot 
WHERE product_id != '' 
ORDER BY volume_24h DESC 
LIMIT 10"""

# Session state to store query
if 'sql_query' not in st.session_state:
    st.session_state.sql_query = default_query

# Query input
query = st.text_area(
    "Enter your SQL query:",
    value=st.session_state.sql_query,
    height=150,
    key="sql_input"
)
st.session_state.sql_query = query

# Execute button
col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    execute_button = st.button("🚀 Execute Query", type="primary", use_container_width=True)

# Results area
if execute_button:
    if query.strip():
        try:
            conn = sqlite3.connect(db_path)
            result = pd.read_sql_query(query, conn)
            
            if not result.empty:
                st.success(f"✅ Query executed! {len(result)} rows returned.")
                st.dataframe(result, use_container_width=True)
                
                # Download button
                csv = result.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name="query_results.csv",
                    mime="text/csv"
                )
            else:
                st.info("ℹ️ Query returned no results")
            conn.close()
        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.warning("Please enter a SQL query")
else:
    st.info("👈 Click 'Execute Query' to run SQL")

# Sample queries expander
with st.expander("📝 Sample Queries"):
    st.markdown("""
    **Try these examples:**
    
    ```sql
    -- Show all Bitcoin pairs
    SELECT * FROM spot WHERE product_id LIKE 'BTC-%'
    
    -- Biggest gainers
    SELECT product_id, price_percentage_change_24h 
    FROM spot 
    ORDER BY price_percentage_change_24h DESC 
    LIMIT 10
    
    -- Top 5 by volume
    SELECT product_id, volume_24h 
    FROM spot 
    ORDER BY volume_24h DESC 
    LIMIT 5""")