from fastapi import APIRouter, HTTPException

from app.schemas.report import IncidentReport
from app.storage.incident_store import get_report

router = APIRouter(prefix="/incidents", tags=["reports"])


@router.get("/{incident_id}/report", response_model=IncidentReport)
def read_incident_report(incident_id: str) -> IncidentReport:
    report = get_report(incident_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Incident report not found")
    return report
