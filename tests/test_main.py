import pytest
from src.main import main as cli_main

def test_main_success(capfd):
    cli_main(["machine learning"])
    out, err = capfd.readouterr()

    assert "✅ Published:" in out or "❌ Failed to publish:" in out
    assert "🎉 Done! Published" in out


def test_main_invalid_args():
    with pytest.raises(SystemExit):
        cli_main(["dummy arg1", "dummy arg2"])
