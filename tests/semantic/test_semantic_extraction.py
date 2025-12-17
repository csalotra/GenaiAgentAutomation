from app.agent_graph import build_graph
from app.models import EmailIn, ExtractedEmail
from google import genai
import numpy as np

client = genai.Client()

# Semantic Test Cases
SEMANTIC_CASES = [
    {
        "name": "support_email_1",
        "input": EmailIn(
            id="1",
            from_email="user@company.com",
            subject="Login issue",
            body="I can't log in to the app."
        ),
        "reference_summary": "User cannot log in to the application.",
        "expected_intent": "support"
    },
    {
        "name": "sales_email_1",
        "input": EmailIn(
            id="2",
            from_email="buyer@acme.com",
            subject="Pricing inquiry",
            body="We want pricing details for your product."
        ),
        "reference_summary": "Customer wants details about product pricing.",
        "expected_intent": "sales"
    },
    {
        "name": "invoice_email_1",
        "input": EmailIn(
            id="3",
            from_email="finance@client.com",
            subject="Invoice question",
            body="Can you provide last month's invoice?"
        ),
        "reference_summary": "Client requests last month's invoice.",
        "expected_intent": "invoice"
    }
]

def get_embedding_google(text: str):
    response = client.models.embed_content(
      model="gemini-embedding-001",
      contents=text
    )
    # Convert embedding list to numpy array
    return np.array(response.embeddings[0].values)


def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


# Semantic Test Function
def test_semantic_embeddings():
    agent = build_graph()
    threshold = 0.8  # similarity threshold to pass semantic test

    for case in SEMANTIC_CASES:
        result = agent.invoke({
            "email_payload": case["input"],
            "extracted": None,
            "decision": None,
            "hubspot_result": None,
            "log_result": None
        })

        extracted: ExtractedEmail = result["extracted"]

        #Intent match
        assert extracted.intent == case["expected_intent"], f"{case['name']} intent mismatch"

        #Semantic similarity
        generated_embedding = get_embedding_google(extracted.summary)
        reference_embedding = get_embedding_google(case["reference_summary"])
        similarity = cosine_similarity(generated_embedding, reference_embedding)
        assert similarity >= threshold, f"{case['name']} semantic similarity too low: {similarity:.2f}"

