import pandas as pd
import sqlite3

# Load the cleaned data
df_cleaned = pd.read_csv('jumia_products_cleaned.csv')

# Connect to your database
conn = sqlite3.connect('jumia_products.db')

# Insert the DataFrame into the 'jumia_products' table

df_cleaned.to_sql('jumia_products', conn, if_exists='replace', index=False)

conn.close()

print("Cleaned data has been successfully loaded into the SQLite database.")