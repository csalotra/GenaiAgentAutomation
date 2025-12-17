# tests/reference/test_email_reference.py
from app.agent_graph import build_graph
from app.models import EmailIn, ExtractedEmail

# Reference Cases (Ground Truths)
REFERENCE_CASES = [
    # Sales emails
    {
        "name": "sales_email_1",
        "input": EmailIn(
            id="1",
            from_email="buyer1@acme.com",
            subject="Pricing Inquiry",
            body="Hi, we are interested in pricing of your product."
        ),
        "expected": {
            "intent": "sales",
            "decision": "sales",
            "crm_update": True
        }
    },
    {
        "name": "sales_email_2",
        "input": EmailIn(
            id="2",
            from_email="buyer2@startup.com",
            subject="Bulk order request",
            body="We want to buy 100 units of your service next month."
        ),
        "expected": {
            "intent": "sales",
            "decision": "sales",
            "crm_update": True
        }
    },
    {
        "name": "sales_email_3",
        "input": EmailIn(
            id="3",
            from_email="partner@enterprise.com",
            subject="Partnership proposal",
            body="We are interested in a long-term partnership with your company."
        ),
        "expected": {
            "intent": "sales",
            "decision": "sales",
            "crm_update": True
        }
    },

    # Non-sales emails
    {
        "name": "support_email_1",
        "input": EmailIn(
            id="4",
            from_email="user1@company.com",
            subject="App issue",
            body="I am facing an issue with your app. Please help."
        ),
        "expected": {
            "intent": "support",
            "decision": "non_sales",
            "crm_update": False
        }
    },
    {
        "name": "invoice_email_1",
        "input": EmailIn(
            id="5",
            from_email="finance@client.com",
            subject="Invoice question",
            body="Can you provide the invoice for last month's subscription?"
        ),
        "expected": {
            "intent": "invoice",
            "decision": "non_sales",
            "crm_update": False
        }
    },
    {
        "name": "general_email_1",
        "input": EmailIn(
            id="6",
            from_email="info@random.com",
            subject="Just saying hello",
            body="Hello, just wanted to reach out and say hi!"
        ),
        "expected": {
            "intent": "general",
            "decision": "non_sales",
            "crm_update": False
        }
    },
]

# Reference Test
def test_email_reference_cases():
    agent = build_graph()

    for case in REFERENCE_CASES:
        result = agent.invoke({
            "email_payload": case["input"],
            "extracted": None,
            "decision": None,
            "hubspot_result": None,
            "log_result": None
        })

        expected = case["expected"]

        # Assert intent
        assert result["extracted"].intent == expected["intent"], f"{case['name']} intent mismatch"

        # Assert decision routing
        assert result["decision"] == expected["decision"], f"{case['name']} decision mismatch"

        # Assert CRM update if expected
        if expected["crm_update"]:
            assert result["hubspot_result"] is not None, f"{case['name']} expected CRM update"
        else:
            assert result["hubspot_result"] is None, f"{case['name']} should not update CRM"
