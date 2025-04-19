import requests
from config_loader import FINANCIAL_DATASETS_API_KEY

def fetch_alternative_sentiment(symbol):
    url = f"https://api.financialdatasets.ai/api/v1/sentiment/{symbol}"
    headers = {'Authorization': f'Bearer {FINANCIAL_DATASETS_API_KEY}'}
    response = requests.get(url, headers=headers)
    return response.json() if response.ok else None

if __name__ == "__main__":
    result = fetch_alternative_sentiment("AAPL")
    print(result)