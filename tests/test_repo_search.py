from pathlib import Path

from app.tools.repo_search import search_repo

DEMO_REPO = Path("demo/demo_repo")


# ---- happy paths -----------------------------------------------------------


def test_repo_search_finds_known_string_in_demo_repo():
    results = search_repo("payment.user_id = user.id", DEMO_REPO)

    assert results
    assert any(result["path"] == "app/routes/payments.py" for result in results)

    match = next(r for r in results if r["path"] == "app/routes/payments.py")
    assert "payment.user_id = user.id" in match["snippet"]
    assert isinstance(match["line"], int) and match["line"] > 0


def test_repo_search_returns_only_real_existing_files():
    results = search_repo("def ", DEMO_REPO)

    assert results
    for result in results:
        # Paths are relative and resolve to a real file inside the demo repo.
        resolved = (DEMO_REPO / result["path"]).resolve()
        assert resolved.is_file()
        assert DEMO_REPO.resolve() in resolved.parents


# ---- failure paths ---------------------------------------------------------


def test_repo_search_empty_term_returns_nothing():
    assert search_repo("", DEMO_REPO) == []


def test_repo_search_missing_term_returns_empty_list():
    results = search_repo("this_string_is_not_anywhere_in_the_repo_xyz", DEMO_REPO)
    assert results == []


def test_repo_search_respects_max_results():
    results = search_repo("e", DEMO_REPO, max_results=3)
    assert len(results) <= 3
