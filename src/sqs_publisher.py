# src/sqs_publisher.py

import boto3
import json

def publish_to_sqs(queue_url, message_body):
    sqs = boto3.client("sqs")
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message_body)
    )
    return response
