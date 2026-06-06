import sqlite3

db_path = r"../data/test.db"
con = sqlite3.connect(db_path)
cur = con.cursor()

# Get column names
cur.execute("PRAGMA table_info(products)")
columns = [col[1] for col in cur.fetchall()]

# Get all data
cur.execute("SELECT * FROM products")
rows = cur.fetchall()

# Print formatted output
print("\n" + "="*100)
print(f"{'PRODUCTS TABLE':^100}")
print("="*100)

for row in rows:
    print(f"\nRecord ID: {row[0]}")
    print(f"  Product ID: {row[1]}")
    print(f"  Price: ${row[2]:,.2f}")
    print(f"  24h Change: {row[3]:.2f}%")
    print(f"  24h Volume: ${row[4]:,.2f}")
    print(f"  Volume Change: {row[5]:.2f}%")
    print(f"  Base Name: {row[6]}")
    print(f"  Quote Name: {row[7]}")
    print(f"  Status: {row[8]}")
    print(f"  Product Type: {row[9]}")
    print(f"  24h Volume (approx): ${row[10]:,.2f}")
    print(f"  24h High: ${row[11]:,.2f}")
    print(f"  24h Low: ${row[12]:,.2f}")
    print(f"  Created: {row[13]}")
    print(f"  Updated: {row[14]}")
    print("-"*50)

con.close()