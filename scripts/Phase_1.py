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
db_path = r"../data/test.db"
con = sqlite3.connect(db_path)
cur = con.cursor()

# TABLE DATA CREATION
# After extracting data (lines 39-46), insert all products:
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
        float(product.get('price', 0)),
        float(product.get('price_percentage_change_24h', 0)),
        float(product.get('volume_24h', 0)),
        float(product.get('volume_percentage_change_24h', 0)),
        product.get('base_name', ''),
        product.get('quote_name', ''),
        product.get('status', ''),
        product.get('product_type', ''),
        float(product.get('approximate_quote_24h_volume', 0)),
        float(product.get('high_24h', 0)),
        float(product.get('low_24h', 0))
    ))

# Fix the final query:
cur.execute("SELECT * FROM spot ORDER BY id")  # Use correct table name

con.commit()
print("\n✓ Data inserted successfully!")

cur.execute("SELECT * FROM products ORDER BY id")
row = cur.fetchall()

con.close()