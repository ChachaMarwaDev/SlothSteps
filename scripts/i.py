import streamlit as st
import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Coinbase Data Viewer",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 Coinbase Spot Market Data Viewer")
st.markdown("Run SQL queries to explore your cryptocurrency data")

# Database path
db_path = os.getenv("DB_PATH")

# Sidebar - Quick info and sample queries
with st.sidebar:
    st.header("ℹ️ Database Info")
    
    # Check if database exists
    db_file = Path(db_path)
    if db_file.exists():
        st.success(f"✅ Database found: {db_file.name}")
        
        # Get table info
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            if tables:
                st.subheader("📁 Available Tables")
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    row_count = cursor.fetchone()[0]
                    st.write(f"- `{table_name}` ({row_count} rows)")
            
            # Get column info for spot table
            cursor.execute("PRAGMA table_info(spot)")
            columns = cursor.fetchall()
            if columns:
                st.subheader("📋 Table Schema")
                col_df = pd.DataFrame(columns, columns=['cid', 'name', 'type', 'notnull', 'dflt_value', 'pk'])
                st.dataframe(col_df[['name', 'type']], use_container_width=True)
            
            conn.close()
        except Exception as e:
            st.error(f"Error reading database: {e}")
    else:
        st.error(f"❌ Database not found at: {db_path}")
    
    st.divider()
    
    # Sample queries
    st.header("📝 Sample Queries")
    st.markdown("""
    **Top 10 products by price:**
    ```sql
    SELECT product_id, price, volume_24h 
    FROM spot 
    WHERE product_id != '' 
    ORDER BY price DESC 
    LIMIT 10""")