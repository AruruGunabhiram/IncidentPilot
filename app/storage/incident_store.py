"""In-memory incident store for the IncidentPilot control plane.

Phase 4 keeps all state in process memory: no database, no disk writes, no
network. Each incident owns its normalized intake, the latest generated report,
and any human approvals, giving the thin FastAPI routes and the deterministic
services a single source of truth.

State is module-global and resets on process restart, which is all the demo and
the test suite require. ``reset_store`` exists so tests can start from a clean
slate.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.schemas.approval import ApprovalRecord
from app.schemas.incident import IncidentIntake
from app.schemas.report import IncidentReport

# Stable ids for the known demo scenarios, so triggering ``broken_api_route``
# always yields ``inc_001`` for the demo regardless of trigger order. Unknown
# scenarios fall back to a sequential id that cannot collide with these.
KNOWN_SCENARIO_IDS: dict[str, str] = {
    "broken_api_route": "inc_001",
    "secret_in_logs": "inc_002",
    "ambiguous_error": "inc_003",
}


@dataclass
class IncidentState:
    """Everything the control plane tracks for a single incident."""

    incident_id: str
    scenario: str
    intake: IncidentIntake
    report: IncidentReport | None = None
    approvals: dict[str, ApprovalRecord] = field(default_factory=dict)


_INCIDENTS: dict[str, IncidentState] = {}
_SCENARIO_INDEX: dict[str, str] = {}
_UNKNOWN_COUNTER = {"next": 900}


def reset_store() -> None:
    """Clear all in-memory state (used by tests)."""
    _INCIDENTS.clear()
    _SCENARIO_INDEX.clear()
    _UNKNOWN_COUNTER["next"] = 900


def _assign_incident_id(scenario: str) -> str:
    """Return a stable id for ``scenario`` (known map first, else sequential)."""
    if scenario in KNOWN_SCENARIO_IDS:
        return KNOWN_SCENARIO_IDS[scenario]
    _UNKNOWN_COUNTER["next"] += 1
    return f"inc_{_UNKNOWN_COUNTER['next']}"


def register_incident(scenario: str, intake: IncidentIntake) -> IncidentState:
    """Create (or refresh) the incident for ``scenario`` and return its state.

    Triggering the same scenario twice is idempotent: it returns the existing
    incident (with refreshed intake) rather than creating a duplicate.
    """
    existing_id = _SCENARIO_INDEX.get(scenario)
    if existing_id is not None and existing_id in _INCIDENTS:
        state = _INCIDENTS[existing_id]
        state.intake = intake
        return state

    incident_id = _assign_incident_id(scenario)
    state = IncidentState(incident_id=incident_id, scenario=scenario, intake=intake)
    _INCIDENTS[incident_id] = state
    _SCENARIO_INDEX[scenario] = incident_id
    return state


def get_incident(incident_id: str) -> IncidentState | None:
    """Return the incident state for ``incident_id``, or ``None`` if unknown."""
    return _INCIDENTS.get(incident_id)


def save_report(incident_id: str, report: IncidentReport) -> None:
    """Attach the latest generated ``report`` to its incident."""
    state = _INCIDENTS.get(incident_id)
    if state is not None:
        state.report = report


def get_report(incident_id: str) -> IncidentReport | None:
    """Return the stored report for ``incident_id``, or ``None`` if not ready."""
    state = _INCIDENTS.get(incident_id)
    return state.report if state is not None else None


def record_approval(incident_id: str, record: ApprovalRecord) -> None:
    """Store a human approval decision, keyed by its action."""
    state = _INCIDENTS.get(incident_id)
    if state is not None:
        state.approvals[record.action] = record


def get_approval(incident_id: str, action: str) -> ApprovalRecord | None:
    """Return the stored approval for ``incident_id``/``action`` if present."""
    state = _INCIDENTS.get(incident_id)
    if state is None:
        return None
    return state.approvals.get(action)
