from fastapi import APIRouter

from app.schemas.incident import IncidentTriggerRequest, IncidentTriggerResponse
from app.services.investigation_service import create_incident

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.post("/trigger", response_model=IncidentTriggerResponse)
def trigger_incident(request: IncidentTriggerRequest) -> IncidentTriggerResponse:
    return create_incident(request.scenario)
