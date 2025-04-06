import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import Adam
import joblib
# Load data (Assuming 'df' contains the transaction data)
# Aggregate the features by user
df = pd.read_csv("../data/MOCK_DATA_with_credit_risk.csv")
user_features = df.groupby('user').agg(
    total_transactions=('transaction_id', 'count'),
    avg_amount_before=('amount_before', 'mean'),
    avg_amount_after=('amount_after', 'mean'),
    max_amount_before=('amount_before', 'max'),
    min_amount_before=('amount_before', 'min'),
    max_amount_after=('amount_after', 'max'),
    min_amount_after=('amount_after', 'min')
).reset_index()

# Assuming 'y' is the target variable (credit risk)
y = df.groupby('user')['credit_risk'].first()  # Assuming the target is the same for each user
label_map = {
    "Low Risk": 1,
    "Medium Risk": 2,
    "High Risk": 3
}
y = y.map(label_map)

# Preprocessing: Standardizing the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(user_features.drop('user', axis=1))

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Define the model
model = models.Sequential([
    layers.InputLayer(input_shape=(X_scaled.shape[1],)),
    layers.Dense(128, activation='relu'),
    layers.Dense(64, activation='relu'),
    layers.Dense(32, activation='relu'),
    layers.Dense(3, activation='softmax')  # For 3 classes (Low, Medium, High Risk)
])

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.01), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.3)

# Evaluate the model
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {test_accuracy}")

# Save the model
model.save("credit_risk_model.h5")
joblib.dump(scaler, 'scaler.pkl')
# Make predictions on the test set
predictions = model.predict(X_test)
predicted_classes = np.argmax(predictions, axis=1)  # Get the class with the highest probability

# Display user name and prediction for test set
test_user_names = y_test.index # Get the user names corresponding to test set
for user, pred in zip(test_user_names, predicted_classes):
    risk_label = {0: 'Low Risk', 1: 'Medium Risk', 2: 'High Risk'}[pred]
    print(f"User: {user}, Predicted Credit Risk: {risk_label}")

# Compute confusion matrix
cm = confusion_matrix(y_test, predicted_classes)
print("\nConfusion Matrix:")
print(cm)

# Save the confusion matrix to a file (optional)
np.savetxt("confusion_matrix.txt", cm, fmt="%d")
