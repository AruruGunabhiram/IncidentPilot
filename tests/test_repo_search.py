from pathlib import Path

from app.tools.repo_search import search_repo


def test_repo_search_finds_known_string_in_demo_repo():
    results = search_repo("BUG_MARKER_BROKEN_PAYMENT_ROUTE", Path("demo/demo_repo"))

    assert results
    assert results[0]["path"] == "app/routes/payments.py"
    assert results[0]["line"] == 6
    assert "BUG_MARKER_BROKEN_PAYMENT_ROUTE" in results[0]["snippet"]
