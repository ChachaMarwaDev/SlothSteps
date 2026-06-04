import os
import json
from dotenv import load_dotenv
from coinbase.rest import RESTClient

load_dotenv()

api_key    = os.getenv("COINBASE_API_KEY").strip()
api_secret = os.getenv("COINBASE_API_SECRET").strip()

client = RESTClient(api_key=api_key, api_secret=api_secret, timeout=5)

"""
Products

get_product(self, product_id: str, get_tradability_status: bool | None = False, **kwargs)

get_products(self, limit: int | None = None, offset: int | None = None, product_type: str | None = None, product_ids: List[str] | None = None, contract_expiry_type: str | None = None, expiring_contract_status: str | None = None, get_tradability_status: bool | None = False, get_all_products: bool | None = False, **kwargs)

get_product_book(self, product_id: str, limit: int | None = None, aggregation_price_increment: str | None = None, **kwargs)

get_best_bid_ask(self, product_ids: List[str] | None = None, **kwargs)
"""
raw = client.get_products(product_type="SPOT", limit=1)
# data = raw.to_dict()

product_info = ["product_id", "price", "price_percentage_change_24h", "base_name", "quote_name", "status", "product_type", "quote_currency_id", "base_currency_id", "price_increment", "high_24h", "low_24h"]

extracted_data = []

for product in raw:
    if product:
        item = {}
        for field in product_info:
            if field in product:
                item[field] = product[field]
        extracted_data.append(item)


with open("product_spot_info.json", "w") as f:
    json.dump(extracted_data, f, indent=2)

print("File is ready for review")
# print(data.keys())

# with open("x1.json", "w") as f:
#     json.dump(data, f, indent=2)

# print("File is saved")

