import re
import pandas as pd
from datetime import datetime

# Load the dataset
df = pd.read_csv('../dataconcat and cleaning/updated_dataset.csv')


# Remove rows with Price equal to 0
df = df[df['Price'] != 0]

# Replace entire 'Énergie' value with 'Hybride' if 'Hybride' is in the string
df.loc[df['Énergie'].str.contains('Hybride', case=False, na=False), 'Énergie'] = 'Hybride'

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

# Save the cleaned dataset to a new CSV file
df.to_csv('updated_dataset.csv', index=False)

print("Columns cleaned and saved as 'updated_dataset.csv'.")
