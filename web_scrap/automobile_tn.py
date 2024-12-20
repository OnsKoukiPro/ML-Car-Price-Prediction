import requests
from bs4 import BeautifulSoup
import csv
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import concurrent.futures
import time
import os

# Set up Chrome options to simulate a real user and avoid headless mode for debugging
chrome_options = Options()
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
chrome_options.add_argument("--headless")  # Uncomment this line if you want to run headless

# Start the Chrome WebDriver (it will run in headless mode if the argument is included)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Helper function to save data to CSV
def save_to_csv(data, filename='mercedes-benz.csv'):
    # Check if the file exists to append new data or create new file
    file_exists = os.path.exists(filename)

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ['Brand', 'Model', 'Car ID', 'Price']

        if not file_exists:  # Write header only if the file is new
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        for car_data in data:
            writer.writerow(car_data)

    print(f"Data saved to {filename}")

def get_car_urls(start_page, end_page):
    car_urls = []  # List to store the URLs of each car card

    for page_num in range(start_page, end_page + 1):
        base_url = f'https://www.automobile.tn/fr/occasion/s=brand%21%3Amercedes-benz/{page_num}'
        response = requests.get(base_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all car cards
        car_cards = soup.find_all('div', class_='occasion-item-v2')

        for card in car_cards:
            link_tag = card.find('a', class_='occasion-link-overlay')
            if link_tag:
                car_url = link_tag['href']
                car_urls.append('https://www.automobile.tn' + car_url)

    return car_urls

def extract_car_data(car_url):
    print(f"Extracting data from: {car_url}")
    url_parts = car_url.split('/')

    try:
        brand = url_parts[7].replace(':', '')
        model = url_parts[8]
        car_id = url_parts[-1]
    except IndexError:
        brand = model = car_id = 'N/A'

    driver.get(car_url)
    driver.implicitly_wait(5)

    print("Current URL:", driver.current_url)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extract the price
    price = soup.find('div', class_='price')
    price_value = price.get_text(strip=True) if price else 'N/A'

    content_container = soup.find('div', id='content_container')
    specs_section = content_container.find('div', class_='occasion-details-v2') if content_container else None

    spec_dict = {}

    if specs_section:
        # Loop through each spec item and get its name and value
        for li in specs_section.find_all('li'):
            name = li.find('span', class_='spec-name').get_text(strip=True) if li.find('span',
                                                                                       class_='spec-name') else ''
            value = li.find('span', class_='spec-value').get_text(strip=True) if li.find('span',
                                                                                         class_='spec-value') else ''

            if name and value:
                spec_dict[name] = value

    # Flatten the specs into the required format
    flattened_data = {
        'Brand': brand,
        'Model': model,
        'Car ID': car_id,
        'Price': price_value
    }

    # Add specifications as individual columns
    for spec_name, spec_value in spec_dict.items():
        flattened_data[spec_name] = spec_value

    return flattened_data

# Main function to scrape and save data
def scrape_and_save_data(start_page, end_page, filename='mercedes_data.csv'):
    car_urls = get_car_urls(start_page, end_page)
    all_car_data = []

    # Use a ThreadPoolExecutor for multithreading
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Submit each car_url extraction to the executor
        future_to_url = {executor.submit(extract_car_data, url): url for url in car_urls}

        for future in concurrent.futures.as_completed(future_to_url):
            try:
                car_data = future.result()
                all_car_data.append(car_data)

                # Save periodically to avoid data loss
                if len(all_car_data) % 10 == 0:  # Save every 10 cars
                    save_to_csv(all_car_data, filename)
                    all_car_data = []  # Reset after saving
            except Exception as e:
                print(f"Error processing {future_to_url[future]}: {e}")

    # Save any remaining data
    if all_car_data:
        save_to_csv(all_car_data, filename)

# Example usage
start_page = 1
end_page = 28  # Adjust this to scrape more pages
scrape_and_save_data(start_page, end_page)

driver.quit()  # Don't forget to quit the WebDriver when done
