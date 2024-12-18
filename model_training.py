# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.ensemble import GradientBoostingRegressor

# Load the dataset
df = pd.read_csv('clean_data/preset2.csv')  # Replace with your cleaned file path

# Display first few rows
print("Dataset Overview:")
print(df.head())

# Step 1: Data Preprocessing
# Drop rows with missing Price values (target variable)
df = df.dropna(subset=['Price'])

# Drop any irrelevant columns (example: an index or ID column if present)
# df = df.drop(['Unnamed: 0'], axis=1)  # Uncomment if needed

# Step 2: Handle Categorical Data
# Define features and target
X = df.drop(columns=['Price'])  # Features (all except Price)
y = df['Price']  # Target variable

# Encode categorical columns using One-Hot Encoding
X = pd.get_dummies(X, columns=['Brand', 'Core_Model', 'Specifications','Year', 'Fuel'], drop_first=True)

# Step 3: Split the Data into Training and Testing Sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Step 4: Train Multiple Models and Compare Predictions
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "XGBoost": XGBRegressor(n_estimators=100, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, random_state=42)
}

# Step 5: Train, Predict and Evaluate Models
results = {}

for model_name, model in models.items():
    print(f"\nTraining and Evaluating: {model_name}")
    # Train the model
    model.fit(X_train, y_train)
    # Predict on test data
    y_pred = model.predict(X_test)

    # Evaluate the model
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    # Store results
    results[model_name] = {'MAE': mae, 'RMSE': rmse, 'R2': r2}

    # Display results
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
    print(f"R-squared (R2): {r2:.2f}")

# Step 6: Compare Model Performance
print("\nModel Comparison:")
result_df = pd.DataFrame(results).T
print(result_df)

# Optional: Visualize Model Performance
import matplotlib.pyplot as plt

result_df.plot(kind='bar', figsize=(10, 6))
plt.title('Model Comparison: MAE, RMSE, and R2')
plt.ylabel('Metrics')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
