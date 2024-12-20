import pandas as pd

# Load your dataset
# Replace 'your_dataset.csv' with the actual file path
df = pd.read_csv('dataconcat.csv')

# List of columns to keep
columns_to_keep = [
    'Car ID', 'Brand', 'Model', 'Price', 'Kilométrage',
    'Mise en circulation','Carrosserie',
    'Boite vitesse', 'Cylindrée', 'Nombre de portes',
    'Puissance fiscale', 'Transmission', 'Énergie'
]

# Filter the DataFrame to keep only the specified columns
filtered_df = df[columns_to_keep]

# Save the cleaned dataset to a new CSV file
filtered_df.to_csv('removing_unwanted_columns.csv', index=False)

print("Dataset cleaned and saved as 'cleaned_dataset.csv'.")
