import coremltools as ct
import numpy as np
import json

# Path to your Core ML model
MODEL_PATH = "mlp_model.mlmodel"

# Path to your index-to-ICD10 mapping JSON
INDEX_TO_ICD10_PATH = "index_to_icd10.json"

def load_model(model_path):
    """
    Loads the Core ML model.
    """
    print(f"Loading Core ML model from {model_path}...")
    try:
        model = ct.models.MLModel(model_path)
        print("Model loaded successfully.")
        return model
    except Exception as e:
        print(f"Error loading Core ML model: {e}")
        return None

def load_index_to_icd10_mapping(mapping_path):
    """
    Loads the index-to-ICD10 mapping JSON.
    """
    print(f"Loading index-to-ICD10 mapping from {mapping_path}...")
    try:
        with open(mapping_path, "r") as f:
            mapping = json.load(f)
        print("Mapping loaded successfully.")
        return mapping
    except Exception as e:
        print(f"Error loading mapping: {e}")
        return None

def generate_random_embeddings():
    """
    Generates random embeddings to simulate the output of EmbeddingGenerator.
    Replace this with actual embeddings from your app if needed.
    """
    return np.random.uniform(-1.0, 1.0, size=(1, 768)).astype(np.float32)

def predict_with_model(model, embeddings):
    """
    Makes a prediction using the Core ML model.
    """
    print(f"Input Embeddings Shape: {embeddings.shape}")
    try:
        prediction = model.predict({"input_1": embeddings})
        print("Prediction successfully performed.")
        return prediction
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None

def main():
    # Load the Core ML model
    model = load_model(MODEL_PATH)
    if model is None:
        print("Exiting due to model loading error.")
        return

    # Load the index-to-ICD10 mapping
    index_to_icd10 = load_index_to_icd10_mapping(INDEX_TO_ICD10_PATH)
    if index_to_icd10 is None:
        print("Exiting due to mapping loading error.")
        return

    # Generate random embeddings
    embeddings = generate_random_embeddings()

    # Perform a prediction
    prediction = predict_with_model(model, embeddings)
    if prediction is None:
        print("Prediction failed.")
        return

    # Extract the output and map it to ICD-10
    try:
        predicted_array = prediction["Identity"]
        predicted_index = int(np.argmax(predicted_array))  # Get the index of the highest score
        print(f"Predicted Index: {predicted_index}")

        # Map index to ICD-10 code
        icd10_code = index_to_icd10.get(str(predicted_index), None)
        if icd10_code is not None:
            print(f"Predicted ICD-10 Code: {icd10_code}")
        else:
            print(f"No ICD-10 mapping found for index: {predicted_index}")

    except Exception as e:
        print(f"Error processing prediction output: {e}")

if __name__ == "__main__":
    main()
