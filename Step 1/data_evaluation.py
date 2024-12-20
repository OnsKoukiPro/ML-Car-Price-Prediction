import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset without changing column names
df = pd.read_csv('../dataconcat and cleaning/updated_dataset.csv')

# Step 1: Basic Data Exploration

# 1.1 Check the first few rows of the dataset
print("Check the first few rows of the dataset")
print(df.head())

# 1.2 Get the basic information about the dataset
print("Get the basic information about the dataset")
print(df.info())

# 1.3 Check for any missing values
print("Check for any missing values")
print(df.isnull().sum())

# 1.4 Summary statistics for numeric columns
print("Summary statistics for numeric columns")
print(df.describe())

# 1.5 Data types of the columns
print("Data types of the columns")
print(df.dtypes)

# Step 2: Visualize Data Distribution

# 2.1 Distribution of prices
plt.figure(figsize=(10, 6))
sns.histplot(df['Price'], kde=True, bins=30)
plt.title('Price Distribution')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()

# 2.2 Price vs. Mileage
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Kilométrage', y='Price', data=df)
plt.title('Price vs Mileage')
plt.xlabel('Mileage')
plt.ylabel('Price')
plt.show()

# 2.3 Price vs. Year
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Année', y='Price', data=df)
plt.title('Price vs Year')
plt.xlabel('Year')
plt.ylabel('Price')
plt.show()

# 2.4 Price vs. Fuel type (Box plot)
plt.figure(figsize=(10, 6))
sns.boxplot(x='Énergie', y='Price', data=df)
plt.title('Price vs Fuel Type')
plt.xlabel('Fuel')
plt.ylabel('Price')
plt.show()

# 2.5 Price vs. Brand (Box plot)
plt.figure(figsize=(12, 6))
sns.boxplot(x='Brand', y='Price', data=df)
plt.title('Price vs Brand')
plt.xlabel('Brand')
plt.ylabel('Price')
plt.xticks(rotation=90)
plt.show()

# Step 3: Correlation Heatmap

# Extract the year from 'Année' for correlation analysis
df['Year'] = df['Année']

# Select only numeric columns for correlation calculation
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

# Compute the correlation matrix for numeric columns
corr = df[numeric_cols].corr()

# Plot the correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', cbar=True)
plt.title('Correlation Heatmap')
plt.show()
