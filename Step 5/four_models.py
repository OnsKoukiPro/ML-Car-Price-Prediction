import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import LabelEncoder

# Initialize LabelEncoder and warnings filter
lab = LabelEncoder()
import warnings

warnings.filterwarnings('ignore')

# Load dataset
data = pd.read_csv('updated_dataset.csv')

# Split the dataset into object and numeric columns
obdata = data.select_dtypes(include=object)
numdata = data.select_dtypes(exclude=object)

# Label encoding for categorical variables
for i in range(0, obdata.shape[1]):
    obdata.iloc[:, i] = lab.fit_transform(obdata.iloc[:, i])

# Combine the transformed categorical and numerical data
data = pd.concat([obdata, numdata], axis=1)

# Define features and target variable
x = data.drop('Price', axis=1)
y = data['Price']

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=5)

# Define models to be evaluated
algorithm = ['LinearRegression', 'DecisionTreeRegressor', 'RandomForestRegressor', 'GradientBoostingRegressor']

# Initialize lists to store R2 and RMSE scores
R2 = []
RMSE = []


# Function to evaluate models
def models(model):
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)

    # Calculate R2 and RMSE
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    # Append scores to respective lists
    R2.append(r2)
    RMSE.append(rmse)

    # Print model type and performance
    print(f'\nModel: {type(model).__name__}')
    print(f'The Score of {type(model).__name__} model is: {model.score(x_test, y_test)}')
    print(f'R²: {r2:.4f}, RMSE: {rmse:.4f}')

    # Create and display DataFrame for actual vs predicted values
    pred_df = pd.DataFrame({'Actual Value': y_test, 'Predicted Value': y_pred, 'Difference': y_test - y_pred})
    print(pred_df.head())  # Print the first few rows of predictions


# Initialize the models with specified parameters for DecisionTreeRegressor
model1 = LinearRegression()
# Best parameters: {'ccp_alpha': 0.01, 'max_depth': 15, 'min_samples_leaf': 1, 'min_samples_split': 10}

model2 = DecisionTreeRegressor(ccp_alpha=0.01, max_depth=15, min_samples_leaf=1, min_samples_split=10)
model3 = RandomForestRegressor()
model4 = GradientBoostingRegressor()

# Evaluate each model
models(model1)
models(model2)  # Now using the Decision Tree with the specified parameters
models(model3)
models(model4)

# Optionally, print the list of R2 and RMSE for all models
print("\nR² for all models:", R2)
print("RMSE for all models:", RMSE)
