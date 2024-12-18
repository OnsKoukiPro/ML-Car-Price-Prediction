import pandas as pd
import re

# Load the dataset (change the path to where your dataset is located)
# If your dataset is in CSV format, you can load it like this:
df = pd.read_csv('../Step 3/preset3.csv')

# Fill missing 'Mileage' with the median value
df['Mileage'] = df['Mileage'].fillna(df['Mileage'].median())

# Fill missing 'Year' with the median value
df['Year'] = df['Year'].fillna(df['Year'].median())

# Step 1: Convert all brand names to lowercase
df['Brand'] = df['Brand'].str.lower()

# Step 2: Trim any leading or trailing spaces
df['Brand'] = df['Brand'].str.strip()

# Step 3: Handle "BMW X" by moving 'X' to the Model column and keeping 'BMW' as the Brand
df['Model'] = df.apply(lambda row: f"X{row['Model']}" if 'x' in row['Brand'].lower() else row['Model'], axis=1)
df['Brand'] = df['Brand'].replace('bmw x', 'bmw')  # Now replace "BMW X" with "BMW" in the Brand column


# Step 3: Standardize common typos (you can extend this dictionary based on your findings)
brand_mapping = {
    # Grouping common variations of the same brand
    'citroen': 'citroën', # Handle the typo for Citroen -> Citroën
    'sear': 'seat',        # Standardize spelling for SEAT
}

# Apply the mapping to the 'Brand' column
df['Brand'] = df['Brand'].replace(brand_mapping)

# Step 4: Remove brands with fewer than 10 samples
# Count the number of occurrences for each brand
brand_counts = df['Brand'].value_counts()

# Get a list of brands that appear less than 10 times
brands_to_remove = brand_counts[brand_counts < 10].index

# Remove rows where the brand is in the 'brands_to_remove' list
df_cleaned = df[~df['Brand'].isin(brands_to_remove)]

# Step 5: Remove rows where the fuel type is "N.C" (Non Classifié / Not Classified)
df_cleaned = df_cleaned[df_cleaned['Fuel'] != 'N.C']

# Step 6: Fix "Serie" to "Série" in the Model column for BMW
df_cleaned.loc[df_cleaned['Brand'] == 'bmw', 'Model'] = df_cleaned.loc[df_cleaned['Brand'] == 'bmw', 'Model'].str.replace(r'(?i)\bserie\b', 'Série', regex=True)


# Now, the 'Brand' column should have consistent values, and we have removed low-count brands and rows where the fuel type is "N.C"

# Step 1: Define the function to clean fuel from Model and update Fuel column
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
            row['Fuel'] = standard_fuel  # Update the fuel column to standardized fuel name
            model = model.replace(keyword, '').strip()  # Remove the fuel keyword from model

    # Clean up multiple spaces in the Model column after removing the fuel keyword
    row['Model'] = ' '.join(model.split())  # Remove excess whitespace

    return row


# Step 2: Apply the function to each row in the DataFrame
df_cleaned = df_cleaned.apply(extract_and_clean_fuel, axis=1)

# Step 3: Capitalize the Fuel column for consistency
df_cleaned['Fuel'] = df_cleaned['Fuel'].str.capitalize()
df_cleaned['Model'] = df_cleaned['Model'].str.capitalize()


# 1. Define multi-word model patterns for specific brands
core_model_patterns = {
    'mercedes-benz': ['classe g', 'classe a', 'classe c', 'classe e', 'classe s','gla','glc','glb','gls','amg gt','amg sl'],
    'bmw': ['x1','x2','x3', 'x4','x5','x6', 'série 1', 'série 2', 'série 3', 'série 4', 'série 5', 'série 6', 'série 7'],
    'kia': ['k1','k2','k3','k4','k5','k6','k7','k8','k9','sorento','sonet','stonic','carens','telluride','ceed','sportage', 'rio', 'sorento'],
    'audi': ['e-tron gt','q6 e-tron','q8 e-tron','q4 e-tron','a6 e-tron','q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6'],
    'volkswagen': ['golf 1','golf 2''golf 3','golf 4','golf 5','golf 6','golf 7','golf 8','golf 9','golf 10','arteon', 'bora','id.1','id.2','id.3','id.4','id.5','id.6','id.7','magotan','lavida','lamando','jetta','sagitar','vento','polo', 'passat'],
    'land rover' : ['defender','range rover','discovery'],
    'fiat' : ['topolino','500','500e','argo','Grande Panda','mobi','panda','tipo','egea','500x','600','fastback','pulse','ulysse','doblo','ducato','scudo','strada','toro','titano'],
    'renault' : ['5 E-tech','clio','lutecia','kwid','kardian','mégane','megane','sandero','twingo','taliant','austral','captur','duster','espace','kiger','koleos','rafale','dokker','kangoo','express'],
    'hyundai' : ['HB20','i10','i20','i30','accent','verna','grand i10','aura','avante','exter','ioniq 9','ioniq 5'],
    'toyota' : ['land cruiser 300','land cruiser 70','crown','corolla','yaris','urban cruiser','proace aerso']
}


# 2. Function to split the model into Core_Model and Specifications
def split_model(brand, model):
    brand = brand.lower()
    model = model.lower()

    core_model = ""
    specifications = model  # Start with the full model string as specifications

    # Step 1: Check if the brand has specific multi-word models
    if brand in core_model_patterns:
        patterns = core_model_patterns[brand]
        for pattern in patterns:
            if pattern in model:
                core_model = pattern.title()  # Extract and capitalize the core model
                specifications = re.sub(re.escape(pattern), '', model, count=1).strip()  # Remove core model
                break

    # Step 2: If no specific pattern, take the first word as the core model
    if not core_model:
        parts = model.split(maxsplit=1)
        core_model = parts[0].title()
        specifications = parts[1] if len(parts) > 1 else ""

    # Return Core_Model and Specifications
    return core_model, specifications.title()


# 3. Apply the function to the DataFrame and create new columns
df_cleaned[['Core_Model', 'Specifications']] = df_cleaned.apply(
    lambda row: pd.Series(split_model(row['Brand'], row['Model'])), axis=1
)

# Checking the distribution of categorical columns in the cleaned dataset
print("\nBrand distribution:")
print(df_cleaned['Brand'].value_counts())

print("\nFuel distribution:")
print(df_cleaned['Fuel'].value_counts())

print("\nModel distribution:")
print(df_cleaned['Model'].value_counts())

df_cleaned = df_cleaned.sort_values(by='Brand', ascending=True)

df_cleaned = df_cleaned.drop('Model', axis=1)

# Standardize 'Fuel' column to use 'Hybrid'
df_cleaned['Fuel'] = df_cleaned['Fuel'].replace({ 'Hybrid':'Hybride', 'hybrid': 'Hybride','hybride': 'Hybride', 'HYBRIDE': 'Hybride'})


column_order = ['Brand', 'Core_Model', 'Specifications','Year', 'Fuel', 'Mileage', 'Price']


df_cleaned = df_cleaned[column_order]

df_cleaned.to_csv('../Step 6/preset4.csv', index=False)
