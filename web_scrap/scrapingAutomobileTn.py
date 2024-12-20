import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Step 1: Function to extract the car listing URLs
def extract_car_listing_urls(base_url):
    print("base_url",base_url)
    response = requests.get(base_url)
    response.raise_for_status()  # Ensure we get a valid response

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all car cards or listing items
    car_cards = soup.find_all('a', class_='occasion-link-overlay')  # Update class name based on the actual HTML

    car_urls = []
    for card in car_cards:
        href = card.get('href')
        if href:
            car_urls.append(href)

    return car_urls


# Step 2: Function to extract details from a car's individual page
def extract_car_details(car_url):
    print(car_url)
    response = requests.get(car_url)
    response.raise_for_status()  # Ensure we get a valid response

    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)
    # Extract brand, model, and ID from the URL
    parts = car_url.strip('/').split('/')
    brand = parts[6]  # e.g., "mercedes-benz"
    model = parts[7]  # e.g., "classe-c"
    car_id = parts[8]  # e.g., "102855"
    print('car_id',car_id)

    # Make sure the brand is Mercedes-Benz
    if brand.lower() != 'mercedes-benz':
        return None  # Skip this listing if the brand is not Mercedes-Benz

    # Construct the exact `href` to match
    hreflink = f"/{parts[3]}/{parts[4]}/{parts[5]}#occasion-{car_id}"
    print("Constructed hreflink:", hreflink)

    # Find the exact `href` match
    car_details_section = soup.find('a', href=lambda x: x == hreflink)

    if not car_details_section:
        print("Exact href not found:", hreflink)
        return None  # If we don't find the car section, skip this listing

    # Find the parent container of the car details section
    parent_container = car_details_section.find_parent('div')  # This will give us the parent div

    # Extract motorisation specifications
    motorisation = {}
    motorisation_section = parent_container.find('div', class_='box-inner-title', string=re.compile(r'\bMotorisation\b', re.IGNORECASE))
    if motorisation_section:
        motorisation_items = motorisation_section.find_next('div', class_='divided-specs').find_all('li')
        for item in motorisation_items:
            spec_name = item.find('span', class_='spec-name').text.strip() if item.find('span', class_='spec-name') else 'N/A'
            spec_value = item.find('span', class_='spec-value text-end').text.strip() if item.find('span', class_='spec-value text-end') else 'N/A'
            motorisation[spec_name] = ' '.join(spec_value.split())  # Clean extra spaces

    # Extract specifications
    specifications = {}
    specifications_section = parent_container.find('div', class_='box-inner-title', string=re.compile(r'\bSpécifications\b', re.IGNORECASE))
    if specifications_section:
        specification_items = specifications_section.find_next('div', class_='divided-specs').find_all('li')
        for item in specification_items:
            spec_name = item.find('span', class_='spec-name').text.strip() if item.find('span', class_='spec-name') else 'N/A'
            spec_value = item.find('span', class_='spec-value text-end').text.strip() if item.find('span', class_='spec-value text-end') else 'N/A'
            specifications[spec_name] = ' '.join(spec_value.split())  # Clean extra spaces

    # Return the extracted data as a dictionary
    car_details = {
        'Brand': brand,
        'Model': model,
        'ID': car_id,
        'Motorisation': motorisation,
        'Specifications': specifications
    }

    return car_details



# Step 3: Function to scrape the car listings and extract details from each
def scrape_car_listings(base_url, max_results=1):
    car_urls = extract_car_listing_urls(base_url)
    print('car_urls',car_urls)
    car_data = []
    for url in car_urls[:max_results]:  # Limit the number of results
        full_url = f"https://www.automobile.tn{url}"
        car_details = extract_car_details(full_url)
        if car_details:
            car_data.append(car_details)

    return car_data


# Base URL of the car listing page
base_url = 'https://www.automobile.tn/fr/occasion/s=brand!:mercedes-benz'

# Step 4: Scrape the data and store it in a DataFrame
car_listings_data = scrape_car_listings(base_url)
df = pd.DataFrame(car_listings_data)

# Save the data to a CSV file
df.to_csv('mercedes_benz_car_details.csv', index=False)

print("Data has been scraped and saved successfully!")
