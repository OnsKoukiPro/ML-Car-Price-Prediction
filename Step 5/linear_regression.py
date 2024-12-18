
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Load the dataset
df = pd.read_csv('../Step 4/preset4.csv')

# Step 1: Data Exploration
# Check for missing values
print("Missing values in each column:")
print(df.isnull().sum())

# Check for duplicates in the dataset
print(f"Number of duplicate rows: {df.duplicated().sum()}")

# Display the data types of columns
print(f"Data types of columns:\n{df.dtypes}")

# Check the number of unique values for each column
print(f"Unique values in each column:\n{df.nunique()}")

# Get statistical summary of the dataset
print(f"Statistical summary of the dataset:\n{df.describe()}")

# Step 2: Explore Categorical Columns
categorical_columns = ['Brand', 'Core_Model', 'Specifications', 'Fuel']
for col in categorical_columns:
    print(f"Categories in {col}: {df[col].unique()}")

# Step 3: Encode Categorical Variables using Label Encoding
label_encoder = LabelEncoder()
for column in categorical_columns:
    df[column] = label_encoder.fit_transform(df[column])

# Step 4: Feature Scaling for Numerical Columns
scaler = StandardScaler()
numerical_columns = ['Year', 'Mileage', 'Price']
df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

# Step 5: Split the Data into Training and Test Sets
X = df.drop(['Price'], axis=1)  # Features
y = df['Price']  # Target variable
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 6: Model Training (Linear Regression)
model = LinearRegression()
model.fit(X_train, y_train)

# Step 7: Predictions
y_pred = model.predict(X_test)

# Step 8: Evaluate the Model
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

# Display the results
print(f"\nLinear Regression Model Evaluation:")
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"R-squared (R2): {r2:.2f}")

# Step 9: Inverse Scaling for the Predicted and Actual Values
# Reverse the scaling for only the 'Price' column
y_test_actual = scaler.inverse_transform(np.concatenate([X_test[['Year', 'Mileage']].values, y_test.values.reshape(-1, 1)], axis=1))[:, -1]  # Actual values (Price)
y_pred_actual = scaler.inverse_transform(np.concatenate([X_test[['Year', 'Mileage']].values, y_pred.reshape(-1, 1)], axis=1))[:, -1]  # Predicted values (Price)

# Step 10: Visualize Actual vs Predicted Prices
plt.figure(figsize=(10, 6))
plt.plot(y_test_actual, label='Actual Price', color='blue', linestyle='-', marker='o')
plt.plot(y_pred_actual, label='Predicted Price', color='red', linestyle='--', marker='x')

# Calculate the difference between actual and predicted prices
difference = y_test_actual - y_pred_actual
plt.plot(difference, label='Difference (Actual - Predicted)', color='green', linestyle=':', marker='^')

# Customize the plot
plt.title('Actual vs Predicted Price with Difference')
plt.xlabel('Sample Index')
plt.ylabel('Price (Original Scale)')
plt.legend()
plt.tight_layout()
plt.show()

# Step 11: Comparison of Actual vs Predicted Values
pred_df = pd.DataFrame({'Actual Value': y_test_actual.flatten(), 'Predicted Value': y_pred_actual.flatten(), 'Difference': difference.flatten()})
print(pred_df)






