# src/main.py

import argparse
from guardian_api import fetch_articles
from sqs_publisher import publish_to_sqs


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Search Guardian articles and publish to an AWS SQS queue.")
    parser.add_argument("search_term", type=str, help="Search term for articles")
    parser.add_argument("--date_from", type=str, required=False, help="Start date for articles in YYYY-MM-DD format")
    parser.add_argument("--queue_url", type=str, required=True, help="SQS queue URL to publish results to")
    return parser.parse_args(args)


def main(args=None):
    args = parse_args(args)

    articles = fetch_articles(args.search_term, args.date_from)

    for article in articles:
        response = publish_to_sqs(args.queue_url, article)
        print(f"✅ Published: {article['webTitle']} (Message ID: {response['MessageId']})")


if __name__ == "__main__":
    main()
