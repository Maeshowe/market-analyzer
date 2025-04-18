import openai
from googleapiclient.discovery import build
import requests
from config_loader import load_credentials, load_settings

# Credential és beállítások betöltése
credentials = load_credentials()
settings = load_settings()

# OpenAI kliens létrehozása (új API formátumhoz)
client = openai.OpenAI(api_key=credentials["openai_api_key"])

# Google Custom Search konfiguráció nyelvi támogatással
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

# Brave Search konfiguráció nyelvi támogatással
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

# GPT-4.1-es API hívás függvénye (változatlan)
def generate_gpt_response(prompt, model="gpt-4.1", temperature=0.7, max_tokens=7500):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Te egy professzionális gazdasági elemző vagy."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()

# Tesztelés, ha közvetlen futtatod ezt a scriptet
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