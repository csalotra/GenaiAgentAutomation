from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.models import ExtractedEmail

client = TestClient(app)


@patch("app.main.agent.invoke")
def test_email_webhook_sales(mock_invoke):
    mock_invoke.return_value = {
        "decision": "sales",
        "extracted": ExtractedEmail(
            intent="sales",
            contact_email="buyer@acme.com",
            company="Acme",
            priority="high",
            summary="Interested in pricing"
        ),
        "hubspot_result": {"status": "created"},
        "log_result": None
    }

    payload = {
        "id": "1",
        "from_email": "buyer@acme.com",
        "subject": "Pricing",
        "body": "Please send pricing details"
    }

    response = client.post("/webhook/email", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "processed"
    assert data["decision"] == "sales"
    assert data["hubspot"]["status"] == "created"


@patch("app.main.agent.invoke")
def test_email_webhook_non_sales(mock_invoke):
    mock_invoke.return_value = {
        "decision": "non_sales",
        "extracted": ExtractedEmail(
            intent="support",
            contact_email="user@company.com",
            company="",
            priority="medium",
            summary="Support needed"
        ),
        "hubspot_result": None,
        "log_result": {"status": "logged for records"}
    }

    payload = {
        "id": "2",
        "from_email": "user@company.com",
        "subject": "Help",
        "body": "App not working"
    }

    response = client.post("/webhook/email", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["decision"] == "non_sales"
    assert data["log"]["status"] == "logged for records"
