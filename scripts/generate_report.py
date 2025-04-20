import os
from datetime import datetime
from api_clients import generate_gpt_response
from market_data_fetcher import fetch_market_data
from web_search import perform_gpt_generated_searches
from alternative_data_fetcher import fetch_alternative_sentiment
from macro_data_fetcher import fetch_macro_data
from earnings_data_fetcher import fetch_earnings_data
from news_fetcher import fetch_news
from translator import translate_to_hungarian
from config_loader import load_settings, load_prompts
from utils import identify_missing_data, fetch_additional_data, format_market_data_prompt

settings = load_settings()
prompts = load_prompts()

def generate_outline(search_results, market_data, sentiment_data, macro_data, earnings_data, news_data, date_str):
    prompt = prompts["outline_prompt"].format(
        date=date_str,
        search_results=search_results,
        market_data=market_data,
        sentiment_data=sentiment_data,
        macro_data=macro_data,
        earnings_data=earnings_data,
        news_data=news_data
    )
    return generate_gpt_response(prompt, max_tokens=settings["general"]["token_limit"])

def generate_analysis(outline, market_data_prompt, date_str):
    prompt = prompts["analysis_prompt"].format(outline=outline, market_data_prompt=market_data_prompt, date=date_str)
    return generate_gpt_response(prompt, max_tokens=settings["general"]["token_limit"])

def perform_iterative_tuning(draft_analysis, market_data_prompt, date_str, iterations=2):
    analysis = draft_analysis
    for i in range(iterations):
        refinement_prompt = prompts["refinement_prompt"].format(
            draft_analysis=analysis,
            market_data_prompt=market_data_prompt,
            date=date_str
        )
        analysis = generate_gpt_response(refinement_prompt, max_tokens=settings["general"]["token_limit"])
        print(f"🔄 Iteration {i+1} of refinement completed.")
    return analysis

def save_report(content, directory, filename):
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath

def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"🗓️ Generating market report for date: {date_str}")

    print("🔎 Performing GPT-generated searches...")
    search_results = perform_gpt_generated_searches()

    print("📊 Fetching market data...")
    market_data = fetch_market_data()

    print("📈 Fetching alternative sentiment data...")
    sentiment_data = fetch_alternative_sentiment()

    print("📉 Fetching macroeconomic data...")
    macro_data = fetch_macro_data()

    print("📑 Fetching earnings data...")
    earnings_data = fetch_earnings_data()

    print("📰 Fetching news data...")
    news_data = fetch_news()

    market_data_prompt = format_market_data_prompt(market_data, date_str)

    print("📝 Generating report outline...")
    outline = generate_outline(
        search_results, market_data, sentiment_data, macro_data, earnings_data, news_data, date_str)

    print("📊 Generating draft analysis...")
    draft_analysis = generate_analysis(outline, market_data_prompt, date_str)

    print("🔍 Checking for missing data...")
    missing_data = identify_missing_data(draft_analysis, market_data)
    if missing_data:
        print(f"🔄 Missing data found: {missing_data}")
        additional_data = fetch_additional_data(missing_data)
        market_data_prompt += "\n" + format_market_data_prompt(additional_data, date_str)
    else:
        print("✅ No missing data found.")

    print("🔄 Performing iterative tuning...")
    final_analysis_en = perform_iterative_tuning(draft_analysis, market_data_prompt, date_str)

    print("🌍 Translating analysis to Hungarian...")
    final_analysis_hu = translate_to_hungarian(final_analysis_en)

    output_dir_en = os.path.join(settings["output"]["output_dir"], "en")
    output_dir_hu = os.path.join(settings["output"]["output_dir"], "hu")

    filename_en = date_str + "-market-report-en.md"
    filename_hu = date_str + "-piaci-jelentes-hu.md"

    print("💾 Saving English report...")
    save_report(final_analysis_en, output_dir_en, filename_en)

    print("💾 Saving Hungarian report...")
    save_report(final_analysis_hu, output_dir_hu, filename_hu)

    save_report(final_analysis_en, output_dir_en, "latest.md")
    save_report(final_analysis_hu, output_dir_hu, "latest.md")

    print("✅ Market reports saved successfully.")

if __name__ == "__main__":
    main()