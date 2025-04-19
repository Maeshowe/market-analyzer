import requests
from config_loader import FINANCIAL_DATASETS_API_KEY

def fetch_earnings(symbol):
    url = f"https://api.financialdatasets.ai/api/v1/earnings/{symbol}"
    headers = {'Authorization': f'Bearer {FINANCIAL_DATASETS_API_KEY}'}
    response = requests.get(url, headers=headers)
    return response.json() if response.ok else None

if __name__ == "__main__":
    data = fetch_earnings("AAPL")
    print(data)