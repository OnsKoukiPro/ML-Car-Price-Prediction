import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('../Step 4/preset4.csv')

# Display first few rows
print("Dataset Overview:")
print(df.head())

# Step 1: Data Preprocessing
# Drop rows with missing Price values (target variable)
df = df.dropna(subset=['Price'])

# Step 2: Handle Categorical Data
# Define features and target
X = df.drop(columns=['Price'])  # Features (all except Price)
y = df['Price']  # Target variable

# Encode categorical columns using One-Hot Encoding
X = pd.get_dummies(X, columns=['Brand', 'Core_Model', 'Specifications', 'Fuel'], drop_first=True)

# Step 3: Split the Data into Training and Testing Sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Step 4: Train Decision Tree Model with Best Parameters
best_params = {'ccp_alpha': 0.0, 'max_depth': 15, 'min_samples_leaf': 1, 'min_samples_split': 10}

# Initialize and train the model
decision_tree = DecisionTreeRegressor(**best_params)
decision_tree.fit(X_train, y_train)

# Predict on test data
y_pred = decision_tree.predict(X_test)

# Step 5: Evaluate the Model
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

# Display the results
print(f"\nDecision Tree Model Evaluation:")
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"R-squared (R2): {r2:.2f}")

# Step 6: Visualize Model Performance
results = {'MAE': mae, 'RMSE': rmse, 'R2': r2}

# Create a DataFrame for visualization
result_df = pd.DataFrame(results, index=[0])

# Plot the results
result_df.T.plot(kind='bar', figsize=(8, 5))
plt.title('Decision Tree Model Performance: MAE, RMSE, and R2')
plt.ylabel('Metric Values')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
