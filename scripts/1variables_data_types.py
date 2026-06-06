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
raw = client.get_product(product_id="ETH-USD")

# print(type(raw)) # <class 'coinbase.rest.types.product_types.GetProductResponse'>

data = raw.to_dict()

# .item() method to get all data types
for key, value in data.items():
    # we remove the none values from the retrieved data
    if value != "":
        # print the values from the call
        # print(f"{key} : {value}")
        pass

"""
==========================
DATABASE CONNECTION
==========================
"""
db_path = r"../data/test.db"
con = sqlite3.connect(db_path)
cur = con.cursor()

# TABLE DATA CREATION
cur.execute("""
    CREATE TABLE IF NOT EXISTS products(
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

# DATA: converting to proper data types
# STRING values (TEXT)
product_id = str(data.get('product_id', ''))
base_name = str(data.get('base_name', ''))
quote_name = str(data.get('quote_name', ''))
status = str(data.get('status', ''))
product_type = str(data.get('product_type', ''))

# NUMERIC values (REAL/DOUBLE) - convert from string to float
price = float(data.get('price', 0))
price_percentage_change_24h = float(data.get('price_percentage_change_24h', 0))
volume_24h = float(data.get('volume_24h', 0))
volume_percentage_change_24h = float(data.get('volume_percentage_change_24h', 0))
approximate_quote_24h_volume = float(data.get('approximate_quote_24h_volume', 0))
high_24h = float(data.get('high_24h', 0))
low_24h = float(data.get('low_24h', 0))

# check for converted values 
print("\n=== Converted Values for Database ===")
print(f"product_id: {product_id} (type: {type(product_id).__name__})")
print(f"price: {price} (type: {type(price).__name__})")
print(f"price_percentage_change_24h: {price_percentage_change_24h} (type: {type(price_percentage_change_24h).__name__})")
print(f"volume_24h: {volume_24h} (type: {type(volume_24h).__name__})")
print(f"base_name: {base_name} (type: {type(base_name).__name__})")
print(f"high_24h: {high_24h} (type: {type(high_24h).__name__})")
print(f"low_24h: {low_24h} (type: {type(low_24h).__name__})")

# TABLE DATA INSERTION
cur.execute("""
    INSERT INTO products(
        product_id,
        price,
        price_percentage_change_24h,
        volume_24h,
        volume_percentage_change_24h,
        base_name,
        quote_name,                
        status,
        product_type,
        approximate_quote_24h_volume,
        high_24h,
        low_24h
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
product_id,
price,
price_percentage_change_24h,
volume_24h,
volume_percentage_change_24h,
base_name,
quote_name,                
status,
product_type,
approximate_quote_24h_volume,
high_24h,
low_24h
))

con.commit()
print("\n✓ Data inserted successfully!")

cur.execute("SELECT * FROM products ORDER BY id")
row = cur.fetchall()

con.close()