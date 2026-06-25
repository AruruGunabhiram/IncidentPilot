from __future__ import annotations

from app.schemas.findings import EvidenceItem, LogFinding
from app.schemas.report import IncidentReport
from app.schemas.safety import SafetyReview

_REPORTS: dict[str, IncidentReport] = {}


def create_placeholder_incident(incident_id: str, scenario: str) -> IncidentReport:
    report = IncidentReport(
        incident_id=incident_id,
        title=f"Investigation pending: {scenario}",
        severity="UNKNOWN",
        affected_service=scenario,
        status="created",
        summary="Placeholder investigation report. AI analysis is not implemented yet.",
        needs_human_review=True,
        log_finding=LogFinding(
            summary="Investigation pending.",
            evidence=[
                EvidenceItem(
                    id="ev_placeholder_1",
                    source="demo_fixtures",
                    source_type="unknown",
                    summary="Local demo fixtures are available for deterministic analysis.",
                )
            ],
        ),
        safety_review=SafetyReview(),
    )
    _REPORTS[incident_id] = report
    return report


def get_report(incident_id: str) -> IncidentReport | None:
    if incident_id not in _REPORTS and incident_id == "inc_001":
        return create_placeholder_incident(incident_id="inc_001", scenario="broken_api_route")
    return _REPORTS.get(incident_id)
