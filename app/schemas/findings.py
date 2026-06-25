from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.schemas.incident import EvidenceItem


Confidence = Field(default=0.0, ge=0.0, le=1.0)


def _coerce_evidence_items(value: Any) -> Any:
    if value is None:
        return []
    if isinstance(value, list):
        coerced: list[Any] = []
        for item in value:
            if isinstance(item, str):
                coerced.append(
                    {
                        "source_type": "system",
                        "source": "legacy",
                        "summary": item,
                        "redacted": True,
                    }
                )
            else:
                coerced.append(item)
        return coerced
    return value


class ReviewedOutput(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    summary: str = Field(default="", min_length=0)
    confidence: float = Confidence
    evidence: list[EvidenceItem] = Field(default_factory=list)
    needs_human_review: bool = True
    blocked_reasons: list[str] = Field(default_factory=list)


class LogFinding(ReviewedOutput):
    finding_type: Literal["log"] = "log"
    severity: Literal["info", "low", "medium", "high", "critical", "unknown"] = "unknown"
    title: str | None = Field(default=None, min_length=1)
    log_source: str | None = Field(default=None, min_length=1)
    matched_text: str | None = Field(default=None, min_length=1)
    recommendation: str | None = Field(default=None, min_length=1)

    @field_validator("evidence", mode="before")
    @classmethod
    def coerce_evidence(cls, value: Any) -> Any:
        return _coerce_evidence_items(value)

    @model_validator(mode="before")
    @classmethod
    def fill_summary_from_legacy_title(cls, value: Any) -> Any:
        if isinstance(value, dict) and not value.get("summary") and value.get("title"):
            value = {**value, "summary": value["title"]}
        return value


class CodeFinding(ReviewedOutput):
    finding_type: Literal["code"] = "code"
    severity: Literal["info", "low", "medium", "high", "critical", "unknown"] = "unknown"
    title: str | None = Field(default=None, min_length=1)
    file_path: str = Field(..., min_length=1)
    line_start: int | None = Field(default=None, ge=1)
    line_end: int | None = Field(default=None, ge=1)
    symbol: str | None = Field(default=None, min_length=1)
    recommendation: str | None = Field(default=None, min_length=1)

    @field_validator("evidence", mode="before")
    @classmethod
    def coerce_evidence(cls, value: Any) -> Any:
        return _coerce_evidence_items(value)


class RootCauseHypothesis(ReviewedOutput):
    hypothesis_type: Literal["root_cause"] = "root_cause"
    likelihood: Literal["low", "medium", "high", "unknown"] = "unknown"
    affected_components: list[str] = Field(default_factory=list)

    @field_validator("evidence", mode="before")
    @classmethod
    def coerce_evidence(cls, value: Any) -> Any:
        return _coerce_evidence_items(value)


class FixPlan(ReviewedOutput):
    plan_type: Literal["fix_plan"] = "fix_plan"
    risk_level: Literal["low", "medium", "high", "unknown"] = "unknown"
    proposed_steps: list[str] = Field(default_factory=list)
    requires_approval: bool = True
    dry_run_only: bool = True

    @field_validator("evidence", mode="before")
    @classmethod
    def coerce_evidence(cls, value: Any) -> Any:
        return _coerce_evidence_items(value)


class Finding(LogFinding):
    """Compatibility alias for existing placeholder report code."""
