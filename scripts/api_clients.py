import openai
from googleapiclient.discovery import build
import requests
from config_loader import load_credentials

# Credential betöltés
credentials = load_credentials()

# OpenAI kliens létrehozása (új API formátumhoz)
client = openai.OpenAI(api_key=credentials["openai_api_key"])

# Google Custom Search konfiguráció
def google_search(query, num_results=5):
    service = build("customsearch", "v1", developerKey=credentials["google_search_api_key"])
    res = service.cse().list(
        q=query,
        cx=credentials["google_cse_id"],
        num=num_results,
        lr="lang_en"
    ).execute()
    return res.get('items', [])

# Brave Search konfiguráció
def brave_search(query, num_results=5):
    headers = {
        "X-Subscription-Token": credentials["brave_search_api_key"]
    }
    params = {
        "q": query,
        "count": num_results
    }
    response = requests.get("https://api.search.brave.com/res/v1/web/search", headers=headers, params=params)
    response.raise_for_status()
    results = response.json()
    return results.get('web', {}).get('results', [])

# GPT-4.1-es API hívás függvénye (javított)
def generate_gpt_response(prompt, model="gpt-4.1", temperature=0.7, max_tokens=3000):
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
    print("🔍 Google Search teszt:")
    google_results = google_search("S&P 500 stock market today")
    for item in google_results[:2]:
        print(f"{item['title']}\n{item['snippet']}\n{item['link']}\n")

    print("\n🔍 Brave Search teszt:")
    brave_results = brave_search("S&P 500 stock market today")
    for item in brave_results[:2]:
        print(f"{item['title']}\n{item['description']}\n{item['url']}\n")

    print("\n🤖 GPT-4.1 API teszt:")
    test_prompt = "Készíts egy rövid elemzést a mai amerikai részvénypiac helyzetéről."
    gpt_result = generate_gpt_response(test_prompt)
    print(gpt_result)