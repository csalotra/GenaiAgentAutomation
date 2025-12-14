from pydantic import BaseModel, EmailStr
from typing import Literal

class EmailIn(BaseModel):
  id:str
  from_email: EmailStr
  to_email :EmailStr | None = None
  subject: str | None = None
  body: str

  model_config = {"extra": "forbid"}

class ExtractedEmail(BaseModel):
  intent: Literal ["sales", "support", "invoice", "general"]
  contact_email: str
  company: str
  priority:Literal["low", "medium", "high"]
  summary: str
