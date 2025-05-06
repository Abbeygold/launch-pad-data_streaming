"""
sqs_publisher.py

This module provides functionality to publish messages to an AWS SQS queue.
It uses boto3 for interacting with AWS services and includes basic logging
and retry configuration using botocore.

Environment configurations are loaded from src.aws_config.
Message formatting and logging constants are imported from src.constants.
"""

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
from src.constants import (
    SQS_MAX_RETRIES,
    SQS_RETRY_MODE,
    LOG_MESSAGE_SENT,
    LOG_MESSAGE_FAILED,
)

# Create a botocore Config with retry options
boto_config = Config(
    region_name=AWS_REGION,
    retries={
        "max_attempts": SQS_MAX_RETRIES,
        "mode": SQS_RETRY_MODE,
    },
)


def get_sqs_client():
    """
    Create and return a new SQS client with configured
    AWS credentials and retry settings.

    Returns:
        boto3.client: A boto3 SQS client instance.
    """
    return boto3.client(
        "sqs",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        config=boto_config,
    )


def publish_messages(messages):
    """
    Publishes a JSON-formatted message to the specified AWS SQS queue.

    Args:
        messages (dict): The message payload to send. It must be serializable to JSON.

    Returns:
        dict or None: The response from AWS SQS if the message is sent successfully,
                      or None if there was a failure.
    """
    sqs_client = get_sqs_client()

    try:
        response = sqs_client.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(messages),
        )
        logging.info(LOG_MESSAGE_SENT.format(response.get("MessageId")))
        return response
    except ClientError as e:
        logging.error(LOG_MESSAGE_FAILED.format(str(e)))
        return None
