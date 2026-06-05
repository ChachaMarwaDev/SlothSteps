from dotenv import load_dotenv
from coinbase.rest import RESTClient
import os

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

