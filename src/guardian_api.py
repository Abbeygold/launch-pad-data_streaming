import os
import requests
from typing import List, Dict, Optional

GUARDIAN_API_URL = "https://content.guardianapis.com/search"

def fetch_articles(search_term: str, date_from: Optional[str] = None) -> List[Dict[str, str]]:
    api_key = os.getenv("GUARDIAN_API_KEY")
    if not api_key:
        raise EnvironmentError("GUARDIAN_API_KEY not found in environment variables")

    params = {
        "q": search_term,
        "api-key": api_key,
        "order-by": "newest",
        "page-size": 10,
    }

    if date_from:
        params["from-date"] = date_from

    response = requests.get(GUARDIAN_API_URL, params=params)
    response.raise_for_status()

    data = response.json()
    results = data.get("response", {}).get("results", [])

    articles = []
    for item in results:
        articles.append({
            "webPublicationDate": item.get("webPublicationDate"),
            "webTitle": item.get("webTitle"),
            "webUrl": item.get("webUrl"),
        })

    return articles
