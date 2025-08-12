import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the database
conn = sqlite3.connect('jumia_products.db')

# Average rating for high-discount products
query1 = """
SELECT AVG("Customer Rating (out of 5)") AS average_rating_high_discount
FROM jumia_products
WHERE "Discount Percentage" >= 50;
"""
df1 = pd.read_sql_query(query1, conn)
print("--- Average Rating for products with 50%+ discount ---")
print(df1)
print("\n")

# Average rating by discount range 
query2 = """
SELECT
  CASE
    WHEN "Discount Percentage" BETWEEN 0 AND 10 THEN '0-10%'
    WHEN "Discount Percentage" BETWEEN 11 AND 50 THEN '11-50%'
    ELSE '>50%'
  END AS discount_range,
  AVG("Customer Rating (out of 5)") AS average_rating
FROM jumia_products
GROUP BY discount_range
ORDER BY average_rating DESC;
"""
df2 = pd.read_sql_query(query2, conn)
print("--- Average Rating by Discount Range ---")
print(df2)
print("\n")

# High discounts but low reviews products
query3 = """
SELECT
  "Product Name",
  "Discounted Price",
  "Discount Percentage",
  "Customer Rating (out of 5)",
  "Number of Reviews"
FROM jumia_products
WHERE "Discount Percentage" > 50
AND "Number of Reviews" < 10
ORDER BY "Customer Rating (out of 5)" ASC;
"""
df3 = pd.read_sql_query(query3, conn)
print("--- High Discount, Low Review Products ---")
print(df3.head())
print("\n")


df_for_correlation = pd.read_sql_query(
    "SELECT \"Discount Percentage\" AS discount_percent, \"Customer Rating (out of 5)\" AS rating FROM jumia_products WHERE \"Customer Rating (out of 5)\" > 0", 
    conn
)

correlation_coefficient = df_for_correlation['discount_percent'].corr(df_for_correlation['rating'])

print("--- Statistical Correlation ---")
print(f"The correlation between discount percentage and rating is: {correlation_coefficient:.2f}")
print("\n")

df_for_plot = pd.read_sql_query(
    "SELECT \"Discount Percentage\" AS discount_percent, \"Customer Rating (out of 5)\" AS rating FROM jumia_products WHERE \"Customer Rating (out of 5)\" > 0", 
    conn
)

plt.figure(figsize=(10, 6))
plt.scatter(df_for_plot['discount_percent'], df_for_plot['rating'], alpha=0.6)
plt.title('Relationship Between Discount Percentage and Customer Rating')
plt.xlabel('Discount Percentage (%)')
plt.ylabel('Customer Rating (out of 5)')
plt.grid(True)
plt.show()

conn.close()