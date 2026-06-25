from app.schemas.incident import IncidentTriggerResponse
from app.storage.incident_store import create_placeholder_incident


def create_incident(scenario: str) -> IncidentTriggerResponse:
    incident_id = "inc_001"
    create_placeholder_incident(incident_id=incident_id, scenario=scenario)
    return IncidentTriggerResponse(incident_id=incident_id, status="created", scenario=scenario)
