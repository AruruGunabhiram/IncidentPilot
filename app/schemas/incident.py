from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class EvidenceItem(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    source_type: Literal["ci_log", "repo_file", "user_note", "system", "unknown"] = "unknown"
    source: str = Field(..., min_length=1)
    summary: str = Field(..., min_length=1)
    content: str | None = Field(default=None, min_length=1)
    file_path: str | None = Field(default=None, min_length=1)
    line_start: int | None = Field(default=None, ge=1)
    line_end: int | None = Field(default=None, ge=1)
    redacted: bool = True


class IncidentIntake(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    scenario: str = Field(..., min_length=1, examples=["broken_api_route"])
    title: str | None = Field(default=None, min_length=1)
    description: str | None = Field(default=None, min_length=1)
    severity: Literal["low", "medium", "high", "critical", "unknown"] = "unknown"
    evidence: list[EvidenceItem] = Field(default_factory=list)
    labels: list[str] = Field(default_factory=list)


class IncidentTriggerRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    scenario: str = Field(..., examples=["broken_api_route"])


class IncidentTriggerResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    incident_id: str
    status: str
    scenario: str
