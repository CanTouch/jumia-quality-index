import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://www.jumia.ug"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# New, more robust get_product_links function
def get_product_links(search_url):
    product_links = []
    try:
        response = requests.get(search_url, headers=HEADERS, timeout=10)
        response.raise_for_status() # This will raise an HTTPError if the response was an error
    except requests.exceptions.RequestException as e:
        print(f"Failed to load search page: {search_url} - {e}")
        return product_links

    soup = BeautifulSoup(response.text, 'html.parser')

    # This is the most direct way to find the product links
    for a_tag in soup.find_all('a', class_='core'):
        href = a_tag.get('href')
        if href and href.startswith('/'):
            # The URL needs to be correctly formed
            product_links.append(f"{BASE_URL}{href}")

    # Remove duplicates before returning
    return list(set(product_links))

# Scrape data from an individual product page
def parse_product_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # Product Name
        product_name_tag = soup.find('h1', class_='-fs20 -pts -pbxs')
        product_name = product_name_tag.get_text(strip=True) if product_name_tag else None

        # Original Price
        orig_price_tag = soup.find('span', class_='-tal -gy5 -lthr -fs16 -pvxs -ubpt')
        original_price = orig_price_tag.get_text(strip=True) if orig_price_tag else None

        # Discounted Price
        disc_price_tag = soup.find('span', class_='-b -ubpt -tal -fs24 -prxs')
        discounted_price = disc_price_tag.get_text(strip=True) if disc_price_tag else None

        # Discount Percentage
        discount_span = soup.find('span', class_='bdg _dsct _dyn -mls')
        discount_pct = discount_span.get('data-disc') if discount_span else None

        # Customer Rating
        rating_div = soup.find('div', class_='in')
        rating = None
        if rating_div and rating_div.has_attr('style'):
            match = re.search(r'width:(\d+)%', rating_div['style'])
            if match:
                rating = round((int(match.group(1)) / 100) * 5, 1)

        # Number of Reviews
        reviews_a = soup.find('a', class_='-plxs _more')
        num_reviews = None
        if reviews_a:
            match = re.search(r'\((\d+)', reviews_a.get_text())
            if match:
                num_reviews = int(match.group(1))

        return {
            'Product Name': product_name,
            'Original Price': original_price,
            'Discounted Price': discounted_price,
            'Discount Percentage': discount_pct,
            'Customer Rating (out of 5)': rating,
            'Number of Reviews': num_reviews,
            'Product URL': url
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Modified scrape_jumia function
def scrape_jumia(search_terms, pages=10, max_workers=10):
    all_products = []

    # Loop through each search term in the list
    for search_term in search_terms:
        print(f"Starting to scrape category: {search_term}")
        all_links = []
        for page in range(1, pages + 1):
            search_url = f"{BASE_URL}/catalog/?q={search_term.replace(' ', '+')}&page={page}"
            print(f"Fetching product links from page {page} for {search_term}...")
            links = get_product_links(search_url)
            all_links.extend(links)
            time.sleep(1)

        print(f"Scraping {len(all_links)} products in parallel for {search_term}...")
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(parse_product_page, link) for link in all_links]
            for future in as_completed(futures):
                data = future.result()
                if data:
                    # Add the search term to the product data for later analysis
                    data['Category'] = search_term
                    all_products.append(data)

    df = pd.DataFrame(all_products)
    df.to_csv('jumia_all_products.csv', index=False)
    print(f"Scraping completed. {len(all_products)} products saved to jumia_all_products.csv")

if __name__ == "__main__":
    categories_to_scrape = ["Kitchen Appliance", "bluetooth speaker", "smart watch", "Blenders", "kettles"]
    scrape_jumia(categories_to_scrape, pages=10, max_workers=10)