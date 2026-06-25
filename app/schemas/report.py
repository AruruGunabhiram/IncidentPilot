from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.findings import (
    CodeFinding,
    Confidence,
    Finding,
    FixPlan,
    LogFinding,
    RootCauseHypothesis,
    _coerce_evidence_items,
)
from app.schemas.incident import EvidenceItem
from app.schemas.safety import SafetyReview


class IncidentReport(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    incident_id: str
    scenario: str
    summary: str = Field(..., min_length=1)
    confidence: float = Confidence
    evidence: list[EvidenceItem] = Field(default_factory=list)
    needs_human_review: bool = True
    blocked_reasons: list[str] = Field(default_factory=list)
    status: Literal["draft", "blocked", "ready_for_review", "approved"] = "draft"
    findings: list[Finding | LogFinding | CodeFinding] = Field(default_factory=list)
    root_cause_hypotheses: list[RootCauseHypothesis] = Field(default_factory=list)
    fix_plan: FixPlan | None = None
    safety: SafetyReview = Field(default_factory=SafetyReview)

    @field_validator("evidence", mode="before")
    @classmethod
    def coerce_evidence(cls, value: Any) -> Any:
        return _coerce_evidence_items(value)
