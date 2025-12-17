from unittest.mock import patch
from app.agent_nodes import extract_node, decision_node, sales_node, non_sales_node
from app.models import ExtractedEmail, EmailIn

@patch("app.agent_nodes.extract_email_info")
def test_extract_node_sets_extracted(mock_extract):
    mock_extract.return_value = ExtractedEmail(
        intent="sales",
        contact_email="a@b.com",
        company="Acme",
        priority="high",
        summary="Sales inquiry"
    )

    state = {
        "email_payload": EmailIn(
            id="1",
            from_email="a@b.com",
            subject="Pricing",
            body="Need pricing"
        ),
        "extracted": None,
        "decision": None,
        "hubspot_result": None,
        "log_result": None
    }

    result = extract_node(state)
    assert result["extracted"] is not None
    assert result["extracted"].intent == "sales"


def test_decision_node_sales():
    state = {
        "email_payload": None,
        "extracted": ExtractedEmail(
            intent="sales",
            contact_email="a@b.com",
            company="Acme",
            priority="high",
            summary="Sales inquiry"
        ),
        "decision": None,
        "hubspot_result": None,
        "log_result": None
    }

    result = decision_node(state)
    assert result["decision"] == "sales"


def test_decision_node_non_sales():
    state = {
        "email_payload": None,
        "extracted": ExtractedEmail(
            intent="support",
            contact_email="a@b.com",
            company="",
            priority="medium",
            summary="Support request"
        ),
        "decision": None,
        "hubspot_result": None,
        "log_result": None
    }

    result = decision_node(state)
    assert result["decision"] == "non_sales"


@patch("app.agent_nodes.create_or_update_contact")
def test_sales_node_calls_hubspot(mock_hubspot):
    mock_hubspot.return_value = {"status": "created"}

    state = {
        "email_payload": None,
        "extracted": ExtractedEmail(
            intent="sales",
            contact_email="a@b.com",
            company="Acme",
            priority="high",
            summary="Sales inquiry"
        ),
        "decision": "sales",
        "hubspot_result": None,
        "log_result": None
    }

    result = sales_node(state)
    mock_hubspot.assert_called_once_with(email="a@b.com", company="Acme")
    assert result["hubspot_result"]["status"] == "created"


def test_non_sales_node_logs():
    state = {
        "email_payload": None,
        "extracted": ExtractedEmail(
            intent="support",
            contact_email="a@b.com",
            company="",
            priority="medium",
            summary="Support request"
        ),
        "decision": "non_sales",
        "hubspot_result": None,
        "log_result": None
    }

    result = non_sales_node(state)
    assert result["log_result"]["status"] == "logged for records"
    assert result["log_result"]["intent"] == "support"
