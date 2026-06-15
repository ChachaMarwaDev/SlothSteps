# Classes Encapsulation
import os
import csv
from dotenv import load_dotenv
from coinbase.rest import RESTClient
from datetime import datetime

load_dotenv()
api_key    = os.getenv("COINBASE_API_KEY").strip()
api_secret = os.getenv("COINBASE_API_SECRET").strip()

client = RESTClient(api_key=api_key, api_secret=api_secret, timeout=5)

class Coinbase:
    def __init__(self, client):
        self.raw = client.get_products()
        self.__data = self.raw.to_dict()
        self.__products = self.__data["products"]

    @property
    def get_products(self):
        return self.__products
    
    def get_product(self, coins:str):
        for product in self.get_products:
            if product.get("base_currency_id") == coins:
                return {
                    "ID":               product.get("product_id"),
                    "Price":            float(product.get("price", 0)),
                    "High":             float(product.get("high_24h", 0)),
                    "Low":              float(product.get("low_24h", 0)),
                    "Price_change %":   float(product.get("price_percentage_change_24h", 0)),
                    "Volume":           float(product.get("volume_24h", 0)),
                    "Volume_change %":  float(product.get("volume_percentage_change_24h", 0)),
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
        return None
    
    def save_prices(self, coins:list):
        file_exists = os.path.exists("Solana_prices.csv")

        with open('Solana_prices.csv', 'a', newline='') as csvfile:
            for coin in coins:
                data = self.get_product(coin)
                if data:
                    writer = csv.DictWriter(csvfile, fieldnames=data.keys())
                    if not file_exists:
                        writer.writeheader()
                        file_exists = True
                    writer.writerow(data)
        return "All work done"

a = Coinbase(client)
# result = a.get_product("SOL")
result = a.save_prices(["SOL", "BTC", "ETH", "WLD"])

# for key, value in result.items():
#     print(f"{key}:{value}")
