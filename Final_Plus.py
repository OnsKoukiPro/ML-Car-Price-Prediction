import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

from sklearn.preprocessing import LabelEncoder
lab = LabelEncoder()

import warnings
warnings.filterwarnings('ignore')
data = pd.read_csv('clean_data/preset2.csv')

obdata = data.select_dtypes(include=object)
numdata = data.select_dtypes(exclude=object)
for i in range(0,obdata.shape[1]):
    obdata.iloc[:,i] = lab.fit_transform(obdata.iloc[:,i])
data = pd.concat([obdata,numdata],axis=1)

x= data.drop('Price',axis=1)
y= data['Price']
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.25,random_state=5)
algorithm = ['LinearRegression','DecisionTreeClassifier','RandomForestClassifier','GradientBoostingRegressor','SVR']
R2=[]
RMSE = []


def models(model):
    model.fit(x_train,y_train)
    y_pred  = model.predict(x_test)
    r2 = r2_score(y_test,y_pred )
    rmse = np.sqrt(mean_squared_error(y_test,y_pred ))
    R2.append(r2)
    RMSE.append(rmse)
    score = model.score(x_test,y_test)
    print(f'The Score of Model is :{score}')
    pred_df = pd.DataFrame({'Actual Value': y_test, 'Predicted Value': y_pred , 'Difference': y_test - y_pred })
    print(pred_df)
model1 = LinearRegression()
model2 = DecisionTreeRegressor()
model3 = RandomForestRegressor()

models(model1)
models(model2)
models(model3)
