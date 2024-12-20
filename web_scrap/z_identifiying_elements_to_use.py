from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options to simulate a real user and avoid headless mode for debugging
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
# chrome_options.add_argument("--headless")  # Uncomment this line if you want to run headless

# Start the Chrome WebDriver (it will run in headless mode if the argument is included)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# URL to scrape
car_url = 'https://www.automobile.tn/fr/occasion/s=brand!:mercedes-benz/1/mercedes-benz/cla/109439'

# Open the car URL
driver.get(car_url)

# Print the current URL after loading the page to check for redirects
print("Current URL:", driver.current_url)

# Optionally, you can pause for a few seconds to let the page fully load
driver.implicitly_wait(5)

print(driver.page_source)


# List of texts to search for and their labels
texts_to_find = [
    ("DT", "Price"),
    ("km", "Mileage"),
    ("10.2015", "Year"),
    ("Essence", "Fuel Type"),
    ("Manuelle", "Transmission"),
    ("8", "Power"),
    ("Traction", "Drive Type"),
    ("Berline", "Car Type"),
    ("20.12.2024", "Expiry Date"),
    ("Ariana", "Location")
]

# Loop through each text and find the corresponding parent element by its child text
for text, label in texts_to_find:
    try:
        # Search for the element containing the text
        element = driver.find_element(By.XPATH, f"//*[contains(text(), '{text}')]")
        # Get the parent element's ID
        parent_element = element.find_element(By.XPATH, "./..")  # Get the parent element
        parent_id = parent_element.get_attribute("id")  # Get the ID attribute of the parent element
        print(f"{label}: Found in element with ID: {parent_id}")
    except Exception as e:
        print(f"Could not find {text} on the page: {str(e)}")

# Close the WebDriver
driver.quit()
