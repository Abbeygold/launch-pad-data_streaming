# tests/test_main.py
import pytest
from src.main import main as cli_main

def test_main_success(capfd):
    cli_main(["machine learning", "--queue_url", "https://example.com/queue"])
    out, err = capfd.readouterr()
    assert "machine learning" in out
    assert "https://example.com/queue" in out

def test_main_invalid_args():
    with pytest.raises(SystemExit):
        cli_main(["--queue_url", "https://example.com/queue"])
