import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('preset3.csv')


# Boxplots for detecting outliers
plt.figure(figsize=(14, 5))

# Boxplot for Mileage
plt.subplot(1, 3, 1)
sns.boxplot(data=df, x='Mileage')
plt.title('Mileage Boxplot 2')

# Boxplot for Year
plt.subplot(1, 3, 2)
sns.boxplot(data=df, x='Year')
plt.title('Year Boxplot 2')

# Boxplot for Price
plt.subplot(1, 3, 3)
sns.boxplot(data=df, x='Price')
plt.title('Price Boxplot 2')

plt.tight_layout()
plt.show()