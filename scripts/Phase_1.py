from dotenv import load_dotenv
from coinbase.rest import RESTClient
import os
import sqlite3

"""
==========================
API CONNECTION
==========================
"""
load_dotenv()

api_key    = os.getenv("COINBASE_API_KEY").strip()
api_secret = os.getenv("COINBASE_API_SECRET").strip()

# client is variable but also an instance of class RESTClient
client = RESTClient(api_key=api_key, api_secret=api_secret, timeout=5)

# gets a dictionary from the rest api
# raw = client.get_products()

# print(type(raw)) # <class 'coinbase.rest.types.product_types.GetProductResponse'>

raw = client.get_products(product_type="SPOT")
data = raw.to_dict()

product_info = [ "product_id", "price", "price_percentage_change_24h", "volume_24h", "volume_percentage_change_24h", "base_name","quote_name", "status", "product_type", "approximate_quote_24h_volume", "high_24h", "low_24h"]

extracted_data = []

for product in data['products']:
    if product:
        item = {}
        for field in product_info:
            if field in product:
                item[field] = product[field]
        extracted_data.append(item)

"""
==========================
DATABASE CONNECTION
==========================
"""

def safe_float(value, default=0.0):
    """Safely convert value to float, handling empty strings and None"""
    if value is None or value == '':
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

db_path = r"../data/products.db"
con = sqlite3.connect(db_path)
cur = con.cursor()

# TABLE DATA CREATION 
# spot products
cur.execute("""
    CREATE TABLE IF NOT EXISTS spot(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id TEXT NOT NULL,
        price REAL NOT NULL,
        price_percentage_change_24h REAL NOT NULL,
        volume_24h REAL NOT NULL,
        volume_percentage_change_24h REAL NOT NULL,
        base_name TEXT NOT NULL,
        quote_name TEXT NOT NULL,                
        status TEXT NOT NULL,
        product_type TEXT NOT NULL,
        approximate_quote_24h_volume REAL NOT NULL,
        high_24h REAL NOT NULL,
        low_24h REAL NOT NULL,  
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP                                    
    )
""")

print("Table was created successfully")

# Insert all products using safe_float
for product in extracted_data:
    cur.execute("""
        INSERT INTO spot(
            product_id, price, price_percentage_change_24h,
            volume_24h, volume_percentage_change_24h,
            base_name, quote_name, status, product_type,
            approximate_quote_24h_volume, high_24h, low_24h
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        product.get('product_id', ''),
        safe_float(product.get('price')),
        safe_float(product.get('price_percentage_change_24h')),
        safe_float(product.get('volume_24h')),
        safe_float(product.get('volume_percentage_change_24h')),
        product.get('base_name', ''),
        product.get('quote_name', ''),
        product.get('status', ''),
        product.get('product_type', ''),
        safe_float(product.get('approximate_quote_24h_volume')),
        safe_float(product.get('high_24h')),
        safe_float(product.get('low_24h'))
    ))

con.commit()
print(f"\n✓ Data inserted successfully! {len(extracted_data)} products added.")

# Fix the final query - use correct table name 'spot' not 'products'
cur.execute("SELECT * FROM spot ORDER BY id LIMIT 5")  # Show first 5 records
rows = cur.fetchall()

for row in rows:
    print(row)

con.close()