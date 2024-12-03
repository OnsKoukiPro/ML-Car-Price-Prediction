import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to fetch car listings from a specific page
def fetch_car_listings(page_number):
    url = f'https://www.autoprix.tn/recherche?cp={page_number}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all car listings on the page
    car_listings = soup.find_all('div', class_='stripe-btn elevation-0 overflow-hidden rounded v-card v-sheet theme--light')

    car_data = []
    for car in car_listings:
        title = car.find('h3', class_='title px-2').text.strip() if car.find('h3', class_='title px-2') else 'N/A'
        location = car.find('div', class_='v-list-item__title caption px-2 grey--text').text.strip() if car.find('div', class_='v-list-item__title caption px-2 grey--text') else 'N/A'
        price = car.find('span', class_='font-weight-black black--text rounded price-card').text.strip() if car.find('span', class_='font-weight-black black--text rounded price-card') else 'N/A'
        year = car.find('div', class_='pb-2 font-weight-bold caption col col-4').text.strip() if car.find('div', class_='pb-2 font-weight-bold caption col col-4') else 'N/A'
        mileage = car.find_all('div', class_='pb-2 font-weight-bold caption col col-4')[1].text.strip() if len(car.find_all('div', class_='pb-2 font-weight-bold caption col col-4')) > 1 else 'N/A'
        fuel_type = car.find_all('div', class_='pb-2 font-weight-bold caption col col-4')[2].text.strip() if len(car.find_all('div', class_='pb-2 font-weight-bold caption col col-4')) > 2 else 'N/A'

        # Exclude car URL and image URL as per the request
        car_data.append({
            'title': title,
            'location': location,
            'price': price,
            'year': year,
            'mileage': mileage,
            'fuel_type': fuel_type,
        })

    return car_data


# Main function to scrape the first 20 pages
def scrape_autoprix():
    all_car_data = []
    for page_number in range(1, 21):  # Scrape the first 20 pages
        print(f"Fetching listings from page {page_number}...")
        page_data = fetch_car_listings(page_number)
        all_car_data.extend(page_data)

    return all_car_data


# Entry point
if __name__ == "__main__":
    car_data = scrape_autoprix()

    # Save the car data to a CSV file
    df = pd.DataFrame(car_data)
    df.to_csv('car_listings_autoprix.csv', index=False, encoding='utf-8')

    print("Data saved to 'car_listings_autoprix.csv'.")