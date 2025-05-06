import os
import requests
from typing import List, Dict, Optional
from src.constants import (
    GUARDIAN_API_SEARCH_ENDPOINT,
    GUARDIAN_API_BASE_URL,
    ERROR_NO_API_KEY,
    DEFAULT_PAGE_SIZE,
    DEFAULT_ORDER_BY,
    CONTENT_PREVIEW_LENGTH,
)


def fetch_articles(
    search_term: str, date_from: Optional[str] = None
) -> List[Dict[str, str]]:
    """
    Fetch a list of articles from The Guardian API based on
    a search term and optional date.

    Args:
        search_term (str): Term to search for in article titles and content.
        date_from (Optional[str]): Optional ISO date string (YYYY-MM-DD) to filter from.

    Returns:
        List[Dict[str, str]]: List of article metadata including
        title, date, URL, and a preview.
    """
    api_key = os.getenv("GUARDIAN_API_KEY")
    if not api_key:
        raise EnvironmentError(ERROR_NO_API_KEY)

    params = {
        "q": search_term,
        "api-key": api_key,
        "order-by": DEFAULT_ORDER_BY,
        "page-size": DEFAULT_PAGE_SIZE,
    }

    if date_from:
        params["from-date"] = date_from

    response = requests.get(GUARDIAN_API_SEARCH_ENDPOINT, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    results = data.get("response", {}).get("results", [])

    articles = []
    for item in results:
        article_id = item.get("id")
        content = fetch_article_details(article_id, api_key, params)
        content_preview = content[:CONTENT_PREVIEW_LENGTH]

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
    """
    Fetch the full HTML body content for a given article using its unique ID.

    Args:
        article_id (str): Unique identifier for the article.
        api_key (str): Guardian API key.
        params (Optional[Dict[str, str]]): Existing query params to extend.

    Returns:
        str: The full body of the article in HTML.
    """
    url = f"{GUARDIAN_API_BASE_URL}/{article_id}"
    if params is None:
        params = {}
    params["show-fields"] = "body"

    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch article details for {article_id}: {response.status_code}"
        )

    article_data = response.json().get("response", {}).get("content", {})
    content = article_data.get("fields", {}).get("body", "")

    print(f"Fetched content for {article_id}: {content[:100]}...")
    return content
