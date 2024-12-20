import pandas as pd

# Load the first dataset
df1 = pd.read_csv('../web_scrap/audi.csv')

# Load the second dataset
df2 = pd.read_csv('../web_scrap/bmw.csv')

# Load the first dataset
df3 = pd.read_csv('../web_scrap/hyundai.csv')

# Load the second dataset
df4 = pd.read_csv('../web_scrap/kia.csv')

# Load the first dataset
df5 = pd.read_csv('../web_scrap/mercedes-benz.csv')

# Load the second dataset
df6 = pd.read_csv('../web_scrap/peugeot.csv')


# Concatenate them vertically (rows)
combined_df = pd.concat([df1, df2, df3, df4, df5, df6], ignore_index=True)

# Save the combined dataset to a new CSV file
combined_df.to_csv('dataconcat.csv', index=False)

print("Datasets concatenated successfully! Saved to 'dataconcat.csv'")
