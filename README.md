The Jumia Bargain Hunter's Compass: A Data-Driven Guide to Discounts & Quality
Problem Statement
As a consumer on Jumia, I've often wondered if the massive discounts I see are too good to be true. Does a heavily discounted product on the platform actually indicate lower quality? This project was born from a personal desire to use data science to answer this question and help shoppers make smarter, more informed purchasing decisions.

Core Hypothesis
My initial hypothesis was that there would be a strong negative correlation between the discount percentage and the average product rating. In other words, I suspected that products with higher discounts would have lower customer ratings.

Methodology
This project followed a standard data science workflow, from data collection to analysis:
Data Collection: I built a multi-threaded web scraper in Python using requests and BeautifulSoup to collect product data, including price, discounts, ratings, and review counts.
Data Cleaning & Storage: The raw data was cleaned using pandas to handle messy prices, standardize values, and remove duplicate entries. The cleaned data was then loaded into an SQLite database (jumia_products.db) for efficient querying.
Data Analysis: I used SQL and Python with pandas and matplotlib to analyze the data, calculate statistical correlations, and visualize the findings.

Key Findings (The Data Story)
The analysis was conducted in two phases, revealing a more nuanced and interesting story than originally anticipated.

Phase 1: Initial Analysis (Smartphones Only):
My first analysis, focused solely on smartphones, produced a surprising result. The correlation coefficient between discount percentage and rating was found to be 0.03. This indicated virtually no relationship between the discount and the quality of smartphones.

Phase 2: Expanded Analysis (Multi-Category Dataset):
To be more diligent, I expanded the data to include nearly 2,000 products from other categories like kitchen appliances, Bluetooth speakers, and smartwatches. The new analysis revealed a weak negative correlation of -0.10. While this is a negative correlation, it's not a strong one, suggesting a slight tendency for products with high discounts to have slightly lower ratings, but the relationship is not robust.

The Compass: Actionable Advice
Based on the full, expanded dataset, the "Bargain Hunter's Compass" offers the following advice for Jumia shoppers:
Don't Fear the Discount: Discounts themselves are not a strong predictor of a product's quality. A deep discount does not automatically mean a product is low-quality.
Trust the Crowd: The most reliable indicator of a product's quality remains the customer rating, especially when supported by a high number of reviews.
Be Skeptical of Unreviewed Items: Products with high discounts but very few reviews should still be approached with caution.

Project Deliverables
Scrapper.py: The Python web scraping script.
clean_data.py: The script used for data cleaning and preparation.
load_data.py: The script to load the cleaned data into the SQLite database.
anaylze_data.py: The script used for SQL queries, statistical analysis, and visualization.
jumia_all_products.csv: The raw scraped data.

jumia_all_products_cleaned.csv: The cleaned data ready for analysis.

jumia_products.db: The SQLite database containing the final dataset.
