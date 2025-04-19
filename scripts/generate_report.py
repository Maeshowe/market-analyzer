from datetime import datetime
from pathlib import Path
from api_clients import generate_gpt_response
from run_searches import perform_gpt_generated_searches
from config_loader import load_settings
from data_fetcher import fetch_daily_market_data

# YAML konfiguráció betöltése
settings = load_settings()
max_tokens = settings["general"]["token_limit"]

# Prompt fájlok betöltése
def load_prompt(template_name):
    path = Path(__file__).parent.parent / "prompts" / template_name
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

# Piaci adatok formázása GPT promptba
def format_market_data_prompt(market_data, date_str):
    return f"""
## 📅 Friss piaci adatok ({date_str}):

- VIX index: {market_data['VIX']} pont
- DXY: {market_data['DXY']}
- EUR/USD: {market_data['EURUSD']}
- USD/JPY: {market_data['USDJPY']}
- Brent olaj: {market_data['Brent']} USD/hordó
- WTI olaj: {market_data['WTI']} USD/hordó
- Arany ára: {market_data['Gold']} USD/uncia
- Réz ára: {market_data['Copper']} USD/tonna
"""

# Keresési eredmények formázása
def format_search_results(search_results, max_per_topic=2):
    formatted = ""
    for topic in search_results.values():
        formatted += f"\n## {topic['topic_name']}\n"
        for res in topic["results"][:max_per_topic]:
            formatted += f"- {res['title']}: {res['snippet']} ([Forrás]({res['link']}))\n"
    return formatted

# Jelentés vázlat generálása GPT segítségével
def generate_outline(formatted_results, date_str):
    outline_prompt_template = load_prompt("outline_prompt.txt")
    prompt = outline_prompt_template.format(date=date_str, search_results=formatted_results)
    return generate_gpt_response(prompt, max_tokens=max_tokens)

# Részletes draft elemzés generálása GPT segítségével
def generate_analysis(outline, market_data_prompt, formatted_results, date_str):
    analysis_prompt_template = load_prompt("analysis_prompt.txt")
    prompt = analysis_prompt_template.format(
        date=date_str,
        outline=outline,
        market_data=market_data_prompt,
        search_results=formatted_results
    )
    return generate_gpt_response(prompt, max_tokens=max_tokens)

# Jelentés iteratív finomítása GPT-vel
def refine_analysis(draft):
    refinement_prompt_template = load_prompt("refinement_prompt.txt")
    prompt = refinement_prompt_template.format(draft=draft)
    return generate_gpt_response(prompt, max_tokens=max_tokens)

# Jelentés mentése havi/éves bontásban és latest.md frissítése
def save_report(content, date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    
    # Éves/havi mappa létrehozása
    year_month_path = Path(__file__).parent.parent / "docs" / "daily" / f"{date_obj.year}/{date_obj.month:02d}"
    year_month_path.mkdir(parents=True, exist_ok=True)

    # Jelentés mentése dátum szerint
    file_name = f"{date_str}-piaci-jelentes.md"
    output_file = year_month_path / file_name
    output_file.write_text(content, encoding="utf-8")
    print(f"📄 Jelentés mentve: {output_file}")

    # latest.md frissítése
    latest_path = Path(__file__).parent.parent / "docs" / "daily" / "latest.md"
    latest_path.write_text(content, encoding="utf-8")
    print(f"🔄 latest.md frissítve: {latest_path}")

# Fő függvény, amely az egész workflow-t vezérli
def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"🗓️ Jelentés készítése dátummal: {date_str}")

    # Webes keresési eredmények lekérése
    search_results = perform_gpt_generated_searches()
    formatted_results = format_search_results(search_results)

    # Piaci adatok begyűjtése
    market_data = fetch_daily_market_data()
    market_data_prompt = format_market_data_prompt(market_data, date_str)

    # GPT-vel vázlat generálása
    print("📝 Vázlat generálása...")
    outline = generate_outline(formatted_results, date_str)
    print("✅ Vázlat elkészült.")

    # GPT-vel draft elemzés generálása, immár valódi adatokkal
    print("📊 Draft elemzés generálása valódi adatokkal...")
    draft_analysis = generate_analysis(outline, market_data_prompt, formatted_results, date_str)
    print("✅ Draft elemzés elkészült.")

    # GPT iteratív finomítás
    print("🔄 Elemzés finomítása iteratív prompt tuninggal...")
    refined_analysis = refine_analysis(draft_analysis)
    print("✅ Elemzés finomítása elkészült.")

    # Jelentés mentése havi/éves struktúrában és latest.md frissítése
    save_report(refined_analysis, date_str)

if __name__ == "__main__":
    main()