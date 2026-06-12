"""
------------------------
ERROR HANDLING
------------------------
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

products = data['products']
all_products = products[:] # [:] - Gives a list of all products

# function 1
def get_price(coin):
    for product in all_products:
        if product['base_currency_id'] == coin:
            return float(product['price'])
    raise ValueError (f"{coin} was not found")

# try:
#     print(get_price("FAKECOIN"))
# except ValueError as e:
#     print(e)

def format_price(coin, price):
    return (f"{coin}: ${price:,.2f}")

def get_multiple_prices(coins:list):
    result = {}
    for coin in coins:
        try:
            price = get_price(coin)
            result[coin] = format_price(coin, price)
        except ValueError as e:
            print(f"Skipping: {coin}")
    return result

print(get_multiple_prices(["BTC", "FAKECOIN", "ETH"]))