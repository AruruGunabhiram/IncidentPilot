"""Minimal demo app used as a fixture target for repo search.

This is part of the demo_repo fixture, not the IncidentPilot service. It exists
so incident scenarios have a small, deterministic entrypoint to point evidence
at. It performs no network or external calls.
"""

from __future__ import annotations

from app.routes.payments import create_payment


def handle_create_payment(payload: dict) -> tuple[int, dict]:
    """Thin entrypoint the demo 'API' uses to create a payment."""
    return create_payment(payload)


if __name__ == "__main__":
    status_code, body = handle_create_payment({"payment_id": "pay_123"})
    print(status_code, body)
