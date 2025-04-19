import yaml
from pathlib import Path

def load_credentials():
    cred_path = Path(__file__).parent.parent / "config" / "credentials.yaml"
    with open(cred_path, "r") as file:
        credentials = yaml.safe_load(file)
    return credentials

credentials = load_credentials()

OPENAI_API_KEY = credentials["openai_api_key"]
GOOGLE_CSE_ID = credentials["google_cse_id"]
BRAVE_SEARCH_API_KEY = credentials["brave_search_api_key"]
ALPHA_VANTAGE_API_KEY = credentials["alpha_vantage_api_key"]
FINANCIAL_DATASETS_API_KEY = credentials["financial_datasets_api_key"]
FMP_API_KEY = credentials["fmp_api_key"]
NEWSAPI_KEY = credentials["newsapi_key"]

if __name__ == "__main__":
    # Gyors ellenőrzés
    for key, value in credentials.items():
        status = "✅ OK" if value else "❌ Missing!"
        print(f"{key}: {status}")