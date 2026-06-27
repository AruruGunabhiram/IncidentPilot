import json
from pathlib import Path

from app.tools.redactor import REDACTION_MARKER
from app.tools.report_writer import (
    build_report_dict,
    render_json,
    render_markdown,
    write_report,
)

EXPECTED_REPORT = Path("demo/incidents/broken_api_route/expected_report.json")

# A report dict carrying a planted secret in an evidence snippet, to prove the
# writer scrubs untrusted text even if it slips through upstream.
REPORT_WITH_SECRET = {
    "incident_id": "inc_test",
    "title": "Test incident",
    "severity": "SEV2",
    "affected_service": "payments-api",
    "status": "awaiting_human_approval",
    "summary": "Deploy logged api_key=fake-api-key-12345 by mistake.",
    "confidence": 0.5,
    "needs_human_review": True,
    "blocked_reasons": [],
    "primary_error": "ConnectionError: billing upstream timeout",
    "evidence": [
        {
            "id": "ev1",
            "source": "demo/incidents/secret_in_logs/ci.log",
            "source_type": "ci_log",
            "summary": "Deploy log line with a token.",
            "snippet": "Using GitHub token ghp_fakeTokenForDemoOnly1234567890",
            "path": "demo/incidents/secret_in_logs/ci.log",
            "line_start": 3,
            "line_end": 3,
            "metadata": {},
        }
    ],
}


# ---- happy paths -----------------------------------------------------------


def test_render_json_is_valid_and_deterministic():
    first = render_json(REPORT_WITH_SECRET)
    second = render_json(REPORT_WITH_SECRET)

    assert first == second  # deterministic
    parsed = json.loads(first)
    assert parsed["incident_id"] == "inc_test"


def test_render_markdown_has_sections():
    md = render_markdown(REPORT_WITH_SECRET)

    assert md.startswith("# Test incident")
    assert "## Summary" in md
    assert "## Evidence" in md
    assert "demo/incidents/secret_in_logs/ci.log:3" in md


def test_write_report_creates_json_and_markdown(tmp_path):
    paths = write_report(REPORT_WITH_SECRET, tmp_path)

    json_path = Path(paths["json_path"])
    md_path = Path(paths["markdown_path"])
    assert json_path.is_file() and md_path.is_file()
    # JSON on disk parses.
    json.loads(json_path.read_text(encoding="utf-8"))


# ---- safety path: no raw secrets ------------------------------------------


def test_no_raw_secrets_in_any_output():
    raw_secrets = [
        "ghp_fakeTokenForDemoOnly1234567890",
        "fake-api-key-12345",
    ]
    json_out = render_json(REPORT_WITH_SECRET)
    md_out = render_markdown(REPORT_WITH_SECRET)

    for secret in raw_secrets:
        assert secret not in json_out
        assert secret not in md_out
    assert REDACTION_MARKER in json_out
    assert REDACTION_MARKER in md_out


def test_real_expected_report_renders_without_leaking_secrets():
    data = json.loads(EXPECTED_REPORT.read_text(encoding="utf-8"))
    redacted = build_report_dict(data)

    # Round-trips and stays JSON-safe.
    json.dumps(redacted)
    md = render_markdown(data)
    assert md.startswith("# ")
    # This clean report needs no redaction, so none should appear.
    assert REDACTION_MARKER not in md
