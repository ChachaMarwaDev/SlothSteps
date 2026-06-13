# Classes Encapsulation
import os
from dotenv import load_dotenv
from coinbase.rest import RESTClient

load_dotenv()

api_key    = os.getenv("COINBASE_API_KEY").strip()
api_secret = os.getenv("COINBASE_API_SECRET").strip()

client = RESTClient(api_key=api_key, api_secret=api_secret, timeout=5)

class Coinbase:
    def __init__(self, client):
        self.raw = client.get_products()
        self.__data = self.raw.to_dict()
        self.__products = self.__data["products"]

    def get_products(self):
        return self.__products
    
    def get_product(self, coins:str):
        for product in self.get_products():
            if product.get("base_currency_id") == coins:
                return {
                    "ID":               product.get("product_id"),
                    "Price":            float(product.get("price", 0)),
                    "High":             float(product.get("high_24h", 0)),
                    "Low":              float(product.get("low_24h", 0)),
                    "Price_change %":   float(product.get("price_percentage_change_24h", 0)),
                    "Volume":           float(product.get("volume_24h", 0)),
                    "Volume_change %":  float(product.get("volume_percentage_change_24h", 0))
                }
        return None

a = Coinbase(client)
result = a.get_product("BTC")

for key, value in result.items():
    print(f"{key}:{value}")
