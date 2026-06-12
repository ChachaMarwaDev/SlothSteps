"""
------------------
Classes and OOP
------------------
"""
import os
from dotenv import load_dotenv
from coinbase.rest import RESTClient

load_dotenv()

api_key    = os.getenv("COINBASE_API_KEY").strip()
api_secret = os.getenv("COINBASE_API_SECRET").strip()

client = RESTClient(api_key=api_key, api_secret=api_secret, timeout=5)

raw = client.get_products()
data = raw.to_dict()

class PriceTracker:
    
    def __init__(self):
        # this runs when you create the tracker
        # move your API call and all_products here
        self.products = data['products'][:]
    
    def get_price(self, coin):
        for product in self.products:
            if product['base_currency_id'] == coin:
                return float(product['price'])
        raise ValueError (f"{coin} was not found")
    
    def format_price(self, coin, price):
        return (f"{coin}: ${price:,.2f}")
        
    
    def get_multiple_prices(self, coins: list):
        result = {}
        for coin in coins:
            try:
                price = self.get_price(coin)
                result[coin] = self.get_price(coin)
            except ValueError as e:
                print(f"Skipping: {coin}")
        return result


tracker = PriceTracker()
print(tracker.get_price("BTC"))
print(tracker.get_multiple_prices(["BTC", "ETH", "FAKECOIN"]))