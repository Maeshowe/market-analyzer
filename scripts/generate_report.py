from datetime import datetime
from pathlib import Path
from api_clients import generate_gpt_response
from run_searches import perform_searches

# Prompt sablonok betöltése
def load_prompt(template_name):
    path = Path(__file__).parent.parent / "prompts" / template_name
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

# Webes keresési eredmények formázása
def format_search_results(search_results):
    formatted = ""
    for topic in search_results.values():
        formatted += f"\n## {topic['topic_name']}\n"
        for res in topic["results"][:3]:  # első 3 találat
            formatted += f"- {res['title']}: {res['snippet']} ([Forrás]({res['link']}))\n"
    return formatted

# Első lépés: Vázlat készítése
def generate_outline(formatted_results, date_str):
    outline_prompt_template = load_prompt("outline_prompt.txt")
    prompt = outline_prompt_template.format(
        date=date_str,
        search_results=formatted_results
    )
    outline = generate_gpt_response(prompt)
    return outline

# Második lépés: Részletes elemzés generálása
def generate_analysis(outline):
    analysis_prompt_template = load_prompt("analysis_prompt.txt")
    prompt = analysis_prompt_template.format(outline=outline)
    analysis = generate_gpt_response(prompt)
    return analysis

# Teljes folyamat végrehajtása
def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"🗓️ Jelentés készítése dátummal: {date_str}")

    search_results = perform_searches()
    formatted_results = format_search_results(search_results)

    print("📝 Vázlat generálása GPT-4.1 segítségével...")
    outline = generate_outline(formatted_results, date_str)
    print("✅ Vázlat elkészült.\n")

    print("📊 Részletes elemzés készítése GPT-4.1 segítségével...")
    analysis = generate_analysis(outline)
    print("✅ Részletes elemzés elkészült.\n")

    # Mentés markdown formátumban
    output_dir = Path(__file__).parent.parent / "docs" / "daily"
    output_dir.mkdir(parents=True, exist_ok=True)
    file_name = f"{date_str}-piaci-jelentes.md"
    output_file = output_dir / file_name

    output_file.write_text(analysis, encoding="utf-8")
    print(f"📄 Jelentés mentve ide: {output_file}")

if __name__ == "__main__":
    main()