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

    def get_product(self):
        return self.__products

a = Coinbase(client)
print(a.get_product())
