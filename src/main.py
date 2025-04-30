import argparse
import logging
from src.guardian_api import fetch_articles
from src.sqs_publisher import publish_messages

logging.basicConfig(level=logging.INFO)


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description="Search Guardian articles and publish to an AWS SQS queue."
    )
    parser.add_argument("search_term", type=str, help="Search term for articles")
    parser.add_argument(
        "--date_from",
        type=str,
        required=False,
        help="Start date for articles in YYYY-MM-DD format",
    )
    return parser.parse_args(args)


def run(search_term: str, date_from: str = None):
    articles = fetch_articles(search_term, date_from)
    results = []

    for article in articles:
        try:
            response = publish_messages(article)
            results.append({
                "title": article["webTitle"],
                "message_id": response.get("MessageId") if response else None,
                "error": None if response else "SQS Error",
            })
        except Exception as e:
            results.append({
                "title": article["webTitle"],
                "message_id": None,
                "error": str(e),
            })
    return results


def main(args=None):
    args = parse_args(args)
    results = run(args.search_term, args.date_from)

    for result in results:
        title = result["title"]
        if result["message_id"]:
            print(f"✅ Published: {title} (Message ID: {result['message_id']})")
        else:
            print(f"❌ Failed to publish: {title} — {result['error']}")

    print(f"\n🎉 Done! Published {len(results)} articles to SQS.")


if __name__ == "__main__":
    main()
