import pandas as pd
import logging
import random

# Setup logging
logging.basicConfig(
    filename='generate_clean_dataset_v2.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.info("Starting the dataset generation process...")

# File paths
input_standard_charges_path = "/Users/nathanculbreath/Documents/Building/MHAI_Build/MHAI/Standard_Charges.csv"
input_dxccsr_path = "/Users/nathanculbreath/Downloads/DXCCSR_v2025-1/DXCCSR_v2025-1/DXCCSR_v2025-1.csv"
input_prccsr_path = "/Users/nathanculbreath/Downloads/PRCCSR_v2025-1/PRCCSR_v2025-1/PRCCSR_v2025-1.csv"
output_cleaned_dataset_path = "/Users/nathanculbreath/Documents/Building/MHAI_Build/MHAI/healthcare_dataset_clean.csv"

# Load datasets with improved exception handling
def load_csv(file_path, file_label):
    try:
        logging.info(f"Loading {file_label} dataset from {file_path}...")
        df = pd.read_csv(file_path, encoding="utf-8", low_memory=False)
        logging.info(f"{file_label} dataset loaded successfully.")
        return df
    except FileNotFoundError:
        logging.error(f"{file_label} dataset not found at {file_path}. Please check the path.")
        raise
    except Exception as e:
        logging.error(f"An error occurred while loading {file_label} dataset: {e}")
        raise

# Load datasets
standard_charges = load_csv(input_standard_charges_path, "Standard Charges")
dxccsr = load_csv(input_dxccsr_path, "DXCCSR")
prccsr = load_csv(input_prccsr_path, "PRCCSR")

# Clean column names
def clean_columns(df, dataset_name):
    logging.info(f"Cleaning column names for {dataset_name} dataset...")
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace("'", "", regex=False)
    df.columns = df.columns.str.replace('"', "", regex=False)
    logging.info(f"Column names for {dataset_name} cleaned successfully.")
    return df

standard_charges = clean_columns(standard_charges, "Standard Charges")
dxccsr = clean_columns(dxccsr, "DXCCSR")
prccsr = clean_columns(prccsr, "PRCCSR")

# Ensure all required columns are present in the dataset
required_columns = [
    "description", "service|type", "pricing|gross", "pricing|discounted", "code|1|description", "code|2|description",
    "clinical_domain", "modifiers", "payer_name", "plan_name", "additional_generic_notes",
    "code|1", "code|1|type", "code|2", "code|2|type", "code|3", "code|3|type", "code|4", "code|4|type",
    "standard_charge|negotiated_dollar", "standard_charge|negotiated_percentage",
    "standard_charge|min", "standard_charge|max", "standard_charge|methodology", "estimated_amount"
]

def validate_and_fill_missing_columns(df, required_columns, dataset_name):
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        logging.warning(f"The following columns are missing from {dataset_name}: {missing_columns}")
        # Fill missing columns with default values
        for col in missing_columns:
            if "pricing" in col or "amount" in col or "percentage" in col:
                df[col] = 0  # Default for numeric columns
            else:
                df[col] = "Unknown"  # Default for text columns
    logging.info(f"Validation completed for {dataset_name}. All required columns are now present.")
    return df

standard_charges = validate_and_fill_missing_columns(standard_charges, required_columns, "Standard Charges")

# Add `service|type` column if missing
def add_service_type_column(df):
    if "service|type" not in df.columns:
        logging.info("Creating `service|type` column...")
        def determine_service_type(row):
            for col in ["code|2|type", "code|1|type", "code|3|type", "code|4|type"]:
                if col in row and pd.notna(row[col]):
                    return row[col]
            return "Unknown Type"
        df["service|type"] = df.apply(determine_service_type, axis=1)
        logging.info("`service|type` column created successfully.")
    return df

standard_charges = add_service_type_column(standard_charges)

# Sample the Standard Charges dataset
def sample_dataset(df, subset_size, dataset_name):
    logging.info(f"Sampling {subset_size} rows from {dataset_name} dataset...")
    subset_size = min(subset_size, len(df))
    if subset_size == 0:
        logging.error(f"{dataset_name} dataset is empty!")
        raise ValueError(f"The input {dataset_name} dataset is empty. Please check your source data.")
    sampled_df = df.sample(n=subset_size, random_state=42)
    logging.info(f"Sampled {subset_size} rows from {dataset_name} successfully.")
    return sampled_df

standard_charges_subset = sample_dataset(standard_charges, 1500, "Standard Charges")

# Save cleaned dataset
def save_cleaned_dataset(df, output_path):
    logging.info(f"Saving cleaned dataset to {output_path}...")
    df.to_csv(output_path, index=False)
    logging.info("Cleaned dataset saved successfully.")
    print(f"Cleaned dataset saved to {output_path}")

save_cleaned_dataset(standard_charges_subset, output_cleaned_dataset_path)

print("Dataset generation process completed successfully!")
