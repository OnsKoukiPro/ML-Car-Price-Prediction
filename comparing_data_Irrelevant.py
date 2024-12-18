import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load datasets
df1 = pd.read_csv('clean_data/preset1.csv')
df2 = pd.read_csv('clean_data/preset1.csv')


# Check if they are exactly the same
if df1.equals(df2):
    print("The datasets are identical.")
else:
    print("The datasets are different.")
