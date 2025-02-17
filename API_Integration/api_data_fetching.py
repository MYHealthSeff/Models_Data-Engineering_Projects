import requests
import json

API_URL = "https://api.example.com/data"
API_KEY = "your_api_key_here"

def fetch_data(endpoint, params=None):
    """Fetches data from the API with authentication and error handling."""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(f"{API_URL}/{endpoint}", headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def fetch_paginated_data(endpoint, params=None):
    """Handles pagination if API supports it."""
    all_data = []
    page = 1
    while True:
        params = params or {}
        params["page"] = page
        data = fetch_data(endpoint, params)

        if data and "results" in data:
            all_data.extend(data["results"])
            if not data.get("next"):
                break
            page += 1
        else:
            break

    return all_data

if __name__ == "__main__":
    endpoint = "healthcare_records"  # Adjust endpoint
    data = fetch_paginated_data(endpoint)
    
    if data:
        with open("data/api_results.json", "w") as f:
            json.dump(data, f, indent=4)
        print("API data fetching complete. Saved as api_results.json")
