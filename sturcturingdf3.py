import pandas as pd
import re

df = pd.read_csv("data/car_listings_baniola.csv")



# Function to extract fuel type and year



def extract_info(row):
    title = row['Title']
    fuel_types = ['Essence', 'Diesel','Hybride']

    # Extract fuel type
    fuel_type = next((fuel for fuel in fuel_types if fuel in title), None)

    # Extract year (4 consecutive digits)
    year_match = re.search(r'\b(19|20)\d{2}\b', title)
    year = year_match.group() if year_match else None

    # Remove fuel type and year from the title
    clean_title = title
    if fuel_type:
        clean_title = clean_title.replace(fuel_type, '').strip()
    if year:
        clean_title = re.sub(r'\b(19|20)\d{2}\b', '', clean_title).strip()

    # Return cleaned data
    return pd.Series([clean_title, fuel_type, year])


# Apply extraction function to the dataset
df[['Clean Title', 'Fuel Type', 'Year']] = df.apply(extract_info, axis=1)

# Drop original Title column and rename Clean Title
df.drop(columns=['Title'], inplace=True)
df.rename(columns={'Clean Title': 'Title'}, inplace=True)
df.to_csv("data/car_listings_baniola2.csv", index=False)
# Display cleaned DataFrame
print(df)