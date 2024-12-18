import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,r2_score

import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('clean_data/preset2.csv')

df.isnull().sum()
print(df.isnull().sum())
# Check Duplication
print(df.duplicated().sum())
# Check datatype
print(df.dtypes)
# Check the number of unique values of each column
print(df.nunique())
# Check statistics of data set
print(df.describe())
categorical_columns = ['Brand', 'Core_Model', 'Specifications', 'Fuel']

for col in categorical_columns:
    print(f"Category in {col} is : {df[col].unique()}")

# Distribution of Numerical Features
numerical_columns = ['Year','Mileage','Price']

# plt.figure(figsize=(12, 8))
# for feature in numerical_columns:
#     plt.subplot(3, 5, numerical_columns.index(feature) + 1)
#     sns.histplot(data=df[feature], bins=20, kde=True)
#     plt.title(feature)
# plt.tight_layout()
# plt.show()
#
# # Price Analysis
# plt.figure(figsize=(8, 6))
# sns.histplot(data=df['Price'], bins=20, kde=True)
# plt.title('Distribution of Price')
# plt.show()
#
# # Create subplots
# fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(12, 9))
# axes = axes.ravel()  # Flatten the 2D array of axes
#
# # Define the list of categorical columns to analyze
# categorical_columns_to_show = ['Fuel']
#
# # Loop through each categorical column
# for i, column in enumerate(categorical_columns_to_show):
#     sns.countplot(x=df[column], data=df, palette='bright', ax=axes[i], saturation=0.95)
#     for container in axes[i].containers:
#         axes[i].bar_label(container, color='black', size=10)
#     axes[i].set_title(f'Count Plot of {column.capitalize()}')
#     axes[i].set_xlabel(column.capitalize())
#     axes[i].set_ylabel('Count')
#
# # Adjust layout and show plots
# plt.tight_layout()
# plt.show()
#
# # Calculate average price for each car model
# avg_prices_by_car = df.groupby('Brand')['Price'].mean().sort_values(ascending=False)
#
# # Plot top N car models by average price
# n = 10  # Number of top car models to plot
# top_car_models = avg_prices_by_car.head(n)
#
# plt.figure(figsize=(10, 6))
# sns.barplot(x=top_car_models.values, y=top_car_models.index)
# plt.title(f'Top {n} Car Models by Average Price')
# plt.xlabel('Average Price')
# plt.ylabel('Car Model')
# plt.tight_layout()
# plt.show()
#
# # Categorical Feature vs. Price
# plt.figure(figsize=(12, 8))
# for feature in categorical_columns:
#     plt.subplot(3, 3, categorical_columns.index(feature) + 1)
#     sns.boxplot(data=df, x=feature, y='Price')
#     plt.title(f'{feature} vs. Price')
# plt.tight_layout()
# plt.show()
#
# # Correlation Analysis
# correlation_matrix = df[numerical_columns].corr()
# plt.figure(figsize=(10, 8))
# sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
# plt.title('Correlation Heatmap')
# plt.show()

# Encoding categorical variables
label_encoder = LabelEncoder()
for column in categorical_columns:
    df[column] = label_encoder.fit_transform(df[column])

# Feature scaling
scaler = StandardScaler()
df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

# Splitting the dataset
X = df.drop(['Price'], axis=1)
y = df['Price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2_square = r2_score(y_test,y_pred)
print(f" R-squared: {r2_square}")
print(f'Mean Squared Error: {mse}')

pred_df=pd.DataFrame({'Actual Value':y_test,'Predicted Value':y_pred,'Difference':y_test-y_pred})
print(pred_df)