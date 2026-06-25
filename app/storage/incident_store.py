from app.schemas.findings import Finding
from app.schemas.report import IncidentReport
from app.schemas.safety import SafetySummary

_REPORTS: dict[str, IncidentReport] = {}


def create_placeholder_incident(incident_id: str, scenario: str) -> IncidentReport:
    report = IncidentReport(
        incident_id=incident_id,
        scenario=scenario,
        summary="Placeholder investigation report. AI analysis is not implemented yet.",
        findings=[
            Finding(
                title="Investigation pending",
                severity="info",
                evidence=["Local demo fixtures are available for deterministic analysis."],
                recommendation="Run local tools before enabling agent orchestration.",
            )
        ],
        safety=SafetySummary(),
    )
    _REPORTS[incident_id] = report
    return report


def get_report(incident_id: str) -> IncidentReport | None:
    if incident_id not in _REPORTS and incident_id == "inc_001":
        return create_placeholder_incident(incident_id="inc_001", scenario="broken_api_route")
    return _REPORTS.get(incident_id)
