import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


# Function to fetch car listings from a specific page
def fetch_car_listings(page_number):
    if page_number == 1:
        page_url = "https://baniola.tn/voitures"
    else:
        page_url = f"https://baniola.tn/voitures?page={page_number}"

    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, "html.parser")
    listings = []
    for card in soup.select(".card"):
        try:
            title = card.select_one(".card-title").text.strip()
            price = card.select_one(".price-button").text.strip().replace("TND", "").replace(",", "")
            location = card.select_one(".fa-map-marker-alt").find_parent().text.strip()
            listings.append({
                "Title": title,
                "Price (TND)": price,
                "Location": location,
            })
        except Exception as e:
            print(f"Error parsing listing: {e}")
    return listings


# Main function to scrape all car listings from the first 20 pages
def scrape_baniola():
    all_listings = []
    for page_number in range(1, 21):  # Scrape the first 20 pages
        print(f"Fetching listings from page {page_number}...")
        category_listings = fetch_car_listings(page_number)

        # If there are no listings on the page, stop scraping
        if not category_listings:
            break

        all_listings.extend(category_listings)
        time.sleep(2)  # Respectful scraping delay

    return all_listings


# Entry point
if __name__ == "__main__":
    car_listings = scrape_baniola()

    # Save car listings to CSV (without links and images)
    pd.DataFrame(car_listings).to_csv("../data/car_listings_baniola.csv", index=False)
    print("Car listings saved to 'car_listings_baniola.csv'.")
