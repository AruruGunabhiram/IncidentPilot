from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.findings import Confidence, _coerce_evidence_items
from app.schemas.incident import EvidenceItem


class SafetySummary(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    secrets_redacted: bool = True
    github_dry_run: bool = True
    write_actions_enabled: bool = False


class SafetyReview(SafetySummary):
    summary: str = Field(default="", min_length=0)
    confidence: float = Confidence
    evidence: list[EvidenceItem] = Field(default_factory=list)
    needs_human_review: bool = True
    blocked_reasons: list[str] = Field(default_factory=list)
    decision: Literal["approved", "blocked", "needs_review"] = "needs_review"
    write_scope: Literal["none", "local_only", "external_dry_run"] = "none"

    @field_validator("evidence", mode="before")
    @classmethod
    def coerce_evidence(cls, value: Any) -> Any:
        return _coerce_evidence_items(value)
