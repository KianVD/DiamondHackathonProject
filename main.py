import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from gemini_api import gemini_api
from gemini_functions import generate_concise_report, interactive_query_interface, detect_anomalies, forecast_risk_trends

print("Current working directory:", os.getcwd())


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
