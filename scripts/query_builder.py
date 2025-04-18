from datetime import datetime
from config_loader import load_settings

settings = load_settings()

def build_query(topic_id):
    # Témák betöltése
    topics = settings["topics"]

    # Dátum formázása
    today_str = datetime.now().strftime("%Y-%m-%d")

    # Lekérdezés sablon megkeresése
    topic_query_template = next((t["query"] for t in topics if t["id"] == topic_id), None)

    if topic_query_template is None:
        raise ValueError(f"Nincs lekérdezési sablon ehhez a témához: {topic_id}")

    # Végső lekérdezés generálása (dátummal kiegészítve)
    final_query = f"{topic_query_template} {today_str}"

    return final_query

# Teszteljük a lekérdezések generálását közvetlen futtatáskor
if __name__ == "__main__":
    test_topic_ids = ["us_stocks", "fed_bonds", "commodities"]

    for topic_id in test_topic_ids:
        query = build_query(topic_id)
        print(f"🔎 Generált lekérdezés ({topic_id}): {query}")