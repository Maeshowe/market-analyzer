import requests
from config_loader import FMP_API_KEY, FINANCIAL_DATASETS_API_KEY, ALPHA_VANTAGE_API_KEY

# Financial Modeling Prep API lekérdezés
def fetch_fmp_market_data(symbol):
    url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={FMP_API_KEY}"
    response = requests.get(url)
    if response.ok:
        data = response.json()
        return data[0] if data else None
    return None

# FinancialDatasets.ai lekérdezés
def fetch_financialdatasets_data(symbol):
    url = f"https://api.financialdatasets.ai/api/v1/market-data/equities/{symbol}"
    headers = {'Authorization': f'Bearer {FINANCIAL_DATASETS_API_KEY}'}
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.json()
    return None

# Alpha Vantage API lekérdezés (backup)
def fetch_alpha_vantage_data(symbol):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    if response.ok:
        data = response.json().get("Global Quote", {})
        return data if data else None
    return None

# Egységesített függvény
def fetch_market_data(symbol):
    data = fetch_financialdatasets_data(symbol)
    if data:
        print(f"{symbol}: FinancialDatasets.ai ✅")
        return data

    data = fetch_fmp_market_data(symbol)
    if data:
        print(f"{symbol}: FMP ✅")
        return data

    data = fetch_alpha_vantage_data(symbol)
    if data:
        print(f"{symbol}: Alpha Vantage ✅")
        return data

    print(f"{symbol}: ⚠️ Nincs adat!")
    return None

# Tesztelés
if __name__ == "__main__":
    symbols = ["^GSPC", "AAPL", "GOOGL", "EURUSD=X", "GC=F", "CL=F"]
    for symbol in symbols:
        result = fetch_market_data(symbol)
        print(result, "\n")