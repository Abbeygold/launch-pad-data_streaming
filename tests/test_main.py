import pytest
from unittest.mock import patch
from src.main import run, main as cli_main


@pytest.fixture
def article_stub():
    return [{"webTitle": "Test Article", "webUrl": "https://example.com"}]


@pytest.fixture
def patch_fetch_articles(article_stub):
    with patch("src.main.fetch_articles", return_value=article_stub) as mock:
        yield mock


@pytest.fixture
def patch_publish_success():
    with patch(
        "src.main.publish_messages", return_value={"MessageId": "12345"}
    ) as mock:
        yield mock


@pytest.fixture
def patch_publish_none():
    with patch("src.main.publish_messages", return_value=None) as mock:
        yield mock


@pytest.fixture
def patch_publish_exception():
    with patch(
        "src.main.publish_messages", side_effect=Exception("Unexpected Error")
    ) as mock:
        yield mock


def test_run_success(patch_fetch_articles, patch_publish_success):
    results = run("machine learning")
    assert results == [{"title": "Test Article", "message_id": "12345", "error": None}]


def test_run_publish_failure(patch_fetch_articles, patch_publish_none):
    results = run("machine learning")
    assert results == [
        {"title": "Test Article", "message_id": None, "error": "SQS Error"}
    ]


def test_run_exception(patch_fetch_articles, patch_publish_exception):
    results = run("machine learning")
    assert results == [
        {"title": "Test Article", "message_id": None, "error": "Unexpected Error"}
    ]


def test_main_cli_output(patch_fetch_articles, patch_publish_success, capfd):
    cli_main(["machine learning"])
    out, _ = capfd.readouterr()

    assert "✅ Published: Test Article (Message ID: 12345)" in out
    assert "🎉 Done! Published 1 articles to SQS." in out


def test_main_invalid_args():
    with pytest.raises(SystemExit):
        cli_main(["too", "many", "args"])
