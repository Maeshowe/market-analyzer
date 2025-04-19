from datetime import datetime
from pathlib import Path
from api_clients import generate_gpt_response

def load_prompt(prompt_name):
    path = Path(__file__).parent.parent / "prompts" / prompt_name
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def generate_search_queries(date_str):
    prompt_template = load_prompt("search_keywords_prompt.txt")
    prompt = prompt_template.format(date=date_str)
    response = generate_gpt_response(prompt)

    queries_by_topic = {}
    current_topic = None  # Ez segít abban, hogy ne üres string legyen.

    for line in response.strip().split('\n'):
        line = line.strip()
        if not line:
            continue

        if line.endswith(':'):
            current_topic = line.replace(':', '').strip()
            queries_by_topic[current_topic] = []
        elif line.startswith('-') and current_topic:
            queries_by_topic[current_topic].append(line.strip('- ').strip())
        else:
            print(f"⚠️ Nem várt formátumú sor a GPT válaszában: '{line}'")

    return queries_by_topic

# Tesztelés
if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    queries = generate_search_queries(today)
    for topic, qlist in queries.items():
        print(f"\n🔎 {topic}:")
        for q in qlist:
            print(f" - {q}")