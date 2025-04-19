import yfinance as yf
import numpy as np

def fetch_daily_market_data():
    data = {}

    symbols = {
        'VIX': '^VIX',
        'DXY': 'DX-Y.NYB',
        'EURUSD': 'EURUSD=X',
        'USDJPY': 'JPY=X',
        'Brent': 'BZ=F',
        'WTI': 'CL=F',
        'Gold': 'GC=F',
        'Copper': 'HG=F'
    }

    for key, symbol in symbols.items():
        try:
            ticker_data = yf.Ticker(symbol).history(period="1d")
            latest_close = ticker_data['Close'].iloc[-1]

            # Réz ára átváltása font-ról tonnára
            if key == 'Copper':
                latest_close = latest_close * 2204.62

            # Konvertálás natív Python float típusra
            data[key] = round(float(np.float64(latest_close)), 2)

        except Exception as e:
            print(f"⚠️ Nem sikerült lekérni a {key} adatát ({symbol}): {e}")
            data[key] = 'N/A'

    return data

if __name__ == "__main__":
    print(fetch_daily_market_data())