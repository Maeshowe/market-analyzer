import csv
from datetime import datetime
import openai
from googleapiclient.discovery import build
import requests
from pathlib import Path
from config_loader import load_credentials, load_settings

# Konfiguráció betöltése
credentials = load_credentials()
settings = load_settings()

# OpenAI kliens létrehozása
client = openai.OpenAI(api_key=credentials["openai_api_key"])

# GPT token limit YAML konfigurációból
max_tokens = settings["general"]["token_limit"]

# Költség logolási funkció
def log_cost(usage, model="gpt-4.1"):
    # Modell alapú árak ($/1000 token)
    cost_per_1k_tokens_input = 0.01    # Példa ár: input tokenek
    cost_per_1k_tokens_output = 0.03   # Példa ár: output tokenek

    input_cost = (usage.prompt_tokens / 1000) * cost_per_1k_tokens_input
    output_cost = (usage.completion_tokens / 1000) * cost_per_1k_tokens_output
    total_cost = input_cost + output_cost

    log_entry = [
        datetime.now().isoformat(),
        model,
        usage.prompt_tokens,
        usage.completion_tokens,
        f"{total_cost:.6f}"
    ]

    log_file = Path(__file__).parent.parent / "data" / "cost_log.csv"
    log_file.parent.mkdir(parents=True, exist_ok=True)

    with open(log_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(log_entry)

# Google Custom Search konfiguráció (nyelvi támogatással)
def google_search(query, num_results=5, language="en"):
    service = build("customsearch", "v1", developerKey=credentials["google_search_api_key"])
    res = service.cse().list(
        q=query,
        cx=credentials["google_cse_id"],
        num=num_results,
        lr=f"lang_{language}"
    ).execute()
    items = res.get('items', [])
    results = [{
        'title': item['title'],
        'snippet': item['snippet'],
        'link': item['link']
    } for item in items]
    return results

# Brave Search konfiguráció (nyelvi támogatással)
def brave_search(query, num_results=5, language="en"):
    headers = {
        "X-Subscription-Token": credentials["brave_search_api_key"]
    }
    params = {
        "q": query,
        "count": num_results,
        "search_lang": language
    }
    response = requests.get("https://api.search.brave.com/res/v1/web/search", headers=headers, params=params)
    response.raise_for_status()
    results = response.json()
    items = results.get('web', {}).get('results', [])
    formatted_results = [{
        'title': item['title'],
        'snippet': item['description'],
        'link': item['url']
    } for item in items]
    return formatted_results

# GPT-4.1-es API hívás függvénye (költséglogolással)
def generate_gpt_response(prompt, model="gpt-4.1", temperature=0.7, max_tokens=max_tokens):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Te egy professzionális gazdasági elemző vagy."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )

    # Költség logolása minden GPT-hívás után
    log_cost(response.usage, model=model)

    return response.choices[0].message.content.strip()

# Tesztelés, ha közvetlenül futtatod ezt a scriptet
if __name__ == "__main__":
    search_language = settings["search"].get("search_language", "en")

    print("🔍 Google Search teszt:")
    google_results = google_search("S&P 500 stock market today", language=search_language)
    for item in google_results[:2]:
       print(f"{item['title']}\n{item['snippet']}\n{item['link']}\n")

    print("\n🔍 Brave Search teszt:")
    brave_results = brave_search("S&P 500 stock market today", language=search_language)
    for item in brave_results[:2]:
        print(f"{item['title']}\n{item['snippet']}\n{item['link']}\n")

    print("\n🤖 GPT-4.1 API teszt:")
    test_prompt = "Készíts egy rövid elemzést a mai amerikai részvénypiac helyzetéről."
    gpt_result = generate_gpt_response(test_prompt)
    print(gpt_result)