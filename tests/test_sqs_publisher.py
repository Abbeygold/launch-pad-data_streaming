import json
import logging
import pytest
from unittest.mock import patch, Mock
from botocore.exceptions import ClientError
from src import sqs_publisher

@pytest.fixture
def mock_sqs_client():
    with patch("src.sqs_publisher.sqs_client") as mock_client:
        yield mock_client

def test_publish_messages_success(mock_sqs_client):
    # Arrange
    mock_response = {"MessageId": "12345"}
    mock_sqs_client.send_message.return_value = mock_response

    test_messages = {"key": "value"}

    # Act
    response = sqs_publisher.publish_messages(test_messages)

    # Assert
    mock_sqs_client.send_message.assert_called_once_with(
        QueueUrl=sqs_publisher.SQS_QUEUE_URL,
        MessageBody=json.dumps(test_messages),
    )
    assert response == mock_response

def test_publish_messages_failure(mock_sqs_client, caplog):
    # Arrange
    error_response = {"Error": {"Code": "500", "Message": "Internal Error"}}
    mock_sqs_client.send_message.side_effect = ClientError(
        error_response=error_response, operation_name="SendMessage"
    )

    test_messages = {"key": "value"}

    with caplog.at_level(logging.ERROR):
        # Act
        response = sqs_publisher.publish_messages(test_messages)

    # Assert
    mock_sqs_client.send_message.assert_called_once()
    assert response is None
    assert "Error sending message to SQS" in caplog.text