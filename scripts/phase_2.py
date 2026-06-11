import os
from dotenv import load_dotenv
from coinbase.rest import RESTClient

load_dotenv()

api_key    = os.getenv("COINBASE_API_KEY").strip()
api_secret = os.getenv("COINBASE_API_SECRET").strip()

client = RESTClient(api_key=api_key, api_secret=api_secret, timeout=5)

raw = client.get_products()
data = raw.to_dict()


# print(data.keys())

"""
Functions and scope

Function 1 — get_price(coin)
Calls the Coinbase API and returns the current price of a coin. For example get_price("BTC") should return something like 45000.23 as a float.
Things to think about:

What does the API URL look like for BTC? For ETH?
How do you get the price out of the response? (hint: it comes back as a string from Coinbase, not a float)
What should the function return?


Function 2 — format_price(coin, price)
Takes a coin name and a price and returns a nicely readable string. For example:
BTC: $45,000.23
ETH: $2,891.10
Things to think about:

How do you format a float to always show 2 decimal places with commas?
Should this function call the API or just format what it's given?


Function 3 — get_multiple_prices(coins)
Takes a list of coin names and returns a dictionary of coin → price. For example:
pythonget_multiple_prices(["BTC", "ETH", "SOL"])
# returns {"BTC": 45000.23, "ETH": 2891.10, "SOL": 142.50}
Things to think about:

This function should reuse get_price() — don't repeat the API call logic
What data structure do you use to build up the result?
"""
# Get values from products

products = data['products']
all_products = products[:] # [:] - Gives a list of all products

# Function 1 — get_price(coin)
# Calls the Coinbase API and returns the current price of a coin. For example get_price("BTC") should return something like 45000.23 as a float.
def get_price(coin):
    for product in all_products:
        if product['base_currency_id'] == coin:
             return float(product['price'])

print(get_price("ETH"))

# Function 2 — format_price(coin, price)
# Takes a coin name and a price and returns a nicely readable string.

def format_price(coin, price):
    name = product['base_currency_id']
    amount = product['price']
    for product in all_products:
        if name == coin :
             return f"{name}:{amount:.2f}"

format_price()
