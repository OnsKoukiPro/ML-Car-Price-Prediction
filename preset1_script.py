import re
import pandas as pd
from datetime import datetime

# Load the dataset
df = pd.read_csv("clean_data/preset1.csv")

# Function to extract and convert mileage to integer
def clean_mileage(value):
    if pd.isna(value):  # Handle NaN values
        return None
    # Extract digits only, ignoring non-digit characters
    value = ''.join(filter(str.isdigit, str(value)))
    return int(value) if value.isdigit() else None

# Function to extract and convert price to integer
def clean_price(value):
    if pd.isna(value):  # Handle NaN values
        return None
    # Extract digits only, ignoring non-digit characters
    value = ''.join(filter(str.isdigit, str(value)))
    return int(value) if value.isdigit() else None

# Function to clean and validate the year
def clean_year(value):
    try:
        year = int(float(value))  # Convert to integer (handles values like 2016.0)
        current_year = datetime.now().year
        if 1900 <= year <= current_year:
            return year
    except (ValueError, TypeError):
        pass
    return None  # Return None for invalid years

# List of multi-word brands
multi_word_brands = [
    "Land Rover", "Mercedes-Benz", "BMW X", "Alfa Romeo", "Rolls-Royce", "BMW M", "Nissan Nismo",
    "Mercedes-AMG", "Audi Sport", "Great Wall", "SAIC Motor", "Faraday Future", "GAC Group",
    "Toyota Crown", "Chevrolet Silverado", "Chevrolet Corvette"
]

# Function to clean and split the Title into Brand and Model
def split_title(title):
    # Iterate over multi-word brands and match them in the title
    for brand in multi_word_brands:
        if brand in title:
            # If the title contains a multi-word brand, treat the brand as the first part
            Model = title.replace(brand, "").strip()
            return brand, Model

    # Default case: split by first space (first word is the brand, the rest is the Model)
    # This regex ensures that we handle titles with spaces more effectively
    match = re.match(r'(\S+)(?:\s+(.+))?', title)
    if match:
        return match.group(1), match.group(2)

    return title, None  # If no match, return the entire title as brand and None for Model

# Apply cleaning functions
df['Mileage'] = df['Mileage'].apply(clean_mileage).astype('Int64')  # Ensures it's an integer
df['Price'] = df['Price'].apply(clean_price).astype('Int64')  # Ensure price is an integer

# Remove rows with Price equal to 0
df = df[df['Price'] != 0]

df['Year'] = df['Year'].apply(clean_year).astype('Int64')  # Ensures Year is an integer

# Split Title into Brand and Model
df[['Brand', 'Model']] = df['Title'].apply(split_title).apply(pd.Series)

# Drop the original Title column
df = df.drop(columns=['Title'])

# Rearrange columns to the desired order
df = df[['Brand', 'Model', 'Fuel', 'Mileage', 'Year', 'Price']]

# Save the cleaned and structured DataFrame
df.to_csv("clean_data/preset1_cleaned_final.csv", index=False)

# Display the structured DataFrame
print("Structured Data:\n", df)

# Get unique brands
unique_brands = df['Brand'].unique()

# Print the unique brands
print("Unique Brands in the dataset: ",len(unique_brands))
for brand in unique_brands:
    print(brand)

# Step 1: Modify only DS-related rows
df.loc[df['Brand'] == 'DS', 'Brand'] = 'Citroen'  # Change DS to Citroen for DS rows
df.loc[df['Brand'] == 'Citroen', 'Model'] = 'DS ' + df['Model']  # Add "DS " to version ONLY for Citroen rows that were originally DS


# Get the frequency (redundancy) of each brand
brand_counts = df['Brand'].value_counts()

# Print the frequency of each brand
print("Redundancy of each brand:")
print(brand_counts)