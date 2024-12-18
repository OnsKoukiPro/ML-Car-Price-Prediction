import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned dataset
df = pd.read_csv('preset2.csv')

# Drop rows with missing values in key columns
df = df.dropna(subset=['Mileage', 'Year', 'Price'])

# Function to plot boxplots
def plot_boxplots(df, columns, titles=None):
    plt.figure(figsize=(5 * len(columns), 5))
    for i, column in enumerate(columns):
        plt.subplot(1, len(columns), i + 1)
        sns.boxplot(data=df, x=column)
        plt.title(titles[i] if titles else column)
    plt.tight_layout()
    plt.show()

# Call the function for specific columns
columns = ['Mileage', 'Year', 'Price']
titles = ['Mileage Boxplot', 'Year Boxplot', 'Price Boxplot']
plot_boxplots(df, columns, titles)

# Display summary statistics
print("Summary Statistics:")
print(df[columns].describe())
