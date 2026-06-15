# Classes Encapsulation
import os
import csv
import sqlite3
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
    
    def create_table(self):
        conn = sqlite3.connect("prices.db")
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT NOT NULL,
            price REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            price_change_pct REAL NOT NULL,
            volume REAL NOT NULL,
            volume_change_pct REAL NOT NULL,
            timestamp TEXT NOT NULL)
        """)
        conn.commit()
        conn.close()

    def insert_prices(self, coins: list):
        conn = sqlite3.connect("prices.db")
        cursor = conn.cursor()
        for coin in coins:
            data=self.get_product(coin)
            if data:
                cursor.execute("""
                INSERT INTO prices 
                    (product_id, price, high, low, price_change_pct, volume, volume_change_pct, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data["ID"],
                data["Price"],
                data["High"],
                data["Low"],
                data["Price_change %"],
                data["Volume"],
                data["Volume_change %"],
                data["Timestamp"]))
        conn.commit()
        conn.close()

    def get_history(self, coin: str):
        conn = sqlite3.connect("prices.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM prices
            WHERE product_id = ?
        """, (coin + "-USD",))  # ← what goes here?
        rows = cursor.fetchall()
        conn.close()
        return rows

a = Coinbase(client)
for row in a.get_history("BTC"):
    print(row)
# a.create_table()
# a.insert_prices(["BTC", "ETH", "SOL", "WLD"])


# conn = sqlite3.connect("prices.db")
# cursor = conn.cursor()
# cursor.execute("SELECT * FROM prices")
# for row in cursor.fetchall():
#     print(row)
# conn.close()
