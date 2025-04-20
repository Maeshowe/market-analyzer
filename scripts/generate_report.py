# generate_report.py (strukturált javaslat)

import datetime
from market_data import fetch_all_market_data
from earnings_data_fetcher import fetch_earnings
from news_fetcher import fetch_news
from web_search import perform_gpt_generated_searches
from api_clients import generate_gpt_response
from config_loader import load_settings

settings = load_settings()

def generate_daily_report(date_str):
    print(f"🗓️ Generating market report for {date_str}")

    # 1. Fetch all market and macro data
    market_data = fetch_all_market_data()
    print("✅ Market data fetched")

    earnings_data = fetch_earnings(["AAPL", "TSLA", "NVDA", "MSFT", "GOOG"])
    print("✅ Earnings data fetched")

    news_data = fetch_news(["stock market", "Federal Reserve", "US economy"])
    print("✅ News data fetched")

    web_search_data = perform_gpt_generated_searches(date_str)
    print("✅ Web search data fetched")

    # 2. Load prompt templates
    with open("prompts/outline_prompt_en.txt") as file:
        outline_prompt = file.read()

    with open("prompts/analysis_prompt_en.txt") as file:
        analysis_prompt = file.read()

    # 3. Generate outline
    outline_input = f"{outline_prompt}\n\nMarket data:\n{market_data}\n\nEarnings:\n{earnings_data}\n\nNews:\n{news_data}\n\nWeb Search Results:\n{web_search_data}"
    outline = generate_gpt_response(outline_input, model="gpt-4.1")
    print("📝 Outline generated")

    # 4. Generate initial analysis draft
    analysis_input = f"{analysis_prompt}\n\nOutline:\n{outline}"
    draft_analysis = generate_gpt_response(analysis_input, model="gpt-4.1")
    print("📊 Draft analysis generated")

    # 5. Identify missing data (iterative step)
    missing_data_prompt = f"Check the following analysis and list any missing or unspecified numeric data points explicitly mentioned:\n\n{draft_analysis}"
    missing_data_response = generate_gpt_response(missing_data_prompt, model="gpt-4.1")

    # Fetch additional missing data (iteratively)
    if missing_data_response.strip().lower() != "none":
        print("🔍 Missing data identified:", missing_data_response)
        additional_data = perform_gpt_generated_searches(missing_data_response)
        print("🔄 Additional data fetched")
        
        # Regenerate final analysis
        final_analysis_prompt = f"{draft_analysis}\n\nAdditional data to include:\n{additional_data}"
        final_analysis = generate_gpt_response(final_analysis_prompt, model="gpt-4.1")
    else:
        final_analysis = draft_analysis
        print("✅ No missing data")

    # 6. Save English report
    english_report_path = f"docs/daily/{date_str}-market-report-en.md"
    with open(english_report_path, "w") as file:
        file.write(final_analysis)
    print(f"📄 English report saved: {english_report_path}")

    # 7. Translate and save Hungarian report
    translation_prompt = f"Translate the following text to Hungarian:\n\n{final_analysis}"
    hungarian_report = generate_gpt_response(translation_prompt, model="gpt-4.1")
    hungarian_report_path = f"docs/daily/{date_str}-market-report-hu.md"
    with open(hungarian_report_path, "w") as file:
        file.write(hungarian_report)
    print(f"📄 Hungarian report saved: {hungarian_report_path}")

def main():
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    generate_daily_report(date_str)

if __name__ == "__main__":
    main()