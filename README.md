# GenaiAgentAutomation
Multi-step Generative AI agent that automates email processing and HubSpot CRM updates using LangGraph and Google Gemini. FastAPI webhook-based architecture with conditional workflows.
# GenAI Agent Automation

A multi-step Generative AI agent that automates email processing and CRM updates using LangGraph, Google Gemini LLM, and HubSpot.

---
## Features

- **Email Ingestion**: Accepts email payloads via a FastAPI webhook.
- **Information Extraction**: Uses Google Gemini to extract structured information (intent, contact email, company, priority, summary).
- **Conditional Workflow**: LangGraph orchestrates multi-step workflow:
  - Sales emails → HubSpot CRM contact creation
  - Non-sales emails → Logging for records
- **Secure Integration**: HubSpot API integration with proper scopes and token management.
- **Error Handling**: Logs internal errors; returns safe messages to clients.
- **Extensible**: Easy to add additional nodes for notifications, approvals, or retries.

---

## Tech Stack

- **FastAPI** – Web framework for webhook API.
- **LangGraph** – State machine for AI agent orchestration.
- **Google Gemini** – LLM for email understanding.
- **HubSpot CRM** – Contact management and automation.
- **Python 3.11+** – Core language.
- **Uvicorn** – ASGI server for FastAPI.

---

## Project Structure

app/
agent_graph.py # LangGraph workflow
agent_nodes.py # Nodes for extract, decision, action
agent_state.py # Agent state typing
gemini_client.py # Gemini extraction wrapper
hubspot_client.py # HubSpot API wrapper
models.py # Pydantic models for payloads and extracted info
main.py # FastAPI server
.env.example # Example environment variables
.gitignore
README.md
requirements.txt


---
### **Setup Instructions**

1. **Clone the repository**
```bash
git clone https://github.com/csalotra/genai-agent-automation.git
cd genai-agent-automation
```

2. **Create a virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```


3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set environment variables**
```bash
Create a .env file with your API keys:
GOOGLE_API_KEY=your_gemini_api_key
HUBSPOT_ACCESS_TOKEN=your_hubspot_token
```

5. **Run FastAPI server**
```bash
uvicorn app.main:app --reload
```
