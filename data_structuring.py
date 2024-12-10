import pandas as pd


pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', 10)      # Adjust the maximum rows as needed
pd.set_option('display.expand_frame_repr', False)  # Prevent line wrapping

df1 = pd.read_csv("data/car_listings.csv")
df2 = pd.read_csv("data/car_listings_autoprix.csv")
df3 = pd.read_csv("data/car_listings_baniola2.csv")
df4 = pd.read_csv("data/car_listings_karahba.csv")


print("df1:\n",df1.columns)
print("df2:\n",df2.columns)
print("df3:\n",df3.columns)
print("df4:\n",df4.columns)

df1.rename(columns={'title': 'Make', 'car_year': 'Year'}, inplace=True)
df2.rename(columns={'title': 'Title', 'price': 'Price', 'year': 'Year', 'fuel_type': 'Fuel', 'mileage': 'Mileage'}, inplace=True)
df3.rename(columns={'Price (TND)': 'Price', 'Fuel Type': 'Fuel'}, inplace=True)
df4.rename(columns={'brand': 'Make', 'manufacture_year': 'Year'}, inplace=True)

print("After Renaming")

print("df1:\n",df1.columns)
print("df2:\n",df2.columns)
print("df3:\n",df3.columns)
print("df4:\n",df4.columns)

# Simulated column names for each dataset
columns_df1 = ['Title', 'Mileage', 'Year', 'Transmission', 'Fuel', 'Price']
columns_df2 = ['Title', 'location', 'Price', 'Year', 'Mileage', 'Fuel']
columns_df3 = ['Price', 'Location', 'Title', 'Fuel', 'Year']
columns_df4 = ['Title', 'Brand', 'Price', 'Mileage', 'Phone', 'Location', 'Date']

# Combine all columns and identify unique ones
all_columns = set(columns_df1 + columns_df2 + columns_df3 + columns_df4)

# Determine common columns across all datasets
common_columns = list(set(columns_df1) & set(columns_df2) & set(columns_df3) & set(columns_df4))

# Rearrange all columns: common first, unique at the end
ordered_columns = common_columns + sorted(all_columns - set(common_columns))

# Function to rearrange and fill missing columns
def rearrange_columns(df, column_order):
    # Reindex the DataFrame with the new column order, filling missing columns with NaN
    return df.reindex(columns=column_order, fill_value=None)

# Rearrange columns for each DataFrame
df1 = rearrange_columns(df1, ordered_columns)
df2 = rearrange_columns(df2, ordered_columns)
df3 = rearrange_columns(df3, ordered_columns)
df4 = rearrange_columns(df4, ordered_columns)

# # Concatenate the datasets
# combined_df = pd.concat([df1, df2, df3, df4], ignore_index=True)

# Display column order and final DataFrame
print("Ordered Columns for datasets:")
# print(combined_df.head())

print("df1:\n",df1.columns)
print("df2:\n",df2.columns)
print("df3:\n",df3.columns)
print("df4:\n",df4.columns)

print("df1:\n",df1)
print("df2:\n",df2)
print("df3:\n",df3)
print("df4:\n",df4)


# Combine Title and Brand
def combine_title_and_brand(row):
    title = row['Title']
    brand = row['Brand']

    if pd.isna(brand) or brand == 'None':  # If no brand exists, do nothing
        return title
    elif brand in title:  # If brand is already in the title, keep the title as-is
        return title
    else:  # Otherwise, combine brand and title
        return f"{brand} {title}"


# Apply the function
df1['Title'] = df1.apply(combine_title_and_brand, axis=1)

# Drop the Brand column
df1.drop(columns=['Brand'], inplace=True)

# Apply the function
df2['Title'] = df2.apply(combine_title_and_brand, axis=1)

# Drop the Brand column
df2.drop(columns=['Brand'], inplace=True)

# Apply the function
df3['Title'] = df3.apply(combine_title_and_brand, axis=1)

# Drop the Brand column
df3.drop(columns=['Brand'], inplace=True)

# Apply the function
df4['Title'] = df4.apply(combine_title_and_brand, axis=1)

# Drop the Brand column
df4.drop(columns=['Brand'], inplace=True)

# Drop the 'Date' column if it exists
df1 = df1.drop(columns=['Date'], errors='ignore')
df2 = df2.drop(columns=['Date'], errors='ignore')
df3 = df3.drop(columns=['Date'], errors='ignore')
df4 = df4.drop(columns=['Date'], errors='ignore')

# Drop the 'location' column if it exists
df1 = df1.drop(columns=['location'], errors='ignore')
df2 = df2.drop(columns=['location'], errors='ignore')
df3 = df3.drop(columns=['location'], errors='ignore')
df4 = df4.drop(columns=['location'], errors='ignore')

# Drop the 'Location' column if it exists
df1 = df1.drop(columns=['Location'], errors='ignore')
df2 = df2.drop(columns=['Location'], errors='ignore')
df3 = df3.drop(columns=['Location'], errors='ignore')
df4 = df4.drop(columns=['Location'], errors='ignore')

# Drop the 'Transmission' column if it exists
df1 = df1.drop(columns=['Transmission'], errors='ignore')
df2 = df2.drop(columns=['Transmission'], errors='ignore')
df3 = df3.drop(columns=['Transmission'], errors='ignore')
df4 = df4.drop(columns=['Transmission'], errors='ignore')


# Drop the 'Phone' column if it exists
df1 = df1.drop(columns=['Phone'], errors='ignore')
df2 = df2.drop(columns=['Phone'], errors='ignore')
df3 = df3.drop(columns=['Phone'], errors='ignore')
df4 = df4.drop(columns=['Phone'], errors='ignore')


print("Brand and Title combined / Dropping Date ,Location and Phone:")

print("df1:\n",df1)
print("df2:\n",df2)
print("df3:\n",df3)
print("df4:\n",df4)

# Concatenate datasets
combined_df = pd.concat([df1, df2], ignore_index=True)
combined_df.to_csv("clean_data/preset1.csv", index=False)

# Display the combined DataFrame
print(combined_df)