import pandas as pd
import json

# Load ICD-10 Mapping CSV
def load_icd10_mapping(csv_path="data/icd10_mappings.csv"):
    """Loads ICD-10 mappings from CSV."""
    return pd.read_csv(csv_path)

# Load FHIR JSON Data
def load_fhir_data(json_path="data/fhir_sample.json"):
    """Loads patient conditions from FHIR JSON dataset."""
    with open(json_path, "r") as file:
        fhir_data = json.load(file)
    
    # Extract conditions
    conditions = []
    for entry in fhir_data["entry"]:
        if entry["resource"]["resourceType"] == "Condition":
            condition = {
                "PatientID": entry["resource"]["patient"]["reference"].split("/")[-1],
                "ICD10_Code": entry["resource"]["code"]["coding"][0]["code"],
                "Condition": entry["resource"]["code"]["coding"][0]["display"]
            }
            conditions.append(condition)
    
    return pd.DataFrame(conditions)

# Merge ICD-10 with FHIR Data
def map_icd10_to_fhir():
    """Maps ICD-10 descriptions to FHIR patient conditions."""
    icd10_df = load_icd10_mapping()
    fhir_df = load_fhir_data()

    # Merge on ICD10 Code
    mapped_df = fhir_df.merge(icd10_df, left_on="ICD10_Code", right_on="icd10_code", how="left")
    mapped_df.drop(columns=["icd10_code"], inplace=True)  # Remove duplicate column

    return mapped_df

if __name__ == "__main__":
    mapped_data = map_icd10_to_fhir()
    mapped_data.to_csv("data/mapped_data.csv", index=False)
    print("ICD-10 & FHIR Data Mapping Complete! Saved as `mapped_data.csv`.")
