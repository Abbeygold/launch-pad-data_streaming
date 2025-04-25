import argparse
from guardian_api import fetch_articles
from sqs_publisher import publish_messages
import logging

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


def main(args=None):
    args = parse_args(args)

    articles = fetch_articles(args.search_term, args.date_from)

    for article in articles:
        try:
            response = publish_messages(article)
            if response:
                print(
                    f"✅ Published: {article['webTitle']} "
                    f"(Message ID: {response['MessageId']})"
                )
            else:
                print(f"❌ Failed to publish: {article['webTitle']} — SQS error")
        except Exception as e:
            print(f"❌ Failed to publish: {article['webTitle']} — {str(e)}")

    print(f"\n🎉 Done! Published {len(articles)} articles to SQS.")


if __name__ == "__main__":
    main()
