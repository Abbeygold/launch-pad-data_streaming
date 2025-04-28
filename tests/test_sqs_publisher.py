import json
import logging
from unittest.mock import patch, Mock
from botocore.exceptions import ClientError
from src import sqs_publisher

@patch("src.sqs_publisher.get_sqs_client")
def test_publish_messages_success(mock_get_sqs_client):
    mock_sqs_client = Mock()
    mock_get_sqs_client.return_value = mock_sqs_client
    
    mock_response = {"MessageId": "12345"}
    mock_sqs_client.send_message.return_value = mock_response
    
    test_messages = {"key": "value"}
    
    response = sqs_publisher.publish_messages(test_messages)
    
    mock_sqs_client.send_message.assert_called_once_with(
        QueueUrl=sqs_publisher.SQS_QUEUE_URL,
        MessageBody=json.dumps(test_messages),
    )
    assert response == mock_response

# Failure to send message (ClientError)
@patch("src.sqs_publisher.get_sqs_client")
def test_publish_messages_failure(mock_get_sqs_client, caplog):
    
    mock_sqs_client = Mock()
    mock_get_sqs_client.return_value = mock_sqs_client

    # Simulate a ClientError during send_message
    error_response = {"Error": {"Code": "500", "Message": "Internal Error"}}
    mock_sqs_client.send_message.side_effect = ClientError(
        error_response=error_response, operation_name="SendMessage"
    )

    test_messages = {"key": "value"}
    
    with caplog.at_level(logging.ERROR):
        response = sqs_publisher.publish_messages(test_messages)
    
    mock_sqs_client.send_message.assert_called_once()
    assert response is None
    assert "Error sending message to SQS" in caplog.text
