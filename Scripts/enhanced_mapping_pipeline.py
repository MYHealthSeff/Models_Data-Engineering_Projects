import pandas as pd
import json
import os

# File paths
hcpcs_file = "HCPC2025_JAN_ANWEB_12172024.csv"
addendum_a_file = "January_2025_Addendum_A.csv"
addendum_b_file = "January_2025_Addendum_B.csv"
icd10_file = "icd10_codesystem.json"
output_file = "mapped_data_final.json"

# Function to print and verify column names in a file
def inspect_columns(file_path):
    if os.path.exists(file_path):
        print(f"\nInspecting columns in file: {file_path}")
        data = pd.read_csv(file_path, nrows=5)  # Read a few rows to save time
        print(f"Columns in {file_path}: {list(data.columns)}")
        return list(data.columns)
    else:
        print(f"ERROR: File not found - {file_path}")
        return []

# Function to standardize column names
def standardize_columns(data, column_mapping, file_name):
    data.rename(columns=column_mapping, inplace=True)
    missing_columns = [col for col in column_mapping.values() if col not in data.columns]
    if missing_columns:
        print(f"WARNING: Missing columns in {file_name}: {missing_columns}")
    return data

# Preprocess HCPCS file
def preprocess_hcpcs(file_path):
    print(f"\nProcessing HCPCS file: {file_path}")
    hcpcs_column_mapping = {
        "LONG DESCRIPTION": "LONG_DESCRIPTION",
        "SHORT DESCRIPTION": "SHORT_DESCRIPTION",
        "SEQNUM": "SEQNUM",  # Ensure this column exists
        "HCPC": "HCPC",  # Ensure this column exists
    }
    hcpcs_data = pd.read_csv(file_path)
    # Explicitly cast to string to avoid FutureWarning
    hcpcs_data = hcpcs_data.astype(str)
    hcpcs_data.fillna("", inplace=True)
    hcpcs_data = standardize_columns(hcpcs_data, hcpcs_column_mapping, "HCPCS File")
    return hcpcs_data

# Preprocess Addendum A file
def preprocess_addendum_a(file_path):
    print(f"\nProcessing Addendum A file: {file_path}")
    addendum_a_column_mapping = {
        "Group Title": "Group_Title",
        "Relative Weight": "Relative_Weight",
        "Payment Rate": "Payment_Rate",
        "National Unadjusted Copayment": "National_Unadjusted_Copayment",
        "Minimum Unadjusted Copayment": "Minimum_Unadjusted_Copayment",
        "IRA Coinsurance percentage": "IRA_Coinsurance_Percentage",
        "Adjusted Beneficiary Copayment": "Adjusted_Beneficiary_Copayment",
        "Drug and Device Pass-Through Expiration during Calendar Year": "Drug_and_Device_Pass-Through_Expiration",
        "APC": "APC",  # Ensure this column exists
    }
    addendum_a_data = pd.read_csv(file_path, skiprows=2)
    addendum_a_data = addendum_a_data.astype(str)  # Explicitly cast to string
    addendum_a_data.fillna("", inplace=True)
    addendum_a_data = standardize_columns(addendum_a_data, addendum_a_column_mapping, "Addendum A File")
    return addendum_a_data

# Preprocess Addendum B file
def preprocess_addendum_b(file_path):
    print(f"\nProcessing Addendum B file: {file_path}")
    addendum_b_column_mapping = {
        "HCPCS Code": "HCPCS_Code",
        "Short Descriptor": "Short_Descriptor",
        "Relative Weight": "Relative_Weight",
        "Payment Rate": "Payment_Rate",
        "National Unadjusted Copayment": "National_Unadjusted_Copayment",
        "Minimum Unadjusted Copayment": "Minimum_Unadjusted_Copayment",
        "Drug and Device Pass-Through Expiration during Calendar Year": "Drug_and_Device_Pass-Through_Expiration",
    }
    addendum_b_data = pd.read_csv(file_path, skiprows=4)
    addendum_b_data = addendum_b_data.astype(str)  # Explicitly cast to string
    addendum_b_data.fillna("", inplace=True)
    addendum_b_data = standardize_columns(addendum_b_data, addendum_b_column_mapping, "Addendum B File")
    return addendum_b_data

# Load and process ICD-10 JSON
def load_icd10(file_path):
    print(f"\nLoading ICD-10 JSON file: {file_path}")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            icd10_data = json.load(f)
        return icd10_data
    else:
        print(f"ERROR: File not found - {file_path}")
        return {"concept": []}

# Perform mapping
def perform_mapping(hcpcs_data, addendum_a_data, addendum_b_data, icd10_data):
    print("\nPerforming ICD-10 mappings...")
    for concept in icd10_data["concept"]:
        icd_code = concept["code"]

        # Map to HCPCS
        matching_hcpcs = hcpcs_data[hcpcs_data["SEQNUM"] == icd_code]
        concept["HCPCS_Mappings"] = matching_hcpcs.to_dict(orient="records")

        # Map to Addendum A
        matching_apc = addendum_a_data[addendum_a_data["APC"].isin(matching_hcpcs["OPPS"].unique())]
        concept["Addendum_A_Mappings"] = matching_apc.to_dict(orient="records")

        # Map to Addendum B
        matching_b = addendum_b_data[addendum_b_data["HCPCS_Code"].isin(matching_hcpcs["HCPC"])]
        concept["Addendum_B_Mappings"] = matching_b.to_dict(orient="records")

    return icd10_data

# Save the final mapped data
def save_mapped_data(mapped_data, output_path):
    print(f"\nSaving mapped data to {output_path}...")
    with open(output_path, "w") as f:
        json.dump(mapped_data, f, indent=4)
    print(f"Mapped data saved to {output_path}\n")

# Main function
def main():
    # Inspect column names in input files
    inspect_columns(hcpcs_file)
    inspect_columns(addendum_a_file)
    inspect_columns(addendum_b_file)

    hcpcs_data = preprocess_hcpcs(hcpcs_file)
    addendum_a_data = preprocess_addendum_a(addendum_a_file)
    addendum_b_data = preprocess_addendum_b(addendum_b_file)
    icd10_data = load_icd10(icd10_file)
    mapped_data = perform_mapping(hcpcs_data, addendum_a_data, addendum_b_data, icd10_data)
    save_mapped_data(mapped_data, output_file)

# Run the script
if __name__ == "__main__":
    main()
