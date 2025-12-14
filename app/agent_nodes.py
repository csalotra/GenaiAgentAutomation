from app.agent_state import AgentState
from app.gemini_client import extract_email_info
from app.hubspot_client import create_or_update_contact

#Node 1: Extract info
def extract_node(state: AgentState) -> AgentState:

  extracted = extract_email_info(state["email_payload"])
  state["extracted"] = extracted
  return state

#Node 2: Decide + act
def decision_node(state: AgentState) -> AgentState:
  extracted = state["extracted"]

  if extracted and extracted.intent == "sales":
    state["decision"] = "sales"
  else:
    state["decision"] = "non_sales"

  return state

#Node 3: Create contact in the Hubspot CRM 
def sales_node(state: AgentState) -> AgentState:
  extracted = state["extracted"]

  result = create_or_update_contact(
    email = extracted.contact_email,
    company = extracted.company
  )

  state["hubspot_result"] = result
  return state

#Node 4: If other than sales email, log the results
def non_sales_node(state:AgentState) -> AgentState:
  extracted = state["extracted"]

  state["log_result"] = {
    "status":"logged for records",
    "intent": extracted.intent,
    "summary":extracted.summary
  }

  return state