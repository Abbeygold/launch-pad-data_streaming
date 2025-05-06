import os
import requests
from typing import List, Dict, Optional

guardian_api_wrapper_URL = "https://content.guardianapis.com/search"


def fetch_articles(
    search_term: str, date_from: Optional[str] = None
) -> List[Dict[str, str]]:
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

    response = requests.get(guardian_api_wrapper_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    results = data.get("response", {}).get("results", [])

    articles = []
    for item in results:
        article_id = item.get("id")
        content = fetch_article_details(article_id, api_key, params)
        content_preview = content[:1000]

        articles.append(
            {
                "webPublicationDate": item.get("webPublicationDate"),
                "webTitle": item.get("webTitle"),
                "webUrl": item.get("webUrl"),
                "content_preview": content_preview,
            }
        )

    return articles


def fetch_article_details(
    article_id: str, api_key: str, params: Optional[Dict[str, str]] = None
) -> str:
    # Fetch full article details using the article's unique ID
    url = f"https://content.guardianapis.com/{article_id}"
    params["show-fields"] = "body"
    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch article details for {article_id}: {response.status_code}"
        )

    # Extract the article body if available
    article_data = response.json().get("response", {}).get("content", {})
    content = article_data.get("fields", {}).get("body", "")

    print(
        f"Fetched content for {article_id}: {content[:100]}..."
    )  # Print preview of content

    return content
