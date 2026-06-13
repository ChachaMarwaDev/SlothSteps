# Classes Introduction
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
        self.data = self.raw.to_dict()
        self.products = self.data["products"]

    def get_product_info(self, coin):
        for product in self.products:
            if product.get("product_id") == coin:
                    return {
                    "ID":product.get("product_id"),
                    "Price":product.get("price"),
                    "High":product.get("high_24h"),
                    "Low":product.get("low_24h"),
                    "Price_change %":product.get("price_percentage_change_24h"),
                    "Volume": product.get("volume_24h"),
                    "Volume_change %": product.get("volume_percentage_change_24h")
                }
        return None

    def extracted_info(self, items:list):
        result = {}
        for item in items:
            info = self.get_product_info(item)
            if info is not None:
                 result[item] = info
            else:
                 print(f"Skipping: {item} not found")
        return result


cb = Coinbase(client)
# print(cb.product)  # Access the first product
print(cb.extracted_info(['BTC-USD', 'FAKE-COIN']))



"""
{'product_id': 'BTC-USD', 'price': '63015', 'price_percentage_change_24h': '0.72007299987581', 'volume_24h': '9136.64802146', 'volume_percentage_change_24h': '-2.47847963789828', 'base_increment': '0.00000001', 'quote_increment': '0.01', 'quote_min_size': '1', 'quote_max_size': '150000000', 'base_min_size': '0.00000001', 'base_max_size': '3400', 'base_name': 'Bitcoin', 'quote_name': 'US Dollar', 'watched': False, 'is_disabled': False, 'new': False, 'status': 'online', 'cancel_only': False, 'limit_only': False, 'post_only': False, 'trading_disabled': False, 'auction_mode': False, 'product_type': 'SPOT', 'quote_currency_id': 'USD', 'base_currency_id': 'BTC', 'fcm_trading_session_details': None, 'mid_market_price': '', 'alias': '', 'alias_to': ['BTC-USDC'], 'base_display_symbol': 'BTC', 'quote_display_symbol': 'USD', 'view_only': False, 'price_increment': '0.01', 'display_name': 'BTC-USD', 'product_venue': 'CBE', 'approximate_quote_24h_volume': '575745875.07', 'new_at': '2023-01-01T00:00:00Z', 'market_cap': '', 'base_cbrn': '', 'quote_cbrn': '', 'product_cbrn': '', 'icon_color': '', 'icon_url': '', 'display_name_overwrite': '', 'is_alpha_testing': False, 'about_description': '', 'best_bid_price': '', 'best_ask_price': '', 'high_24h': '63866.82', 'low_24h': '62255.87'}
"""