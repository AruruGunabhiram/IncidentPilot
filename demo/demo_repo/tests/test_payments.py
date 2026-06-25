from app.routes.payments import create_payment


def test_create_payment_returns_created():
    status_code, body = create_payment({"payment_id": "pay_123"})

    assert status_code == 201
    assert body["payment_id"] == "pay_123"
