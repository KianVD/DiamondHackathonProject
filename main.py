import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from gemini_api import gemini_api
from gemini_functions import generate_concise_report, interactive_query_interface, detect_anomalies, forecast_risk_trends

print("Current working directory:", os.getcwd())

# -------------------------------
# Load the transaction data
# -------------------------------
# Use test data from Test_data.csv located in the data folder.
df = pd.read_csv("data/Test_data.csv")
print("Columns in dataset:", df.columns.tolist())

# -------------------------------
# Step 1: Aggregate user-level features
# -------------------------------
# Group by 'card_number' since the test data uses this as a unique identifier.
user_features = df.groupby('card_number').agg(
    total_amount=('transaction_amount', 'sum'),
    transaction_count=('transaction_amount', 'count'),
    avg_amount=('transaction_amount', 'mean')
).reset_index()

print("Sample aggregated user features:")
print(user_features.head())

# -------------------------------
# Step 2: Apply k-means clustering to assign credit risk
# -------------------------------
X = user_features[['total_amount']].values
kmeans = KMeans(n_clusters=3, random_state=42)
user_features['cluster'] = kmeans.fit_predict(X)

cluster_order = user_features.groupby('cluster')['total_amount'].mean().sort_values().index.tolist()
risk_labels = {
    cluster_order[0]: 'Low Risk',
    cluster_order[1]: 'Medium Risk',
    cluster_order[2]: 'High Risk'
}
user_features['credit_risk'] = user_features['cluster'].map(risk_labels)

print("User features with assigned credit risk:")
print(user_features[['card_number', 'total_amount', 'credit_risk']].head())

# -------------------------------
# Step 3: Visualize the clusters (optional)
# -------------------------------
plt.figure(figsize=(8, 6))
scatter = plt.scatter(
    user_features['total_amount'],
    user_features['transaction_count'],
    c=user_features['cluster'], cmap='viridis', s=50
)
plt.xlabel('Total Transaction Amount')
plt.ylabel('Transaction Count')
plt.title('User Clusters by Credit Risk')
plt.colorbar(scatter, ticks=[0, 1, 2], label='Cluster')
plt.show()

# -------------------------------
# Step 4: Merge credit risk back to the transaction dataset
# -------------------------------
df = df.merge(user_features[['card_number', 'credit_risk']], on='card_number', how='left')
print("Transaction data with credit risk labels:")
print(df.head())
df.to_csv('Test_data_with_credit_risk.csv', index=False)

# -------------------------------
# Gemini API Integration: Generate a concise report for one user.
# -------------------------------
# Choose one user (identified by card_number) for the concise report.
card_number = user_features['card_number'].iloc[0]
generate_concise_report(user_features, card_number)

# Optionally, you can use the interactive query interface.
# interactive_query_interface()

detect_anomalies(user_features)

historical_data = pd.DataFrame({
    'date': pd.date_range(start='2023-01-01', periods=12, freq='M'),
    'avg_total_amount': np.random.normal(loc=1000, scale=200, size=12)
})
forecast_risk_trends(historical_data)

prompt = "Explain how AI works"
generated_content = gemini_api.generate_content(prompt)
print("\nGenerated Content from Gemini API:")
print(generated_content)

# Pause to view output before exiting.
input("Press Enter to exit...")
