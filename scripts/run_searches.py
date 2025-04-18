import yaml
from pathlib import Path
from api_clients import google_search, brave_search
from config_loader import load_settings
from query_builder import build_query

# Beállítások betöltése
settings = load_settings()

def perform_searches():
    topics = settings["topics"]
    max_results = settings["search"]["max_results_per_topic"]
    primary_provider = settings["search"]["primary_provider"]

    search_results = {}

    for topic in topics:
        query = build_query(topic["id"])
        topic_name = topic["name"]
        print(f"\n🔍 Keresés: {topic_name} – '{query}'")

        try:
            # Elsődleges kereső: Google
            if primary_provider == "google":
                results = google_search(query, max_results)
                if not results:
                    raise ValueError("Google nem adott találatot.")
            # Másik keresőre váltás, ha nincs találat
            if not results:
                print("Google találatok nem érhetők el vagy üresek, váltás Brave-re.")
                results = brave_search(query, max_results)
        except Exception as e:
            print(f"Hiba történt a keresés során: {e}")
            print("Váltás Brave keresőre.")
            results = brave_search(query, max_results)

        formatted_results = []
        for res in results:
            formatted_results.append({
                "title": res.get("title", "N/A"),
                "snippet": res.get("snippet") or res.get("description", "N/A"),
                "link": res.get("link") or res.get("url", "N/A")
            })

        search_results[topic["id"]] = {
            "topic_name": topic_name,
            "results": formatted_results
        }

        print(f"✅ Találatok: {len(formatted_results)} db")

    return search_results

# Fő futtató blokk teszteléshez
if __name__ == "__main__":
    results = perform_searches()

    # Eredmények megjelenítése
    for topic_id, content in results.items():
        print(f"\n📌 {content['topic_name']} – Összes találat: {len(content['results'])}")
        for res in content['results'][:3]:  # első 3 találat röviden
            print(f" • {res['title']}\n   {res['snippet']}\n   🔗 {res['link']}\n")