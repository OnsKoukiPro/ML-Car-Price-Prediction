import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


# Function to fetch a page and parse safety features
def fetch_safety_features(soup):
    safety_features = []
    for label in soup.find_all("label", class_="d-block my-1"):
        feature = label.text.strip().split("\n")[0]  # Extract feature name
        count = label.find("span", class_="count").text.strip()  # Extract count
        safety_features.append({"Feature": feature, "Count": int(count)})
    return safety_features


# Function to fetch car listings from a single page
def fetch_car_listings(soup):
    car_listings = []
    for car in soup.find_all("div", class_="occasion-item-v2"):
        try:
            title = car.find("h2").text.strip()  # Extract car title
            specs = car.find_all("li")  # Extract specifications
            mileage = specs[0].text.strip() if len(specs) > 0 else None
            year = specs[1].text.strip() if len(specs) > 1 else None
            transmission = specs[2].text.strip() if len(specs) > 2 else None
            fuel = specs[5].text.strip() if len(specs) > 5 else None
            price = car.find("div", class_="price").text.strip()  # Extract price

            car_listings.append({
                "Title": title,
                "Mileage": mileage.replace("km", "").strip() if mileage else None,
                "Year": year,
                "Transmission": transmission,
                "Fuel": fuel,
                "Price": price.replace("DT", "").replace(",", "").strip() if price else None
            })
        except Exception as e:
            print(f"Error extracting car listing: {e}")
    return car_listings


# Main function to scrape all pages
def scrape_website(base_url, max_pages=50):
    all_safety_features = []
    all_car_listings = []
    for page in range(1, max_pages + 1):
        print(f"Fetching page {page}...")
        response = requests.get(f"{base_url}?page={page}")
        soup = BeautifulSoup(response.content, "html.parser")

        # Fetch safety features from the first page only
        if page == 1:
            safety_features = fetch_safety_features(soup)
            all_safety_features.extend(safety_features)

        # Fetch car listings
        car_listings = fetch_car_listings(soup)
        all_car_listings.extend(car_listings)

        # Delay between requests to avoid overloading the server
        time.sleep(2)

    return all_safety_features, all_car_listings


# Entry point
if __name__ == "__main__":
    # Define the base URL
    base_url = "https://www.automobile.tn/fr/occasion"

    # Scrape the website
    safety_features, car_listings = scrape_website(base_url, max_pages=50)

    # Save safety features to CSV
    safety_features_df = pd.DataFrame(safety_features)
    safety_features_df.to_csv("safety_features.csv", index=False)
    print("Safety features saved to 'safety_features.csv'.")

    # Save car listings to CSV
    car_listings_df = pd.DataFrame(car_listings)
    car_listings_df.to_csv("car_listings.csv", index=False)
    print("Car listings saved to 'car_listings.csv'.")
