from fastapi import FastAPI
from dotenv import load_dotenv
from app.models import EmailIn
from app.agent_graph import build_graph
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(title = "GenAI Agent Automation")

agent = build_graph()

@app.get("/")
def root():
  return {"status":"ok", "service":"genai-agent-automation"}

@app.post("/webhook/email")
async def receive_email(payload: EmailIn):
  try:
    result = agent.invoke({
        "email_payload": payload,
        "extracted": None,
        "decision": None,
        "hubspot_result": None,
        "log_result": None
    })

    return {
        "status": "processed",
        "email_id": payload.id,
        "decision": result["decision"],
        "extracted": result["extracted"].model_dump(),
        "hubspot": result["hubspot_result"],
        "log": result["log_result"]
    }
  
  except Exception as e:

    logger.exception(f"Failed processing email ID {payload.id}")

    return {
      "status": "failed",
      "email_id": payload.id,
      "error": "Internal processing error"
    }

