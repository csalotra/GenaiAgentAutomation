import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from app.models import ExtractedEmail

load_dotenv()

genai.configure(api_key = os.getenv("GEMINI_API_KEY")) #your llm api key

model = genai.GenerativeModel("gemini-2.5-flash")

def extract_email_info(payload: dict) ->dict:

  email_text = getattr(payload, "body", "")
  from_email = getattr(payload, "from_email", "")

  prompt = f"""

You are an enterprise AI assistant.

TASK:
Extract the information from the email below:

RULES:
- Respond ONLY with valid json
- Do NOT include markdown
- Do NOT add explanations
- Follow this exact schema

SCHEMA:
{{
"intent": "sales | support | invoice | general",
"contact_email": "string",
"company": "string or empty",
"priority": "low | medium | high",
"summary": "string"
}}

Email:
\"\"\"
{email_text}
\"\"\"
"""
  response = model.generate_content(prompt)
  
  try:
    raw_text = response.text.strip()
    parsed_json = json.loads(raw_text)
    extracted =  ExtractedEmail(**parsed_json)

    if not extracted.contact_email and from_email:
      extracted.contact_email = from_email

    return extracted

  except Exception as e:
    return {"error":str(e)}