import sqlite3

# Connect to the SQLite database file. 
conn = sqlite3.connect('jumia_products.db')

cursor = conn.cursor()

# Create the table
create_table_query = """
CREATE TABLE IF NOT EXISTS jumia_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_title TEXT,
    original_price REAL,
    discounted_price REAL,
    discount_percent REAL,
    rating REAL,
    review_count INTEGER
);
"""
cursor.execute(create_table_query)
conn.commit()
conn.close()

print("Database and table 'jumia_products' created successfully.")