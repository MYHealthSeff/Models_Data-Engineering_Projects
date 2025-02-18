Preprocessed Healthcare Pricing Dataset

Overview:
This dataset contains preprocessed medical billing data, including pricing, payer information, and service classifications. It is structured to support AI/ML models, NLP processing, and data analysis.

Data Source:
* Extracted from real-world claims and reimbursement data
* Cleaned and structured for predictive modeling and cost estimation

File Details:
Ed_analytics_data.json: Structured FHIR healthcare data.  
ICD-10 to procedure mappings for medical coding.  
HL7 v2 messages for patient records.  
DICOM metadata samples (excluding images).  
Generic dataset for ML preprocessing.  
description: Medical procedure or product name
code|1, code|2: Unique medical codes (CDM, HCPCS, CPT, etc.)
payer_name: Name of the insurance provider
standard_charge|gross: Gross billing price before discounts
standard_charge|negotiated_dollar: Negotiated price between provider and insurer
estimated_amount: Expected patient cost after insurance

Potential Use Cases:
Price Transparency Analysis: Compare real vs. estimated costs
ML Model Training: Train models to predict out-of-pocket expenses
Data Visualization: Generate insights into medical pricing trends
