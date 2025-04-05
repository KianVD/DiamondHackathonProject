import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt

# Load the transaction data
df = pd.read_csv("MOCK_DATA.csv")

# Inspect the columns to confirm the names of the identifier and amount columns.
print("Columns in dataset:", df.columns.tolist())

# -------------------------------
# Step 1: Aggregate user-level features
# -------------------------------
# Aggregating the data by user and including additional features
# We will include transaction-related features like:
# - 'transaction_type': type of transaction (encoded)
# - 'transaction_category': category of transaction (encoded)
# - 'location': location of transaction (encoded)
# - 'amount_before': amount before the transaction (numerical)
# - 'amount_after': amount after the transaction (numerical)

# Perform one-hot encoding for categorical features
categorical_columns = ['transaction_type', 'transaction_category', 'location']
encoder = OneHotEncoder(sparse=False, drop='first')  # Drop first to avoid multicollinearity
encoded_features = encoder.fit_transform(df[categorical_columns])

# Convert the encoded features back to a DataFrame with proper column names
encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(categorical_columns))

# Concatenate the encoded features with the original DataFrame
df_encoded = pd.concat([df, encoded_df], axis=1)

# Aggregate the data by user
user_features = df_encoded.groupby('user').agg(
    total_amount=('transaction_amount', 'sum'),
    transaction_count=('transaction_amount', 'count'),
    avg_amount=('transaction_amount', 'mean'),
    total_amount_before=('amount_before', 'sum'),
    total_amount_after=('amount_after', 'sum')
).reset_index()

# Add the encoded categorical features (aggregating by sum or average)
encoded_features_per_user = df_encoded.groupby('user')[encoded_df.columns].sum().reset_index()
user_features = user_features.merge(encoded_features_per_user, on='user', how='left')

print("Sample aggregated user features with additional features:")
print(user_features.head())

# -------------------------------
# Step 2: Apply k-means clustering
# -------------------------------
# Now we use all relevant features for clustering
features_for_clustering = user_features.drop(columns=['user'])

# Apply k-means clustering to form 3 clusters.
kmeans = KMeans(n_clusters=3, random_state=42)
user_features['cluster'] = kmeans.fit_predict(features_for_clustering)

# Determine cluster ordering based on average total_amount.
# We assume that users with a higher total transaction amount are considered higher credit risk.
cluster_order = user_features.groupby('cluster')['total_amount'].mean().sort_values().index.tolist()

# Map clusters to risk levels:
#   Lowest total_amount  -> "Low Risk"
#   Medium total_amount  -> "Medium Risk"
#   Highest total_amount -> "High Risk"
risk_labels = {cluster_order[0]: 'Low Risk', 
               cluster_order[1]: 'Medium Risk', 
               cluster_order[2]: 'High Risk'}
user_features['credit_risk'] = user_features['cluster'].map(risk_labels)

print("User features with assigned credit risk:")
print(user_features[['user', 'total_amount', 'credit_risk']].head())

# -------------------------------
# Step 3: Visualize the clusters
# -------------------------------
# We can create a scatter plot using two aggregated features.
# For example, plot total transaction amount (x-axis) vs. total amount before the transaction (y-axis),
# coloring by cluster assignment and annotating with the risk level.

plt.figure(figsize=(8, 6))
scatter = plt.scatter(user_features['total_amount'], 
                      user_features['total_amount_before'], 
                      c=user_features['cluster'], cmap='viridis', s=50)
plt.xlabel('Total Transaction Amount')
plt.ylabel('Total Amount Before Transaction')
plt.title('User Clusters by Credit Risk')
plt.colorbar(scatter, ticks=[0, 1, 2], label='Cluster')
# Optionally, annotate a few points with their risk labels for clarity.
for i in range(min(10, len(user_features))):
    plt.annotate(user_features['credit_risk'].iloc[i],
                 (user_features['total_amount'].iloc[i], user_features['total_amount_before'].iloc[i]),
                 fontsize=8, alpha=0.75)
plt.show()

# -------------------------------
# Step 4: Merge credit risk back to the transaction dataset
# -------------------------------
# Join the credit risk labels back to the original transaction records based on 'user_id'.
df = df.merge(user_features[['user', 'credit_risk']], on='user', how='left')

print("Transaction data with credit risk labels:")
print(df.head())

# Optionally, save the updated dataset to a new CSV file.
df.to_csv('MOCK_DATA_with_credit_risk.csv', index=False)
