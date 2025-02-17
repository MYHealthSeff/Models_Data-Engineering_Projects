from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import pickle

# Load dataset
dataset_path = "healthcare_dataset.csv"
df = pd.read_csv(dataset_path)

# Data Preprocessing
def preprocess_and_validate(df):
    # Drop duplicates and null values
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    
    # Define valid code mappings
    codes_icd10 = ["J20.9", "I10", "E11.9", "R07.2", "R10.9", "Q87.19", "E78.6"]
    codes_hcpcs = ["J1335", "A0428", "A9273", "J1100", "J2505", "J3301", "J0585"]
    codes_ndc = ["44567082010", "12345678901", "23456789012", "34567890123"]
    codes_drg = ["001-1", "002-2", "003-3", "004-4"]
    codes_cpt = ["81403", "70450", "99213", "96372"]
    valid_codes = codes_icd10 + codes_hcpcs + codes_ndc + codes_drg + codes_cpt

    # Validate code mappings
    if not all(df["code|1"].isin(valid_codes)):
        raise ValueError("Invalid codes found in dataset.")
    
    return df

# Apply preprocessing and validation
df = preprocess_and_validate(df)

# Vectorize the "description" column
vectorizer = TfidfVectorizer(max_features=5000)  # Ensure max_features matches Core ML input
description_vectors = vectorizer.fit_transform(df["description"]).toarray()

# Fix vectorizer output dimension mismatch
# Pad with zeros if the vectorized output has fewer dimensions than 5000
if description_vectors.shape[1] < 5000:
    padded_vectors = np.zeros((description_vectors.shape[0], 5000))
    padded_vectors[:, :description_vectors.shape[1]] = description_vectors
    description_vectors = padded_vectors

# Confirm the array shape matches the Core ML model requirements
assert description_vectors.shape[1] == 5000, "Vectorizer output dimension mismatch."

# Save the vectorizer and vectorized data
vectorizer_path = "vectorizer_new.pkl"
description_vectors_path = "description_vectors.pkl"

with open(vectorizer_path, "wb") as f:
    pickle.dump(vectorizer, f)

with open(description_vectors_path, "wb") as f:
    pickle.dump(description_vectors, f)

# Print information for confirmation
print(description_vectors.shape)  # Ensure the first dimension matches 5000
print(f"Vectorizer saved to {vectorizer_path}")
print(f"Vectorized data saved to {description_vectors_path}")
