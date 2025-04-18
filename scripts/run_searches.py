from datetime import datetime
from query_generator import generate_search_queries
from api_clients import google_search, brave_search
from config_loader import load_settings

settings = load_settings()

def perform_gpt_generated_searches():
    date_str = datetime.now().strftime("%Y-%m-%d")
    queries_by_topic = generate_search_queries(date_str)

    max_results_per_query = settings["search"]["max_results_per_topic"]
    primary_provider = settings["search"]["primary_provider"]
    fallback_provider = settings["search"]["fallback_provider"]
    search_language = settings["search"].get("search_language", "en")

    search_results = {}

    print(f"\n🔎 GPT által generált keresések futtatása dátummal: {date_str}\n")

    for topic, queries in queries_by_topic.items():
        print(f"📌 Téma: {topic}")
        search_results[topic] = {"topic_name": topic, "results": []}

        for query in queries:
            print(f" - Lekérdezés: '{query}'")

            results = []

            # Elsődleges kereső API
            if primary_provider == "google":
                try:
                    results = google_search(query, max_results_per_query, language=search_language)
                    if not results:
                        raise ValueError("Google API nem adott találatot.")
                except Exception as e:
                    print(f"   ⚠️ Google API hiba vagy limit: {e}, átváltás Brave API-ra.")
                    results = brave_search(query, max_results_per_query, language=search_language)

            elif primary_provider == "brave":
                try:
                    results = brave_search(query, max_results_per_query, language=search_language)
                    if not results:
                        raise ValueError("Brave API nem adott találatot.")
                except Exception as e:
                    print(f"   ⚠️ Brave API hiba vagy limit: {e}, átváltás Google API-ra.")
                    results = google_search(query, max_results_per_query, language=search_language)

            else:
                print(f"   ⚠️ Ismeretlen elsődleges keresőszolgáltató: '{primary_provider}'.")

            # Ha még mindig nincs eredmény, logoljuk
            if not results:
                print(f"   ❌ Nincs találat a '{query}' lekérdezésre egyik API-nál sem.")
            else:
                print(f"   ✅ {len(results)} találat érkezett.")

            search_results[topic]["results"].extend(results)

    print("\n🎯 Keresések befejezve.")
    return search_results

# Tesztfuttatás (önálló scriptként való futtatásra)
if __name__ == "__main__":
    final_results = perform_gpt_generated_searches()

    # Rövid összegzés kiíratása a terminálra ellenőrzéshez
    for topic, data in final_results.items():
        print(f"\n📚 Eredmények a '{topic}' témában ({len(data['results'])} találat):")
        for res in data['results']:
            print(f"- {res['title']} ({res['link']})")