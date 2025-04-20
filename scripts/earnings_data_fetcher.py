import requests
from config_loader import FINANCIAL_DATASETS_API_KEY

def fetch_earnings(ticker):
    url = "https://api.financialdatasets.ai/earnings/press-releases"
    querystring = {"ticker": ticker}
    headers = {"X-API-KEY": FINANCIAL_DATASETS_API_KEY}

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"API-hiba: {e}")
        return None