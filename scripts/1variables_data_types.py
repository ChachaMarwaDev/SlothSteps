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
        print(f"{key} : {value}")
        # pass

"""
==========================
DATABASE CONNECTION
==========================
"""
db_path = r"../data/test.db"
con = sqlite3.connect(db_path)
cur = con.cursor()

# TABLE CREATION
cur.execute("""
    CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id STRING NOT NULL,
    price INT NOT NULL,
    price_percentage_change_24h DOUBLE NOT NULL,
    volume_24h DOUBLE NOT NULL,
    volume_percentage_change_24h DOUBLE NOT NULL,
    base_name STRING NOT NULL,
    quote_name STRING NOT NULL,                
    status STRING NOT NULL,
    product_type STRING NOT NULL,
    approximate_quote_24h_volume DOUBLE NOT NULL,
    high_24h DOUBLE NOT NULL,
    low_24h DOUBLE NOT NULL,  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP                                    
    )
""")

print("Table was created successfully")
# test_result = cur.execute("INSERT INTO product")



# con.close()