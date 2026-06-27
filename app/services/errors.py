"""Domain errors for the incident control plane.

Services raise these plain exceptions instead of importing FastAPI. ``app.main``
registers a single handler that turns each one into a clean JSON response with
the right HTTP status, so route handlers stay thin and never build error
responses by hand.
"""

from __future__ import annotations


class IncidentError(Exception):
    """Base class for control-plane errors. Carries an HTTP status + detail."""

    status_code: int = 400

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class ScenarioNotFound(IncidentError):
    """The requested demo scenario has no intake fixture."""

    status_code = 404


class IncidentNotFound(IncidentError):
    """No incident exists for the given id (it was never triggered)."""

    status_code = 404


class ReportNotReady(IncidentError):
    """The incident exists but has not been investigated yet."""

    status_code = 400


class SafetyBlocked(IncidentError):
    """The safety review does not permit the requested external action."""

    status_code = 403


class ApprovalRequired(IncidentError):
    """A required human approval is missing for the requested action."""

    status_code = 403
