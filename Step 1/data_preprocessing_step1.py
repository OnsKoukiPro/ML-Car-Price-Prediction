import pandas as pd

# Display Settings for Pandas
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', 10)      # Limit rows for better readability
pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping

# ---------------------------
# 1. Load Datasets
# ---------------------------
df1 = pd.read_csv("../data/car_listings.csv")
df2 = pd.read_csv("../data/car_listings_autoprix.csv")
df3 = pd.read_csv("../data/car_listings_baniola2.csv")
df4 = pd.read_csv("../data/car_listings_karahba.csv")

# ---------------------------
# 2. Rename Columns for Consistency
# ---------------------------
df1.rename(columns={'title': 'Make', 'car_year': 'Year'}, inplace=True)
df2.rename(columns={'title': 'Title', 'price': 'Price', 'year': 'Year', 'fuel_type': 'Fuel', 'mileage': 'Mileage'}, inplace=True)
df3.rename(columns={'Price (TND)': 'Price', 'Fuel Type': 'Fuel'}, inplace=True)
df4.rename(columns={'brand': 'Make', 'manufacture_year': 'Year'}, inplace=True)

# ---------------------------
# 3. Define Unified Columns
# ---------------------------
columns_df1 = ['Title', 'Mileage', 'Year', 'Transmission', 'Fuel', 'Price']
columns_df2 = ['Title', 'location', 'Price', 'Year', 'Mileage', 'Fuel']
columns_df3 = ['Price', 'Location', 'Title', 'Fuel', 'Year']
columns_df4 = ['Title', 'Brand', 'Price', 'Mileage', 'Phone', 'Location', 'Date']

# Combine all columns to identify unique ones
all_columns = set(columns_df1 + columns_df2 + columns_df3 + columns_df4)

# Determine common columns
common_columns = list(set(columns_df1) & set(columns_df2) & set(columns_df3) & set(columns_df4))

# Arrange columns: common columns first, followed by unique ones
ordered_columns = common_columns + sorted(all_columns - set(common_columns))

# Function to rearrange and fill missing columns
def rearrange_columns(df, column_order):
    return df.reindex(columns=column_order, fill_value=None)

# Rearrange columns in each DataFrame
df1 = rearrange_columns(df1, ordered_columns)
df2 = rearrange_columns(df2, ordered_columns)
df3 = rearrange_columns(df3, ordered_columns)
df4 = rearrange_columns(df4, ordered_columns)

# ---------------------------
# 4. Combine 'Title' and 'Brand' Columns
# ---------------------------
def combine_title_and_brand(row):
    title = row['Title']
    brand = row['Brand']

    if pd.isna(brand) or brand == 'None':  # If no brand exists, keep title
        return title
    elif brand in title:  # If brand is already in title, return title
        return title
    else:  # Combine brand and title
        return f"{brand} {title}"

# Apply the function to each dataset
for df in [df1, df2, df3, df4]:
    df['Title'] = df.apply(combine_title_and_brand, axis=1)
    df.drop(columns=['Brand'], inplace=True, errors='ignore')

# ---------------------------
# 5. Drop Unnecessary Columns
# ---------------------------
columns_to_drop = ['Date', 'location', 'Location', 'Transmission', 'Phone']

for df in [df1, df2, df3, df4]:
    df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

# ---------------------------
# 6. Combine Datasets and Export
# ---------------------------
combined_df = pd.concat([df1, df2, df3, df4], ignore_index=True)

# Save the combined data to CSV
combined_df.to_csv("preset1.csv", index=False)

# Display Final Output
print("Final Combined DataFrame:")
print(combined_df.head())
