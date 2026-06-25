from pydantic import BaseModel, Field


class IncidentTriggerRequest(BaseModel):
    scenario: str = Field(..., examples=["broken_api_route"])


class IncidentTriggerResponse(BaseModel):
    incident_id: str
    status: str
    scenario: str
