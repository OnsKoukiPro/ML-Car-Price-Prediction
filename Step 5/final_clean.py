import pandas as pd

df = pd.read_csv('../Step 4/updated_dataset.csv')

# 1. Store the original column names
original_columns = df.columns.copy()

# 2. Convert column names to lowercase
df.columns = df.columns.str.lower()

# 3. Convert data types (if needed)
df['price'] = df['price'].astype(float)
df['kilométrage'] = df['kilométrage'].astype(int)
df['age'] = df['age'].astype(float)


# 5. Handle outliers or unusual values
df = df[df['kilométrage'] > 0]
df = df[df['age'] > 0]

# 6. Handle missing values in categorical columns
# For 'énergie', 'type', and 'transmission', fill NaN with the most frequent value (mode)
df['énergie'] = df['énergie'].fillna(df['énergie'].mode()[0])
df['transmission'] = df['transmission'].fillna(df['transmission'].mode()[0])


# 8. Handle missing values for numerical columns (fill NaN with mean)
numerical_cols = ['price', 'kilométrage', 'age']
for col in numerical_cols:
    df[col] = df[col].fillna(df[col].mean())

# 9. Restore the original column capitalization
df.columns = original_columns

# 10. Output the cleaned data (for example, save to a new CSV)
df.to_csv('updated_dataset.csv', index=False)

# Preview the cleaned data
print(df.head())
