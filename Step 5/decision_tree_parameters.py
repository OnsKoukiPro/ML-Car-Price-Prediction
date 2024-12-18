import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeRegressor

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
X = pd.get_dummies(X, columns=['Brand', 'Core_Model', 'Specifications', 'Year', 'Fuel'], drop_first=True)

# Step 3: Split the Data into Training and Testing Sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Grid Search for hyperparameter tuning
param_grid = {
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'ccp_alpha': [0.0, 0.01, 0.1]
}
grid_search = GridSearchCV(DecisionTreeRegressor(), param_grid, cv=5, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)
print("Best parameters:", grid_search.best_params_)
