import logging
import boto3
import json
from botocore.exceptions import ClientError
from botocore.config import Config
from src.aws_config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    SQS_QUEUE_URL,
)

# Create a botocore Config with retry options
boto_config = Config(
    region_name=AWS_REGION,
    retries={
        "max_attempts": 5,
        "mode": "standard",
    },
)


def get_sqs_client():
    return boto3.client(
        "sqs",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        config=boto_config,
    )


def publish_messages(messages):
    sqs_client = get_sqs_client()  # Lazy instantiation inside function scope

    try:
        response = sqs_client.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(messages),
        )
        logging.info(f"Message sent: {response.get('MessageId')}")
        return response
    except ClientError as e:
        logging.error(f"Error sending message to SQS: {str(e)}")
        return None
