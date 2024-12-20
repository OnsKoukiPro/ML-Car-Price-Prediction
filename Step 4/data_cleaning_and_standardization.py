import pandas as pd

# Load the dataset
df = pd.read_csv('../Step 3/updated_dataset.csv')

# Step 1: Remove rows that don't meet the specified criteria

df = df[
    (df['Price'] < 500000) &               # Price should be below 500000
    (df['Kilométrage'] < 600000) &         # Kilométrage should be below 600,000
    (df['Cylindrée'] < 5000) &             # Cylindrée should be below 5000
    (df['Puissance fiscale'] < 30) &       # Puissance fiscale should be below 30
    (df['Age'] < 25)                       # Age should be below 25
]

# Step 2: Display the cleaned dataset
print("Cleaned dataset:")
print(df.head())

# Optionally, save the cleaned dataset to a new CSV
df.to_csv('updated_dataset.csv', index=False)
