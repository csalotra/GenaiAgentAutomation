from unittest.mock import patch
from app.agent_graph import build_graph
from app.models import EmailIn, ExtractedEmail


@patch("app.agent_nodes.extract_email_info")
@patch("app.agent_nodes.create_or_update_contact")
def test_sales_email_full_workflow(mock_hubspot, mock_extract):
    """
    extract -> decision -> sales_node
    """

    mock_extract.return_value = ExtractedEmail(
        intent="sales",
        contact_email="buyer@acme.com",
        company="Acme",
        priority="high",
        summary="Interested in pricing"
    )

    mock_hubspot.return_value = {"status": "created"}

    agent = build_graph()

    result = agent.invoke({
        "email_payload": EmailIn(
            id="1",
            from_email="buyer@acme.com",
            subject="Pricing",
            body="Please share pricing details"
        ),
        "extracted": None,
        "decision": None,
        "hubspot_result": None,
        "log_result": None
    })

    assert result["decision"] == "sales"
    assert result["hubspot_result"]["status"] == "created"
    mock_hubspot.assert_called_once()


@patch("app.agent_nodes.extract_email_info")
def test_non_sales_email_full_workflow(mock_extract):
    """
    extract -> decision -> non_sales_node
    """

    mock_extract.return_value = ExtractedEmail(
        intent="support",
        contact_email="user@company.com",
        company="",
        priority="medium",
        summary="Need help"
    )

    agent = build_graph()

    result = agent.invoke({
        "email_payload": EmailIn(
            id="2",
            from_email="user@company.com",
            subject="Issue",
            body="App is not working"
        ),
        "extracted": None,
        "decision": None,
        "hubspot_result": None,
        "log_result": None
    })

    assert result["decision"] == "non_sales"
    assert result["log_result"]["status"] == "logged for records"
