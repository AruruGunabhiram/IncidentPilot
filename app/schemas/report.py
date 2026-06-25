from pydantic import BaseModel

from app.schemas.findings import Finding
from app.schemas.safety import SafetySummary


class IncidentReport(BaseModel):
    incident_id: str
    scenario: str
    summary: str
    findings: list[Finding]
    safety: SafetySummary
