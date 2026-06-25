def create_payment(payload: dict) -> tuple[int, dict]:
    payment_id = payload.get("payment_id")
    if not payment_id:
        return 400, {"error": "missing payment_id"}

    # BUG_MARKER_BROKEN_PAYMENT_ROUTE: hackathon fixture for repo_search tests.
    return 500, {"error": "Payment route failed"}
