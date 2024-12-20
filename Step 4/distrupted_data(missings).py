import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load the dataset
data = pd.read_csv('updated_dataset.csv')

# Print basic dataset information
print("data head:\n", data.head())
print("data shape:\n", data.shape)
print("data info:")
data.info()
print("data duplicated:\n", data.duplicated().sum())
print("data missing:\n", data.isna().sum())
print("data unique:\n", data.nunique())
print("data describe:\n", data.describe())

# Visualizations (example plots)

# Plot distribution of 'Price'
plt.figure(figsize=(10, 6))
sns.histplot(data['Price'], kde=True, bins=30)
plt.title('Price Distribution')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()

# Plot correlation heatmap for numerical columns
numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
corr = data[numeric_cols].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', cbar=True)
plt.title('Correlation Heatmap')
plt.show()

# Scatter plot for 'Kilométrage' vs 'Price'
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Kilométrage', y='Price', data=data)
plt.title('Kilométrage vs Price')
plt.xlabel('Kilométrage')
plt.ylabel('Price')
plt.show()

# Bar plot for 'Transmission' vs 'Price'
plt.figure(figsize=(10, 6))
sns.boxplot(x='Transmission', y='Price', data=data)
plt.title('Transmission vs Price')
plt.xlabel('Transmission')
plt.ylabel('Price')
plt.show()

# For categorical features, you can also visualize unique categories
for col in data.columns:
    print(f'Category in {col} is :\n {data[col].unique()}\n')
    print('\\'*50)
