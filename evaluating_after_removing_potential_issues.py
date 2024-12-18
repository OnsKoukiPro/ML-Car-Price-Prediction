import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('clean_data/preset1_cleaned_final.csv')

# 1. Remove cars with mileage above 500,000
df_cleaned = df[df['Mileage'] <= 500000]

# 2. Limit the year to 2000
df_cleaned = df_cleaned[df_cleaned['Year'] >= 2000]

# 3. Handle missing mileage for new cars and remove rows with missing mileage for older cars
# Define the threshold for recent cars (e.g., 3 years ago)
current_year = datetime.now().year
recent_year_threshold = current_year - 3

# Keep rows with missing mileage if the year is recent (within 5 years)
df_cleaned.loc[(df_cleaned['Mileage'].isnull()) & (df_cleaned['Year'] >= recent_year_threshold), 'Mileage'] = None

# Remove rows where mileage is missing for older cars
df_cleaned = df_cleaned[~((df_cleaned['Mileage'].isnull()) & (df_cleaned['Year'] < recent_year_threshold))]

# 4. Remove prices below 8,000 or above 500,000
df_cleaned = df_cleaned[(df_cleaned['Price'] >= 8000) & (df_cleaned['Price'] <= 500000)]


df_cleaned.to_csv('clean_data/evaluating_after_removing_potential_issues.csv', index=False)

# Boxplots for detecting outliers
plt.figure(figsize=(14, 5))

# Boxplot for Mileage
plt.subplot(1, 3, 1)
sns.boxplot(data=df_cleaned, x='Mileage')
plt.title('Mileage Boxplot 2')

# Boxplot for Year
plt.subplot(1, 3, 2)
sns.boxplot(data=df_cleaned, x='Year')
plt.title('Year Boxplot 2')

# Boxplot for Price
plt.subplot(1, 3, 3)
sns.boxplot(data=df_cleaned, x='Price')
plt.title('Price Boxplot 2')

plt.tight_layout()
plt.show()