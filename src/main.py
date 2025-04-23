# main.py
import argparse
from guardian_api import fetch_articles
from sqs_publisher import publish_articles

def parse_args():
    parser = argparse.ArgumentParser(
        description="Search Guardian articles and publish to an AWS SQS queue."
    )
    parser.add_argument("search_term", help="Search term for Guardian API")
    parser.add_argument("--date_from", help="Filter articles from this date (YYYY-MM-DD)", default=None)
    parser.add_argument("--queue_url", required=True, help="SQS Queue URL to publish results to")

    return parser.parse_args()

def main():
    args = parse_args()

    articles = fetch_articles(
        search_term=args.search_term,
        date_from=args.date_from
    )

    if not articles:
        print("No articles found.")
        return

    publish_articles(articles, queue_url=args.queue_url)
    print(f"Published {len(articles)} articles to {args.queue_url}")

if __name__ == "__main__":
    main()
