import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


def init_webdriver():
    """Initialize a single Selenium WebDriver instance."""
    chrome_options = Options()
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_argument("--headless")  # Uncomment for headless mode
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def get_car_urls(start_page, end_page):
    """Fetch car URLs from the list pages."""
    session = requests.Session()
    car_urls = []

    for page_num in range(start_page, end_page + 1):
        try:
            base_url = f'https://www.automobile.tn/fr/occasion/s=brand%21%3Apeugeot/{page_num}'
            response = session.get(base_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find car URLs
            car_cards = soup.find_all('div', class_='occasion-item-v2')
            for card in car_cards:
                link_tag = card.find('a', class_='occasion-link-overlay')
                if link_tag:
                    car_urls.append('https://www.automobile.tn' + link_tag['href'])
        except Exception as e:
            print(f"Error fetching page {page_num}: {e}")

    return car_urls


def extract_car_data(driver, car_url):
    """Extract car data from a specific URL using Selenium."""
    try:
        driver.get(car_url)
        driver.implicitly_wait(0)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        url_parts = car_url.split('/')

        brand = url_parts[7].replace(':', '') if len(url_parts) > 7 else 'N/A'
        model = url_parts[8] if len(url_parts) > 8 else 'N/A'
        car_id = url_parts[-1] if url_parts else 'N/A'

        # Extract price
        price = soup.find('div', class_='price')
        price_value = price.get_text(strip=True) if price else 'N/A'

        # Extract specifications
        specs_section = soup.find('div', class_='occasion-details-v2')
        spec_dict = {}
        if specs_section:
            for li in specs_section.find_all('li'):
                name = li.find('span', class_='spec-name').get_text(strip=True) if li.find('span', class_='spec-name') else ''
                value = li.find('span', class_='spec-value').get_text(strip=True) if li.find('span', class_='spec-value') else ''
                if name and value:
                    spec_dict[name] = value

        # Flatten data
        flattened_data = {'Brand': brand, 'Model': model, 'Car ID': car_id, 'Price': price_value}
        flattened_data.update(spec_dict)

        return flattened_data
    except Exception as e:
        print(f"Error extracting data from {car_url}: {e}")
        return {}


def save_to_csv(start_page, end_page, filename='peugeot.csv'):
    """Save car data to a CSV file."""
    car_urls = get_car_urls(start_page, end_page)
    car_data_list = []

    # Initialize WebDriver
    driver = init_webdriver()

    try:
        for car_url in car_urls:
            print(f"Processing {car_url}")
            car_data = extract_car_data(driver, car_url)
            car_data_list.append(car_data)

    finally:
        driver.quit()  # Ensure WebDriver is closed

    # Determine all possible fields
    fieldnames = {'Brand', 'Model', 'Car ID', 'Price'}
    for car_data in car_data_list:
        fieldnames.update(car_data.keys())

    # Write to CSV
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=sorted(fieldnames))
        writer.writeheader()
        for car_data in car_data_list:
            writer.writerow(car_data)

    print(f"Data saved to {filename}")


# Example usage
if __name__ == "__main__":
    start_time = time.time()
    save_to_csv(start_page=1, end_page=12)  # Adjust `end_page` for more pages maxx = = 12
    print(f"Time taken: {time.time() - start_time:.2f} seconds")

    print("Fin peugeot")