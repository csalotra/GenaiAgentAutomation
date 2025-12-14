from typing import Optional, TypedDict, Literal
from app.models import ExtractedEmail, EmailIn

class AgentState(TypedDict):
  email_payload: Optional[EmailIn]
  extracted: Optional[ExtractedEmail]
  decision: Optional[Literal["sales", "non_sales"]]
  hubspot_result: Optional[dict]
  log_result: Optional[dict]
