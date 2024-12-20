import re
import pandas as pd
from datetime import datetime

# Load the dataset
df = pd.read_csv("../dataconcat and cleaning/updated_dataset.csv")

def extract_and_clean_fuel(row):
    model = row['Model'].lower()  # Convert model to lowercase for consistent comparison

    # Define fuel keywords mapping
    fuel_keywords = {
        'hybride': 'hybrid',  # Fix incorrect spelling
        'hybrid': 'hybrid',
        'essence': 'essence',
        'diesel': 'diesel'
    }

    # Search for each fuel keyword in the model
    for keyword, standard_fuel in fuel_keywords.items():
        if keyword in model:  # If fuel keyword is found in the model
            row['Énergie'] = standard_fuel  # Update the fuel column to standardized fuel name

    # Replace 'Hybride' followed by any characters with 'Hybride' only
    df['Énergie'] = df['Énergie'].str.replace(r'^Hybride.*', 'Hybride', regex=True)


    return row


# Remove rows with Price equal to 0
df = df[df['Price'] != 0]

# Display the structured DataFrame
print("Structured Data:\n", df)

# Get unique brands
unique_brands = df['Brand'].unique()

# Print the unique brands
print("Unique Brands in the dataset: ",len(unique_brands))
for brand in unique_brands:
    print(brand)

# Get the frequency (redundancy) of each brand
brand_counts = df['Brand'].value_counts()

# Print the frequency of each brand
print("Redundancy of each brand:")
print(brand_counts)

df.to_csv("preset2.csv", index=False)

# Save the cleaned dataset to a new CSV file
df.to_csv('updated_dataset.csv', index=False)

print("Fuel cleaned and saved as 'updated_dataset.csv'.")
