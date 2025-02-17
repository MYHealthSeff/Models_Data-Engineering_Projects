import pandas as pd
import numpy as np
import coremltools as ct
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def load_and_prepare_data(file_path):
    """Loads dataset and prepares it for ML training."""
    df = pd.read_csv(file_path)
    X = df.drop(columns=["target"])  # Adjust target column name
    y = df["target"]

    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train, y_train):
    """Trains a RandomForest classifier model."""
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def convert_to_coreml(model):
    """Converts trained model to CoreML format for iOS deployment."""
    coreml_model = ct.converters.sklearn.convert(model)
    coreml_model.save("models/ml_model.mlmodel")
    print("Model successfully converted to CoreML and saved.")

if __name__ == "__main__":
    file_path = "data/sample_ml_data.csv"  # Adjust accordingly
    X_train, X_test, y_train, y_test = load_and_prepare_data(file_path)

    model = train_model(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    print(f"Model Accuracy: {accuracy_score(y_test, y_pred):.4f}")

    # Convert and save CoreML model
    convert_to_coreml(model)
