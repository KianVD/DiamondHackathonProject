import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import joblib

# Step 1: Load the saved model
def make_preds():
    print("Function is called")
    model = load_model("credit_risk_model.h5")

    # Step 2: Load the saved scaler
    scaler = joblib.load('scaler.pkl')

    # Step 3: Load new data (no 'user' column in new data)
    new_data = pd.read_csv("../data/test_data.csv")  # Replace with the actual file path

    # Step 4: Aggregate new data by user (assuming the data has a column like 'transaction_id' and 'amount_before')
    new_data['user_id'] = 1  # Create a dummy user ID (0, 1, 2, ...)

    # Step 5: Aggregate new data by the dummy 'user_id'
    new_user_features = new_data.groupby('user_id').agg(
        total_transactions=('transaction_id', 'count'),
        avg_amount_before=('amount_before', 'mean'),
        avg_amount_after=('amount_after', 'mean'),
        max_amount_before=('amount_before', 'max'),
        min_amount_before=('amount_before', 'min'),
        max_amount_after=('amount_after', 'max'),
        min_amount_after=('amount_after', 'min')
    ).reset_index()
    new_user_features['card_number'] = new_data.loc[0,'card_number']
    new_user_features.to_json('new_user_features.json', orient='records', lines=True)
    del new_user_features['card_number']
    # Step 5: Preprocess the new data by scaling it
    X_new_scaled = scaler.transform(new_user_features.drop('user_id', axis=1))  # Drop user_id (the identifier)

    # Step 6: Make predictions on the new data
    predictions = model.predict(X_new_scaled)
    predicted_classes = np.argmax(predictions, axis=1)  # Get the class with the highest probability

    # Step 7: Display predictions
    ans = ''
    for user, pred in zip(new_user_features['user_id'], predicted_classes):
        risk_label = {0: 'Low Risk', 1: 'Medium Risk', 2: 'High Risk'}[pred]
        print(f"User: {user}, Predicted Credit Risk: {risk_label}")
        ans = risk_label
    print(ans)
    return ans


