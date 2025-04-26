import pytest
from src.main import main as cli_main
from unittest.mock import patch

@patch("src.main.publish_messages", return_value={"MessageId": "12345"})
@patch("src.main.fetch_articles", return_value=[{"webTitle": "Test Article", "webUrl": "https://example.com"}])
def test_main_success(mock_fetch_articles, mock_publish_messages, capfd):
    cli_main(["machine learning"])

    out, err = capfd.readouterr()

    assert "✅ Published: Test Article (Message ID: 12345)" in out
    assert "🎉 Done! Published 1 articles to SQS." in out


def test_main_invalid_args():
    with pytest.raises(SystemExit):
        cli_main(["dummy arg1", "dummy arg2"])
