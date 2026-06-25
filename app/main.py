from fastapi import FastAPI

from app.api.routes_health import router as health_router
from app.api.routes_incidents import router as incidents_router
from app.api.routes_reports import router as reports_router

app = FastAPI(title="IncidentPilot", version="0.1.0")

app.include_router(health_router)
app.include_router(incidents_router)
app.include_router(reports_router)
