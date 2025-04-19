import requests
from config_loader import FMP_API_KEY

def fetch_macro_data():
    macro_indicators = ["GDP", "CPI", "UNEMPLOYMENT"]
    base_url = "https://financialmodelingprep.com/api/v4/economic"
    headers = {"Accept": "application/json"}
    results = {}

    for indicator in macro_indicators:
        url = f"{base_url}?name={indicator}&apikey={FMP_API_KEY}"
        response = requests.get(url, headers=headers)
        if response.ok:
            results[indicator] = response.json()
        else:
            results[indicator] = "Nincs adat"
    return results

if __name__ == "__main__":
    data = fetch_macro_data()
    print(data)