from pathlib import Path

from app.tools.repo_search import search_repo


def test_repo_search_finds_known_string_in_demo_repo():
    results = search_repo("payment.user_id = user.id", Path("demo/demo_repo"))

    assert results
    assert any(result["path"] == "app/routes/payments.py" for result in results)

    match = next(result for result in results if result["path"] == "app/routes/payments.py")
    assert "payment.user_id = user.id" in match["snippet"]
    assert isinstance(match["line"], int) and match["line"] > 0
