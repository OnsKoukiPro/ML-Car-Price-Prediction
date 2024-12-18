import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset (change the path to where your dataset is located)
# If your dataset is in CSV format, you can load it like this:
df = pd.read_csv('clean_data/preset1_cleaned_final.csv')

# Boxplots for detecting outliers
plt.figure(figsize=(14, 5))

# Boxplot for Mileage
plt.subplot(1, 3, 1)
sns.boxplot(data=df, x='Mileage')
plt.title('Mileage Boxplot 1')

# Boxplot for Year
plt.subplot(1, 3, 2)
sns.boxplot(data=df, x='Year')
plt.title('Year Boxplot 1')

# Boxplot for Price
plt.subplot(1, 3, 3)
sns.boxplot(data=df, x='Price')
plt.title('Price Boxplot 1')

plt.tight_layout()
plt.show()
