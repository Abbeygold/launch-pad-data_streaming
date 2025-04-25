# tests/test_main.py
import pytest
from src.main import main as cli_main

def test_main_success(capfd):
    cli_main(["machine learning"])
    out, err = capfd.readouterr()
    assert "machine learning" in out
    assert "Successfully published" in out or "No articles found" in out

def test_main_invalid_args():
    with pytest.raises(SystemExit):
        cli_main(["--queue_url", "https://example.com/queue"])
