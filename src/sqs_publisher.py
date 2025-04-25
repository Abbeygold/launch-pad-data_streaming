import logging
import boto3
import json
from aws_config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    SQS_QUEUE_URL,
)
from botocore.exceptions import ClientError


def get_sqs_client():
    return boto3.client(
        "sqs",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )


def publish_messages(messages):
    try:
        sqs = boto3.client("sqs")
        response = sqs.send_message(
            QueueUrl=SQS_QUEUE_URL, MessageBody=json.dumps(messages)
        )
        logging.info(f"Message sent: {response.get('MessageId')}")
        return response
    except ClientError as e:
        logging.error(f"Error sending message to SQS: {str(e)}")
        return None  # Return None to indicate failure
