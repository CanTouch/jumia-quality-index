import pandas as pd
import re

# Load data 
df = pd.read_csv('jumia_all_products.csv')

# Clean the price columns and convert to numeric
df['Original Price'] = df['Original Price'].str.replace('UGX', '', regex=False).str.replace(',', '', regex=False).str.extract(r'(\d+)', expand=False)
df['Discounted Price'] = df['Discounted Price'].str.replace('UGX', '', regex=False).str.replace(',', '', regex=False).str.extract(r'(\d+)', expand=False)

# Convert columns to a float, handle NaNs
df['Original Price'] = pd.to_numeric(df['Original Price'], errors='coerce')
df['Discounted Price'] = pd.to_numeric(df['Discounted Price'], errors='coerce')

df['Discount Percentage'] = df['Discount Percentage'].str.replace('%', '', regex=False).astype(float)

# Handle missing values
df['Customer Rating (out of 5)'] = df['Customer Rating (out of 5)'].fillna(0)
df['Number of Reviews'] = df['Number of Reviews'].fillna(0)

print("Cleaned DataFrame:")
print(df.head())

# Save data to a new csv file
df.to_csv('jumia_products_cleaned.csv', index=False)
print("Cleaned data saved to 'jumia_products_cleaned.csv'.")