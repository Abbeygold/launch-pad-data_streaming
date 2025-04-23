# guardian_api.py

def fetch_articles(search_term, date_from=None):
    print(f"[Stub] Fetching articles for '{search_term}' from date: {date_from}")
    # Return dummy data
    return [
        {
            "webPublicationDate": "2023-11-21T11:11:31Z",
            "webTitle": f"Stubbed Article for {search_term}",
            "webUrl": "https://www.theguardian.com/stubbed-article",
            "content_preview": "This is a stub preview of the article content."
        }
    ]

# TODO: update the above code to implement actual function to use guardian api  