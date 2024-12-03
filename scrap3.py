import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL
url = 'https://karahba.tn'

# Function to scrape data from the page
def scrape_karahba_page():
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve the page")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    listings = soup.find_all('article', class_='hp-listing')

    data = []
    for listing in listings:
        title = listing.find('h4', class_='hp-listing__title').get_text(strip=True)
        brand = listing.find('div', class_='hp-listing__attribute--marque').get_text(strip=True)
        price = listing.find('div', class_='hp-listing__attribute--prix').get_text(strip=True)
        mileage = listing.find('div', class_='hp-listing__attribute--kilometrage').get_text(strip=True)
        phone = listing.find('div', class_='hp-listing__attribute--telephone').get_text(strip=True)
        location = listing.find('div', class_='hp-listing__location').get_text(strip=True)
        date = listing.find('time', class_='hp-listing__created-date').get_text(strip=True)

        data.append({
            'Title': title,
            'Brand': brand,
            'Price': price,
            'Mileage': mileage,
            'Phone': phone,
            'Location': location,
            'Date': date,
        })

    return data

# Scrape the page (only one page in this case)
all_data = scrape_karahba_page()

# Save the data to a CSV file
df = pd.DataFrame(all_data)
df.to_csv('car_listings_karahba.csv', index=False, encoding='utf-8')

print("Data saved to 'car_listings_karahba.csv'.")
