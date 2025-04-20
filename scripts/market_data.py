import requests
from config_loader import load_credentials

credentials = load_credentials()

FMP_API_KEY = credentials['fmp_api_key']
ALPHA_VANTAGE_API_KEY = credentials['alpha_vantage_api_key']

def get_stock_price(ticker, api="fmp"):
    if api == "fmp":
        url = f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={FMP_API_KEY}"
        response = requests.get(url)
        data = response.json()
        if data:
            return data[0]['price']
        else:
            return None
    elif api == "alpha":
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={ALPHA_VANTAGE_API_KEY}"
        response = requests.get(url)
        data = response.json()
        try:
            return float(data['Global Quote']['05. price'])
        except (KeyError, ValueError):
            return None

def get_forex_rate(pair="EURUSD", api="fmp"):
    if api == "fmp":
        url = f"https://financialmodelingprep.com/api/v3/fx/{pair}?apikey={FMP_API_KEY}"
        response = requests.get(url)
        data = response.json()
        if data:
            return data[0]['bid']
        else:
            return None
    elif api == "alpha":
        url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={pair[:3]}&to_currency={pair[3:]}&apikey={ALPHA_VANTAGE_API_KEY}"
        response = requests.get(url)
        data = response.json()
        try:
            return float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
        except (KeyError, ValueError):
            return None

def get_commodity_price(symbol="XAUUSD", api="fmp"):
    if api == "fmp":
        url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={FMP_API_KEY}"
        response = requests.get(url)
        data = response.json()
        if data:
            return data[0]['price']
        else:
            return None
    elif api == "alpha":
        return None

if __name__ == "__main__":
    print("AAPL árfolyam:", get_stock_price("AAPL"))
    print("EUR/USD árfolyam:", get_forex_rate("EURUSD"))
    print("Arany árfolyam (XAUUSD):", get_commodity_price("XAUUSD"))