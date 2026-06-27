"""Human approval and GitHub issue request/response schemas.

No external write action is performed without an explicit, approved decision;
GitHub issue handling defaults to a dry run and only ever returns a preview in
this build. These models are the API contracts for the ``/approve`` and
``/github/issue`` endpoints.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ApprovalAction = Literal["create_github_issue", "create_pr", "post_comment"]


class ApprovalRequest(BaseModel):
    """Explicit human approval gate for a sensitive action."""

    model_config = ConfigDict(extra="forbid", strict=True)

    incident_id: str
    action: ApprovalAction
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


# ---------------------------------------------------------------------------
# Phase 4 control-plane contracts
# ---------------------------------------------------------------------------


class ApprovalDecision(BaseModel):
    """Body for ``POST /incidents/{id}/approve``.

    Every field has a default so the demo can approve with an empty body. The
    action is fixed to ``create_github_issue`` — the only sensitive action this
    phase supports.
    """

    model_config = ConfigDict(extra="forbid", strict=True)

    approved: bool = True
    approved_by: str = "demo-operator"
    note: str | None = None


class ApprovalRecord(BaseModel):
    """A stored approval decision for one incident + action."""

    model_config = ConfigDict(extra="forbid", strict=True)

    incident_id: str
    action: ApprovalAction = "create_github_issue"
    approved: bool = False
    approved_by: str = "demo-operator"
    note: str | None = None
    recorded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ApprovalResponse(BaseModel):
    """Response for ``POST /incidents/{id}/approve``."""

    model_config = ConfigDict(extra="forbid")

    incident_id: str
    action: ApprovalAction
    approved: bool
    approved_by: str
    message: str


class GitHubIssueOptions(BaseModel):
    """Body for ``POST /incidents/{id}/github/issue``.

    The title and body are generated from the grounded, redacted report — never
    taken from the caller — so an issue can only ever contain verified content.
    """

    model_config = ConfigDict(extra="forbid", strict=True)

    dry_run: bool = True
    labels: list[str] = Field(default_factory=list)


class GitHubIssueResult(BaseModel):
    """Response for ``POST /incidents/{id}/github/issue``.

    In this phase ``created`` is always ``False``: the endpoint returns a
    redacted preview of the issue it *would* file, never performing a network
    write.
    """

    model_config = ConfigDict(extra="forbid")

    incident_id: str
    created: bool
    dry_run: bool
    mode: Literal["preview", "not_implemented"]
    title: str
    body: str
    labels: list[str] = Field(default_factory=list)
    url: str | None = None
    message: str
