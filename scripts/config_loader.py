import yaml
from pathlib import Path

def load_credentials():
    cred_path = Path(__file__).parent.parent / "config" / "credentials.yaml"
    with open(cred_path, "r") as file:
        return yaml.safe_load(file)

def load_settings():
    settings_path = Path(__file__).parent.parent / "config" / "settings.yaml"
    with open(settings_path, "r") as file:
        return yaml.safe_load(file)

# API kulcsok betöltése változókba
credentials = load_credentials()

OPENAI_API_KEY = credentials.get("openai_api_key")
GOOGLE_SEARCH_API_KEY = credentials.get("google_search_api_key")
GOOGLE_CSE_ID = credentials.get("google_cse_id")
BRAVE_SEARCH_API_KEY = credentials.get("brave_search_api_key")
ALPHA_VANTAGE_API_KEY = credentials.get("alpha_vantage_api_key")
FINANCIAL_DATASETS_API_KEY = credentials.get("financial_datasets_api_key")
FMP_API_KEY = credentials.get("fmp_api_key")
NEWSAPI_KEY = credentials.get("newsapi_key")

# gyors teszt
if __name__ == "__main__":
    print("✅ API-kulcsok betöltve:")
    for key, value in credentials.items():
        print(f"{key}: {'rendben' if value else 'hiányzik'}")