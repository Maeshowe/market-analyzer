from api_clients import google_search, brave_search

def perform_web_search(query, num_results=5):
    results = google_search(query, num_results)
    if not results:
        results = brave_search(query, num_results)
    return results

if __name__ == "__main__":
    search_results = perform_web_search("NASDAQ performance today")
    print(search_results)