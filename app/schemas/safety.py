"""Safety reviewer schema.

Defaults are conservative: nothing is approved, human approval is required, and
no direct production change is assumed, until the Safety Reviewer agent proves
otherwise from evidence.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from app.schemas.findings import ReviewedOutput


class SafetyReview(ReviewedOutput):
    """Output of the Safety Reviewer agent gating display and external writes."""

    approved_for_display: bool = False
    approved_for_github_issue: bool = False
    approved_for_pr: bool = False
    risk_level: Literal["low", "medium", "high", "critical"] = "high"
    secrets_redacted: bool = False
    repo_paths_verified: bool = False
    confidence_above_threshold: bool = False
    human_approval_required: bool = True
    no_direct_production_change: bool = True
    required_human_action: str | None = None
