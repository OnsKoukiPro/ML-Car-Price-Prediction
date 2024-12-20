import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import r2_score, mean_squared_error

from sklearn.preprocessing import LabelEncoder
lab = LabelEncoder()

import warnings
warnings.filterwarnings('ignore')

data =pd.read_csv('../Step 2/updated_dataset.csv')

print("data head:\n",data.head())

print("data shape:\n",data.shape)

print("data info:")
data.info()

print("data duplicated:\n",data.duplicated().sum())

data.drop_duplicates(inplace= True)

print("data missing:\n",data.isna().sum())

print("data unique:\n",data.nunique())

print("data describe:\n",data.describe())



data=data.drop(['Car ID','Nombre de portes'],axis=1)

dtime = dt.datetime.now()
data['Age']=dtime.year - data['Année']
data = data.drop('Année',axis=1)
print("data head:\n",data.head())

# Converting Mileage type to int64
data.Kilométrage = data.Kilométrage.astype('Int64')
data.Kilométrage.head()

for col in data.columns:
    print(f'Category in {col} is :\n {data[col].unique()}\n')
    print('\\'*50)

# Save the cleaned dataset to a new CSV file
data.to_csv('updated_dataset.csv', index=False)

print("Columns cleaned and saved as 'updated_dataset.csv'.")