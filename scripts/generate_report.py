from datetime import datetime
from pathlib import Path
from api_clients import generate_gpt_response
from run_searches import perform_gpt_generated_searches

def load_prompt(template_name):
    path = Path(__file__).parent.parent / "prompts" / template_name
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def format_search_results(search_results, max_per_topic=2):
    formatted = ""
    for topic in search_results.values():
        formatted += f"\n## {topic['topic_name']}\n"
        for res in topic["results"][:max_per_topic]:
            formatted += f"- {res['title']}: {res['snippet']} ([Forrás]({res['link']}))\n"
    return formatted

def generate_outline(formatted_results, date_str):
    outline_prompt_template = load_prompt("outline_prompt.txt")
    prompt = outline_prompt_template.format(date=date_str, search_results=formatted_results)
    return generate_gpt_response(prompt)

def generate_analysis(outline, date_str):
    analysis_prompt_template = load_prompt("analysis_prompt.txt")
    prompt = analysis_prompt_template.format(date=date_str, outline=outline)
    return generate_gpt_response(prompt)

def refine_analysis(draft):
    refinement_prompt_template = load_prompt("refinement_prompt.txt")
    prompt = refinement_prompt_template.format(draft=draft)
    return generate_gpt_response(prompt)

def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"🗓️ Jelentés készítése dátummal: {date_str}")

    # Webes keresési eredmények lekérése
    search_results = perform_gpt_generated_searches()
    formatted_results = format_search_results(search_results)

    # Első GPT hívás: vázlat
    print("📝 Vázlat generálása...")
    outline = generate_outline(formatted_results, date_str)
    print("✅ Vázlat elkészült.")

    # Második GPT hívás: részletes elemzés (draft)
    print("📊 Draft elemzés generálása...")
    draft_analysis = generate_analysis(outline, date_str)
    print("✅ Draft elemzés elkészült.")

    # Harmadik GPT hívás: iteratív finomítás
    print("🔄 Elemzés finomítása iteratív prompt tuninggal...")
    refined_analysis = refine_analysis(draft_analysis)
    print("✅ Elemzés finomítása elkészült.")

    # Mentés markdown formátumban
    output_dir = Path(__file__).parent.parent / "docs" / "daily"
    output_dir.mkdir(parents=True, exist_ok=True)
    file_name = f"{date_str}-piaci-jelentes.md"
    output_file = output_dir / file_name

    output_file.write_text(refined_analysis, encoding="utf-8")
    print(f"📄 Finomított jelentés mentve: {output_file}")

    # latest.md frissítése
    latest_path = output_dir / "latest.md"
    latest_path.write_text(refined_analysis, encoding="utf-8")
    print(f"🔄 latest.md frissítve: {latest_path}")

if __name__ == "__main__":
    main()