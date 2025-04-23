# sqs_publisher.py

def publish_articles(articles, queue_url):
    print(f"[Stub] Publishing {len(articles)} articles to queue: {queue_url}")
    for article in articles:
        print(f" -> {article['webTitle']}")
