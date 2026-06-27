"""Phase 7 — deterministic safety gate and action gating.

These tests pin the safety reviewer's *deterministic* behavior: the Python gate
in :mod:`app.services.safety_gate` is the single source of truth for whether a
report may be displayed, filed as a GitHub issue, or used for a PR. They cover

* the structured ``SafetyChecks`` shape and the exact, stable blocked-reason
  strings,
* the three-tier confidence policy (>=0.75 eligible, 0.50–0.75 blocked, <0.50
  low-confidence diagnostic),
* secret handling and unverified file references,
* determinism,
* the action gate — unsafe GitHub issue creation is blocked *before* any GitHub
  client call, a PR is never allowed, and no real external write happens, and
* authority — the gate reads the structured checks, so flipping a single
  approval boolean (as a misbehaving LLM/agent might) cannot authorize a blocked
  action.

No LLM, no network, no real GitHub write.
"""

from __future__ import annotations

import pytest

from app.schemas.approval import ApprovalRecord, GitHubIssueOptions
from app.schemas.report import IncidentReport
from app.schemas.safety import SafetyChecks, SafetyReview
from app.services import investigation_service as svc
from app.services import safety_gate
from app.services.errors import ApprovalRequired, SafetyBlocked
from app.services.safety_gate import (
    REASON_CONFIDENCE_BELOW_THRESHOLD,
    REASON_DIRECT_PRODUCTION_CHANGE,
    REASON_HUMAN_APPROVAL_REQUIRED,
    REASON_REPO_PATHS_UNVERIFIED,
    REASON_SECRET_BEARING_SOURCE,
    REASON_SECRETS_NOT_REDACTED,
    REASON_UNVERIFIED_FILE_REFERENCE,
    SAFETY_ISSUE_CONFIDENCE_THRESHOLD,
    assert_github_issue_allowed,
    checks_blocked_reasons,
    evaluate_safety,
    github_issue_block_reasons,
)
from app.storage import incident_store as store

# Fake secrets seeded into demo/incidents/secret_in_logs; none may ever appear
# raw in a safety verdict or a blocked-reason error message.
RAW_FAKE_SECRETS = [
    "ghp_fakeTokenForDemoOnly1234567890",
    "fake.jwt.token",
    "postgres://user:password@example.com:5432/payments",
    "fake-api-key-12345",
]

# The six structured checks, by exact field name. Pinned so the required output
# shape can never drift silently.
REQUIRED_CHECK_FIELDS = {
    "secrets_redacted",
    "repo_paths_verified",
    "confidence_above_threshold",
    "human_approval_required",
    "no_direct_production_change",
    "no_unverified_file_references",
}


@pytest.fixture(autouse=True)
def _reset_store():
    store.reset_store()
    yield
    store.reset_store()


def _report(scenario: str) -> IncidentReport:
    """Investigate ``scenario`` from a clean store and return its report."""
    store.reset_store()
    return svc.investigate_incident(scenario, persist=False)


# ---------------------------------------------------------------------------
# Structured checks + exact blocked-reason strings
# ---------------------------------------------------------------------------


def test_safety_checks_fields_match_required_shape():
    """The structured ``checks`` object exposes exactly the six required fields."""
    assert set(SafetyChecks.model_fields) == REQUIRED_CHECK_FIELDS


def test_all_checks_pass_yields_no_blocked_reasons():
    checks = SafetyChecks(
        secrets_redacted=True,
        repo_paths_verified=True,
        confidence_above_threshold=True,
        human_approval_required=True,
        no_direct_production_change=True,
        no_unverified_file_references=True,
    )
    assert checks_blocked_reasons(checks) == []


def test_each_failing_check_maps_to_its_exact_reason():
    cases = [
        ("secrets_redacted", REASON_SECRETS_NOT_REDACTED),
        ("repo_paths_verified", REASON_REPO_PATHS_UNVERIFIED),
        ("confidence_above_threshold", REASON_CONFIDENCE_BELOW_THRESHOLD),
        ("no_unverified_file_references", REASON_UNVERIFIED_FILE_REFERENCE),
        ("no_direct_production_change", REASON_DIRECT_PRODUCTION_CHANGE),
        ("human_approval_required", REASON_HUMAN_APPROVAL_REQUIRED),
    ]
    base = dict(
        secrets_redacted=True,
        repo_paths_verified=True,
        confidence_above_threshold=True,
        human_approval_required=True,
        no_direct_production_change=True,
        no_unverified_file_references=True,
    )
    for field, reason in cases:
        # ``no_*`` and ``*_required`` style fields fail when set to False.
        failing = dict(base)
        failing[field] = False
        reasons = checks_blocked_reasons(SafetyChecks(**failing))
        assert reasons == [reason], f"{field} should map only to {reason!r}"


# ---------------------------------------------------------------------------
# evaluate_safety: the happy, fully-grounded, high-confidence path
# ---------------------------------------------------------------------------


def test_clean_grounded_high_confidence_is_eligible():
    review = evaluate_safety(
        secrets_present=False,
        unverified_file_reference=False,
        confidence=0.90,
    )
    assert review.approved_for_display is True
    assert review.approved_for_github_issue is True  # eligible (pending approval)
    assert review.approved_for_pr is False
    assert review.risk_level == "low"
    assert review.blocked_reasons == []
    assert review.needs_human_review is False
    assert all(review.checks.model_dump().values())  # every invariant holds


def test_pr_is_never_approved_even_at_max_confidence():
    review = evaluate_safety(
        secrets_present=False,
        unverified_file_reference=False,
        confidence=1.0,
    )
    assert review.approved_for_pr is False


# ---------------------------------------------------------------------------
# Confidence policy — three tiers around the 0.75 issue threshold
# ---------------------------------------------------------------------------


def test_threshold_constant_is_three_quarters():
    assert SAFETY_ISSUE_CONFIDENCE_THRESHOLD == 0.75


def test_confidence_at_threshold_is_eligible():
    review = evaluate_safety(
        secrets_present=False, unverified_file_reference=False, confidence=0.75
    )
    assert review.checks.confidence_above_threshold is True
    assert review.approved_for_github_issue is True


def test_mid_confidence_blocks_issue_but_allows_display():
    # 0.50 <= confidence < 0.75: report shown, human review required, issue blocked.
    review = evaluate_safety(
        secrets_present=False, unverified_file_reference=False, confidence=0.60
    )
    assert review.approved_for_display is True
    assert review.approved_for_github_issue is False
    assert review.approved_for_pr is False
    assert review.needs_human_review is True
    assert REASON_CONFIDENCE_BELOW_THRESHOLD in review.blocked_reasons
    assert review.checks.confidence_above_threshold is False


def test_low_confidence_is_diagnostic_only_and_explains_itself():
    # confidence < 0.50: display allowed as a low-confidence diagnostic, every
    # external action blocked, and the low confidence is stated explicitly.
    review = evaluate_safety(
        secrets_present=False, unverified_file_reference=False, confidence=0.20
    )
    assert review.approved_for_display is True
    assert review.approved_for_github_issue is False
    assert review.approved_for_pr is False
    assert review.needs_human_review is True
    assert REASON_CONFIDENCE_BELOW_THRESHOLD in review.blocked_reasons


# ---------------------------------------------------------------------------
# Secrets + unverified file references
# ---------------------------------------------------------------------------


def test_secret_bearing_source_is_high_risk_and_blocked_even_when_redacted():
    review = evaluate_safety(
        secrets_present=True,
        unverified_file_reference=False,
        confidence=0.90,  # high confidence must NOT rescue a secret-bearing source
        redactions_applied=4,
    )
    assert review.risk_level == "high"
    assert review.approved_for_github_issue is False
    assert review.needs_human_review is True
    assert review.secrets_detected is True
    # The secrets were redacted (no leak), so that invariant still passes...
    assert review.checks.secrets_redacted is True
    # ...but the untrusted source blocks an automated external write.
    assert REASON_SECRET_BEARING_SOURCE in review.blocked_reasons


def test_unredacted_secret_fails_the_secrets_check():
    review = evaluate_safety(
        secrets_present=True,
        unverified_file_reference=False,
        confidence=0.90,
        secrets_fully_redacted=False,
    )
    assert review.checks.secrets_redacted is False
    assert REASON_SECRETS_NOT_REDACTED in review.blocked_reasons
    assert review.approved_for_github_issue is False


def test_unverified_file_reference_fails_path_and_reference_checks():
    review = evaluate_safety(
        secrets_present=False,
        unverified_file_reference=True,
        confidence=0.90,
    )
    assert review.checks.repo_paths_verified is False
    assert review.checks.no_unverified_file_references is False
    assert REASON_REPO_PATHS_UNVERIFIED in review.blocked_reasons
    assert REASON_UNVERIFIED_FILE_REFERENCE in review.blocked_reasons
    assert review.approved_for_github_issue is False


def test_required_output_shape_serializes_with_checks_block():
    """Mirrors the Phase 7 required SafetyReview shape, including nested checks."""
    review = evaluate_safety(
        secrets_present=False,
        unverified_file_reference=True,
        confidence=0.40,
    )
    dumped = review.model_dump()
    for key in (
        "approved_for_display",
        "approved_for_github_issue",
        "approved_for_pr",
        "risk_level",
        "checks",
        "blocked_reasons",
        "required_human_action",
    ):
        assert key in dumped
    assert set(dumped["checks"]) == REQUIRED_CHECK_FIELDS
    assert REASON_CONFIDENCE_BELOW_THRESHOLD in dumped["blocked_reasons"]
    assert REASON_UNVERIFIED_FILE_REFERENCE in dumped["blocked_reasons"]
    assert dumped["required_human_action"]


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------


def test_evaluate_safety_is_deterministic():
    kwargs = dict(
        secrets_present=True,
        unverified_file_reference=True,
        confidence=0.42,
        redactions_applied=3,
    )
    first = evaluate_safety(**kwargs)
    second = evaluate_safety(**kwargs)
    assert first.model_dump() == second.model_dump()


# ---------------------------------------------------------------------------
# Integration with the deterministic investigation pipeline
# ---------------------------------------------------------------------------


def test_broken_api_route_report_is_issue_eligible():
    report = _report("broken_api_route")
    review = report.safety_review
    assert review is not None
    assert review.checks.model_dump() == {
        "secrets_redacted": True,
        "repo_paths_verified": True,
        "confidence_above_threshold": True,
        "human_approval_required": True,
        "no_direct_production_change": True,
        "no_unverified_file_references": True,
    }
    assert review.approved_for_github_issue is True
    assert github_issue_block_reasons(report) == []


def test_ambiguous_report_blocked_only_by_confidence():
    report = _report("ambiguous_error")
    assert github_issue_block_reasons(report) == [REASON_CONFIDENCE_BELOW_THRESHOLD]
    assert report.safety_review.approved_for_github_issue is False


def test_secret_report_blocked_and_high_risk():
    report = _report("secret_in_logs")
    review = report.safety_review
    assert review.risk_level == "high"
    assert review.approved_for_github_issue is False
    reasons = github_issue_block_reasons(report)
    assert REASON_SECRET_BEARING_SOURCE in reasons
    assert REASON_CONFIDENCE_BELOW_THRESHOLD in reasons


# ---------------------------------------------------------------------------
# Action gate — assert_github_issue_allowed
# ---------------------------------------------------------------------------


def _approved_record(incident_id: str) -> ApprovalRecord:
    return ApprovalRecord(incident_id=incident_id, approved=True, approved_by="tester")


def test_gate_allows_clean_report_with_approval():
    report = _report("broken_api_route")
    # Should not raise.
    assert_github_issue_allowed(report, _approved_record(report.incident_id))


def test_gate_requires_human_approval_for_clean_report():
    report = _report("broken_api_route")
    with pytest.raises(ApprovalRequired) as exc:
        assert_github_issue_allowed(report, None)
    assert "approval" in str(exc.value).lower()


def test_gate_rejects_unapproved_record():
    report = _report("broken_api_route")
    record = ApprovalRecord(incident_id=report.incident_id, approved=False)
    with pytest.raises(ApprovalRequired):
        assert_github_issue_allowed(report, record)


def test_gate_blocks_unsafe_report_before_approval_is_considered():
    report = _report("secret_in_logs")
    # Even WITH an approval on file, safety blocks first.
    with pytest.raises(SafetyBlocked) as exc:
        assert_github_issue_allowed(report, _approved_record(report.incident_id))
    msg = str(exc.value)
    assert "safety" in msg.lower()
    # The block message must never leak a raw secret.
    for secret in RAW_FAKE_SECRETS:
        assert secret not in msg


def test_gate_is_authoritative_over_a_flipped_approval_boolean():
    """A misbehaving agent/LLM flipping the flat approval cannot authorize a block.

    The gate re-derives its verdict from the structured ``checks``, so tampering
    with the convenience boolean has no effect.
    """
    report = _report("ambiguous_error")
    assert report.safety_review is not None
    report.safety_review.approved_for_github_issue = True  # simulate tampering
    with pytest.raises(SafetyBlocked):
        assert_github_issue_allowed(report, _approved_record(report.incident_id))


def test_missing_safety_review_is_blocked():
    report = _report("broken_api_route")
    report.safety_review = None
    assert github_issue_block_reasons(report)  # non-empty: not eligible
    with pytest.raises(SafetyBlocked):
        assert_github_issue_allowed(report, _approved_record(report.incident_id))


# ---------------------------------------------------------------------------
# End-to-end through investigation_service.create_github_issue (no real write)
# ---------------------------------------------------------------------------


def test_create_github_issue_blocked_for_secret_scenario_even_after_approval():
    svc.investigate_incident("secret_in_logs", persist=False)
    svc.record_github_approval("inc_002", approved=True, approved_by="tester", note=None)
    with pytest.raises(SafetyBlocked):
        svc.create_github_issue(
            "inc_002", GitHubIssueOptions(), github_configured=True, env_dry_run=False
        )


def test_create_github_issue_requires_approval_for_clean_scenario():
    svc.investigate_incident("broken_api_route", persist=False)
    with pytest.raises(ApprovalRequired):
        svc.create_github_issue(
            "inc_001", GitHubIssueOptions(), github_configured=True, env_dry_run=False
        )


def test_create_github_issue_never_writes_even_when_configured_and_not_dry_run():
    """An approved, eligible report still performs no real GitHub write."""
    svc.investigate_incident("broken_api_route", persist=False)
    svc.record_github_approval("inc_001", approved=True, approved_by="tester", note=None)

    result = svc.create_github_issue(
        "inc_001",
        GitHubIssueOptions(dry_run=False),
        github_configured=True,
        env_dry_run=False,
    )
    # No network write occurs in this build: creation is "not_implemented".
    assert result.created is False
    assert result.url is None
    assert result.mode == "not_implemented"


def test_create_github_issue_dry_run_preview_after_approval():
    svc.investigate_incident("broken_api_route", persist=False)
    svc.record_github_approval("inc_001", approved=True, approved_by="tester", note=None)

    result = svc.create_github_issue(
        "inc_001", GitHubIssueOptions(), github_configured=True, env_dry_run=True
    )
    assert result.created is False
    assert result.dry_run is True
    assert result.mode == "preview"
    assert result.title.startswith("[IncidentPilot]")


# ---------------------------------------------------------------------------
# The report explains why an unsafe action was blocked
# ---------------------------------------------------------------------------


def test_blocked_report_explains_itself():
    report = _report("secret_in_logs")
    review = report.safety_review
    assert review.blocked_reasons, "a blocked report must list its reasons"
    assert review.required_human_action
    # The human-facing summary states the issue is blocked and stays secret-free.
    assert "blocked" in review.summary.lower()
    for secret in RAW_FAKE_SECRETS:
        assert secret not in review.summary
