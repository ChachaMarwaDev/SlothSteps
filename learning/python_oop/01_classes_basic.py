# Classes Introduction
import os
from dotenv import load_dotenv
from coinbase.rest import RESTClient

load_dotenv()

api_key    = os.getenv("COINBASE_API_KEY").strip()
api_secret = os.getenv("COINBASE_API_SECRET").strip()

client = RESTClient(api_key=api_key, api_secret=api_secret, timeout=5)

raw = client.get_products()
data = raw.to_dict()

products = data["products"][0]

class Coinbase:
    def __init__(self, client):
        self.raw = client.get_products()
        self.data = self.raw.to_dict()
        self.product = self.data["products"][0]