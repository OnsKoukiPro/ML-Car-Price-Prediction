import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Load dataset
data = pd.read_csv('../Step 4/preset4.csv')

# Define the features including categorical variables
features = data[['Brand', 'Core_Model', 'Year', 'Fuel', 'Mileage', 'Price']]

# Initialize LabelEncoder for categorical columns
lab = LabelEncoder()

# Apply LabelEncoder to categorical columns
features.loc[:, 'Brand'] = lab.fit_transform(features['Brand'])
features.loc[:, 'Core_Model'] = lab.fit_transform(features['Core_Model'])
features.loc[:, 'Fuel'] = lab.fit_transform(features['Fuel'])

# Now we can scale the numeric columns
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)


# Define a function to plot clusters for different k values
def plot_clusters(k_values, scaled_features, data):
    plt.figure(figsize=(12, 8))

    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=5)
        data['Cluster'] = kmeans.fit_predict(scaled_features)

        plt.subplot(1, len(k_values), k_values.index(k) + 1)
        plt.scatter(data['Mileage'], data['Price'], c=data['Cluster'], cmap='viridis', s=50)
        plt.title(f'K-means Clustering: k={k}')
        plt.xlabel('Mileage')
        plt.ylabel('Price')
        plt.colorbar(label='Cluster')

    plt.tight_layout()
    plt.show()


# Plot the clustering results for 3, 4, and 5 clusters
plot_clusters([3, 4, 5], scaled_features, data)

# Optionally, print the cluster centers for each k
for k in [3, 4, 5]:
    kmeans = KMeans(n_clusters=k, random_state=5)
    kmeans.fit(scaled_features)
    print(f"Cluster Centers for k={k}:\n{kmeans.cluster_centers_}\n")

# Evaluate the performance of KMeans for each k
from sklearn.metrics import silhouette_score

for k in [3, 4, 5]:
    kmeans = KMeans(n_clusters=k, random_state=5)
    data['Cluster'] = kmeans.fit_predict(scaled_features)
    sil_score = silhouette_score(scaled_features, data['Cluster'])
    print(f"Silhouette Score for KMeans Clustering (k={k}): {sil_score:.4f}")
