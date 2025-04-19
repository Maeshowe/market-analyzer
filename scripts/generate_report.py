from datetime import datetime
from pathlib import Path
import re

from api_clients import generate_gpt_response
from config_loader import load_credentials
from market_data_fetcher import fetch_market_data
from macro_data_fetcher import fetch_macro_data
from earnings_data_fetcher import fetch_earnings
from news_fetcher import fetch_news
from alternative_data_fetcher import fetch_alternative_sentiment
from web_search import perform_web_search

# Prompt betöltése
def load_prompt(template_name):
    path = Path(__file__).parent.parent / "prompts" / template_name
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

# Webes keresési eredmények formázása
def format_search_results(search_results, max_per_topic=3):
    formatted = ""
    for topic in search_results.values():
        formatted += f"\n## {topic['topic_name']}\n"
        for res in topic["results"][:max_per_topic]:
            formatted += f"- [{res['title']}]({res['link']}): {res['snippet']}\n"
    return formatted

# Piaci és makroadatok előkészítése prompthoz
def prepare_prompt_data():
    market_symbols = ["^GSPC", "^DJI", "^IXIC", "EURUSD=X", "USDJPY=X", "GC=F", "CL=F", "HG=F"]
    market_data = {sym: fetch_market_data(sym) for sym in market_symbols}

    macro_data = fetch_macro_data()
    earnings_symbols = ["AAPL", "TSLA", "NVDA", "JPM"]
    earnings_data = {sym: fetch_earnings(sym) for sym in earnings_symbols}
    sentiment_data = {sym: fetch_alternative_sentiment(sym) for sym in earnings_symbols}
    news_data = fetch_news("stock market")

    return market_data, macro_data, earnings_data, sentiment_data, news_data

# GPT-4.1 jelentés generálása
def generate_market_report(date_str, formatted_results, market_data, macro_data, earnings_data, sentiment_data, news_data, additional_data=""):
    prompt_template = load_prompt("analysis_prompt.txt")

    prompt_filled = prompt_template.format(
        date=date_str,
        market_data=market_data,
        macro_data=macro_data,
        earnings_data=earnings_data,
        sentiment_data=sentiment_data,
        news_data=news_data,
        search_results=formatted_results,
        additional_data=additional_data
    )

    report = generate_gpt_response(prompt_filled)
    return report

# Jelentés mentése fájlba
def save_report(report, date_str):
    output_dir = Path(__file__).parent.parent / "docs" / "daily" / datetime.now().strftime("%Y/%m")
    output_dir.mkdir(parents=True, exist_ok=True)

    file_name = f"{date_str}-piaci-jelentes.md"
    output_file = output_dir / file_name
    output_file.write_text(report, encoding="utf-8")
    print(f"📄 Jelentés mentve: {output_file}")

    latest_path = Path(__file__).parent.parent / "docs" / "daily" / "latest.md"
    latest_path.write_text(report, encoding="utf-8")
    print(f"🔄 Legfrissebb jelentés frissítve: {latest_path}")

# Hiányzó adatok felismerése GPT-vel
def find_missing_data(gpt_report):
    pattern = re.compile(r"\[(.*?)\]")
    return pattern.findall(gpt_report)

# Hiányzó adatok automatikus lekérése
def fetch_missing_data(data_requests):
    translations = {
        "EUR/GBP árfolyam": "EURGBP=X",
        "EUR/USD árfolyam": "EURUSD=X",
        "palládium ára": "PA=F",
        "brent olaj ára": "BZ=F",
        "USA GDP": "GDP",
        "USA infláció": "CPI",
        "munkanélküliségi ráta": "UNEMPLOYMENT"
    }

    data_responses = {}
    macro_data = fetch_macro_data()

    for request in data_requests:
        symbol = translations.get(request, None)

        if symbol is None:
            data_responses[request] = "Adat nem található"
            continue

        if symbol in ["GDP", "CPI", "UNEMPLOYMENT"]:
            data_responses[request] = macro_data.get(symbol, "Nincs adat")
        else:
            data_responses[request] = fetch_market_data(symbol)
    return data_responses

# Iteratív jelentésgenerálás hiányzó adatokkal
def generate_refined_report(date_str, draft_report, formatted_results, market_data, macro_data, earnings_data, sentiment_data, news_data):
    missing_data_requests = find_missing_data(draft_report)
    
    if missing_data_requests:
        print(f"🔍 Hiányzó adatok: {missing_data_requests}")
        additional_data = fetch_missing_data(missing_data_requests)
        print(f"📊 Lekért további adatok: {additional_data}")

        refined_report = generate_market_report(
            date_str, formatted_results, market_data, macro_data,
            earnings_data, sentiment_data, news_data, additional_data=additional_data
        )
        return refined_report
    else:
        return draft_report

# Teljes folyamat végrehajtása
def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"🗓️ Jelentés készítése dátummal: {date_str}")

    print("\n🔎 Webes keresések végrehajtása...")
    queries = ["US stock market today", "economic policy", "bond yields", "options market", "Asia market", "commodity prices"]
    search_results = {query: {"topic_name": query, "results": perform_web_search(query)} for query in queries}
    formatted_results = format_search_results(search_results)

    print("\n📊 Friss pénzügyi adatok lekérdezése API-kkal...")
    market_data, macro_data, earnings_data, sentiment_data, news_data = prepare_prompt_data()

    print("\n🤖 Első draft jelentés generálása...")
    draft_report = generate_market_report(date_str, formatted_results, market_data, macro_data, earnings_data, sentiment_data, news_data)

    print("\n🧐 Hiányzó adatok ellenőrzése...")
    final_report = generate_refined_report(date_str, draft_report, formatted_results, market_data, macro_data, earnings_data, sentiment_data, news_data)

    print("\n💾 Jelentés mentése...")
    save_report(final_report, date_str)

    print("\n✅ Jelentésgenerálás sikeresen befejeződött.")

if __name__ == "__main__":
    main()