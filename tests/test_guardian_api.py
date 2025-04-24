import os
import pytest
import requests
from unittest.mock import patch, Mock
from src.guardian_api import fetch_articles

# Sample API response from Guardian
MOCK_RESPONSE = {
    "response": {
        "results": [
            {
                "webPublicationDate": "2023-11-21T11:11:31Z",
                "webTitle": "Who said what: using machine learning to correctly attribute quotes",
                "webUrl": "https://www.theguardian.com/info/2023/nov/21/who-said-what"
            }
        ]
    }
}

@patch("src.guardian_api.requests.get")
def test_fetch_articles_success(mock_get):
    os.environ["GUARDIAN_API_KEY"] = "test-key"
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_RESPONSE
    mock_get.return_value = mock_response

    articles = fetch_articles("machine learning")

    assert isinstance(articles, list)
    assert len(articles) == 1
    assert articles[0]["webTitle"] == MOCK_RESPONSE["response"]["results"][0]["webTitle"]

@patch("src.guardian_api.requests.get")
def test_fetch_articles_with_date(mock_get):
    os.environ["GUARDIAN_API_KEY"] = "test-key"

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_RESPONSE
    mock_get.return_value = mock_response

    articles = fetch_articles("machine learning", date_from="2023-01-01")

    mock_get.assert_called_once()
    url = mock_get.call_args[1]["params"]
    assert url["from-date"] == "2023-01-01"

@patch("src.guardian_api.requests.get")
def test_fetch_articles_error_response(mock_get):
    os.environ["GUARDIAN_API_KEY"] = "test-key"

    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("Bad request")
    mock_get.return_value = mock_response

    with pytest.raises(requests.HTTPError):
        fetch_articles("machine learning")

def test_fetch_articles_missing_api_key():
    if "GUARDIAN_API_KEY" in os.environ:
        del os.environ["GUARDIAN_API_KEY"]

    with pytest.raises(EnvironmentError, match="GUARDIAN_API_KEY not found"):
        fetch_articles("machine learning")
