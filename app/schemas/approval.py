from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.findings import Confidence, _coerce_evidence_items
from app.schemas.incident import EvidenceItem


class ApprovalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    summary: str = Field(..., min_length=1)
    confidence: float = Confidence
    evidence: list[EvidenceItem] = Field(default_factory=list)
    needs_human_review: bool = True
    blocked_reasons: list[str] = Field(default_factory=list)
    requested_action: Literal[
        "generate_report",
        "open_github_issue_dry_run",
        "apply_local_fix_dry_run",
    ]
    requester: str | None = Field(default=None, min_length=1)
    dry_run: bool = True

    @field_validator("evidence", mode="before")
    @classmethod
    def coerce_evidence(cls, value: Any) -> Any:
        return _coerce_evidence_items(value)


class GitHubIssueRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    summary: str = Field(..., min_length=1)
    confidence: float = Confidence
    evidence: list[EvidenceItem] = Field(default_factory=list)
    needs_human_review: bool = True
    blocked_reasons: list[str] = Field(default_factory=list)
    repo_owner: str = Field(..., min_length=1)
    repo_name: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)
    labels: list[str] = Field(default_factory=list)
    dry_run: bool = True

    @field_validator("evidence", mode="before")
    @classmethod
    def coerce_evidence(cls, value: Any) -> Any:
        return _coerce_evidence_items(value)
