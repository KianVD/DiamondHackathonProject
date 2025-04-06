import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from tensorflow.keras.models import load_model
import joblib



new_data = pd.read_csv("dest_data.csv") #figure out where to get file from

model = load_model("credit_risk_model.h5") # load model

preprocessor = joblib.load("credit_risk_preprocessor.pkl")

"""# Identify column types
numeric_features = new_data.select_dtypes(include=["int64", "float64"]).columns.tolist()
categorical_features = new_data.select_dtypes(include=["object", "category"]).columns.tolist()

# Preprocessing pipeline
numeric_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(handle_unknown="ignore")

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ]
)"""

X_new_processed = preprocessor.transform(new_data)
predictions = model.predict(X_new_processed)
predicted_classes = (predictions > 0.5).astype(int)
print(predicted_classes)