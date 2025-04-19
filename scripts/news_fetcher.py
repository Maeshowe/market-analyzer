import requests
from config_loader import NEWSAPI_KEY

def fetch_news(query, language="en"):
    url = f"https://newsapi.org/v2/everything?q={query}&language={language}&apiKey={NEWSAPI_KEY}"
    response = requests.get(url)
    return response.json().get("articles", []) if response.ok else []

if __name__ == "__main__":
    news = fetch_news("stock market")
    print(news)