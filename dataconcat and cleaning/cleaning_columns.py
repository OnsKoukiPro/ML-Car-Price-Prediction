import pandas as pd
import re

# Load your dataset
df = pd.read_csv('removing_unwanted_columns.csv')

# Modify the 'Model' column: take the first 2 characters and capitalize them
df['Model'] = df['Model'].apply(lambda x: x[:2].upper())

print("Audi Model column updated.")

# Function to modify the BMW 'Model' column
def modify_bmw_model(model, brand):
    if brand.lower() == 'bmw':
        # Use regex to find "serie-" followed by a number and remove the rest
        match = re.match(r'(serie-\d+)', model.lower())
        if match:
            return match.group(1)  # Return only "serie-x"
    return model

# Apply the function to modify the 'Model'
df['Model'] = df.apply(lambda row: modify_bmw_model(row['Model'], row['Brand']), axis=1)

print("BMW Model column updated.")

# Function to clean and format the columns
def clean_columns(df):
    # Price: Remove the unit 'DT'
    df['Price'] = df['Price'].apply(lambda x: re.sub(r'\D', '', str(x)))  # Remove non-digit characters (units)

    # Kilométrage: Remove the unit 'km'
    df['Kilométrage'] = df['Kilométrage'].apply(lambda x: re.sub(r'\D', '', str(x)))  # Remove non-digit characters (units)

    # Mise en circulation: Extract the year (last 4 digits after the period) and rename the column to 'année'
    def extract_year(value):
        if isinstance(value, str):
            # Handle the '12.2018' format (DD.MM.YYYY)
            parts = value.split('.')  # Split by the period
            if len(parts) > 1:
                return parts[-1]  # Return the last part after the period, which is the year
        return None  # Return None if the value doesn't match the expected format

    # Rename the 'Mise en circulation' column to 'année'
    df.rename(columns={'Mise en circulation': 'Année'}, inplace=True)
    # Convert the 'Année' column to string
    df['Année'] = df['Année'].astype(str)


    # Extract the year from the 'année' column
    df['Année'] = df['Année'].apply(lambda x: str(x).split('.')[-1] if isinstance(x, str) else None)

    # Function to pad year values to four digits
    def pad_year(year):
        year_str = str(year)
        return year_str + '0' * (4 - len(year_str))

    # Apply the function to the 'Année' column and create a new 'Année_Padded' column
    df['Année'] = df['Année'].apply(pad_year)

    # Step 1: Convert 'Année' to datetime if it's not already
    df['Année'] = pd.to_datetime(df['Année'], errors='coerce').dt.year

    # Cylindrée: Remove the unit 'cm³'
    df['Cylindrée'] = df['Cylindrée'].apply(lambda x: re.sub(r'\D', '', str(x)))  # Remove non-digit characters (units)

    # Nombre de portes: Keep only numeric part
    df['Nombre de portes'] = df['Nombre de portes'].apply(lambda x: re.sub(r'\D', '', str(x)))  # Remove non-digit characters

    # Puissance fiscale: Remove the unit 'cv' while keeping the numeric part
    df['Puissance fiscale'] = df['Puissance fiscale'].apply(lambda x: re.sub(r'\D', '', str(x)))  # Remove non-digit characters

    # Return the cleaned dataframe
    return df

# Apply the cleaning function to the DataFrame
df_cleaned = clean_columns(df)

# Save the cleaned dataset to a new CSV file
df_cleaned.to_csv('updated_dataset.csv', index=False)

print("Columns cleaned and saved as 'updated_dataset.csv'.")
