"""Human approval and GitHub issue request schemas.

No external write action is performed without an explicit approved
``ApprovalRequest``; ``GitHubIssueRequest`` defaults to a dry run.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ApprovalRequest(BaseModel):
    """Explicit human approval gate for a sensitive action."""

    model_config = ConfigDict(extra="forbid", strict=True)

    incident_id: str
    action: Literal["create_github_issue", "create_pr", "post_comment"]
    approved_by: str
    approved: bool = False
    note: str | None = None


class GitHubIssueRequest(BaseModel):
    """Payload for creating a GitHub issue, dry-run by default."""

    model_config = ConfigDict(extra="forbid", strict=True)

    incident_id: str
    title: str
    body: str
    labels: list[str] = Field(default_factory=list)
    dry_run: bool = True
