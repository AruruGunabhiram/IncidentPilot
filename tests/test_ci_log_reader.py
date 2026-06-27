from pathlib import Path

import pytest

from app.tools.ci_log_reader import read_ci_log, read_ci_log_structured
from app.tools.path_guard import UnsafePathError
from app.tools.redactor import REDACTION_MARKER

BROKEN = Path("demo/incidents/broken_api_route")
SECRET = Path("demo/incidents/secret_in_logs")

RAW_FAKE_SECRETS = [
    "ghp_fakeTokenForDemoOnly1234567890",
    "fake.jwt.token",
    "postgres://user:password@example.com:5432/payments",
    "fake-api-key-12345",
]


# ---- happy paths -----------------------------------------------------------


def test_read_ci_log_preserves_line_numbers():
    lines = read_ci_log(BROKEN, "ci.log")

    assert lines
    # Line numbers are 1-based, contiguous, and in order.
    assert [item["line"] for item in lines] == list(range(1, len(lines) + 1))

    # The AttributeError sits on the line the expected report cites (26).
    error_line = next(
        item for item in lines if "AttributeError: 'NoneType'" in item["content"]
    )
    assert error_line["line"] == 26


def test_read_ci_log_redacts_secrets():
    result = read_ci_log_structured(SECRET, "ci.log")
    joined = "\n".join(item["content"] for item in result["lines"])

    for secret in RAW_FAKE_SECRETS:
        assert secret not in joined, f"raw secret leaked: {secret}"
    assert REDACTION_MARKER in joined
    assert result["redactions_applied"] >= 4
    assert result["line_count"] == len(result["lines"])


def test_clean_log_reports_zero_redactions():
    result = read_ci_log_structured(BROKEN, "ci.log")
    assert result["redactions_applied"] == 0


# ---- failure paths ---------------------------------------------------------


def test_read_ci_log_blocks_path_traversal():
    with pytest.raises(UnsafePathError):
        read_ci_log(BROKEN, "../../../etc/passwd")


def test_read_ci_log_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        read_ci_log(BROKEN, "does_not_exist.log")
