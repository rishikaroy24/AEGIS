from app.tools import tickets
from fastapi import FastAPI
from fastapi import HTTPException
from app.security import secure_read_ticket
from app.agent import run_agent
from app.security import get_activity_logs
from app.security import ALLOWED_TICKETS
from pydantic import BaseModel
from app.security import secure_send_email
from app.security import workflow_read, workflow_send
from app.llm_agent import execute_agent_request

app = FastAPI(
    title="AEGIS",
    description="Lightweight Security Gateway for AI Agents",
    version="0.1.0"
)

@app.get("/")
def home():
    return {
        "project": "AEGIS",
        "status": "running",
        "message": "Backend initialized successfully"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/tickets")
def list_tickets():
    """Return safe metadata for the Ticket Explorer."""

    ticket_list = []

    for ticket_id, ticket in sorted(tickets.items()):
        authorized = ticket_id in ALLOWED_TICKETS

        ticket_info = {
            "ticket_id": ticket_id,
            "status": ticket["status"],
            "access": (
                "AUTHORIZED" if authorized else "RESTRICTED"
            )
        }

        if authorized:
            ticket_info["customer"] = ticket["customer"]
            ticket_info["issue"] = ticket["issue"]
        else:
            ticket_info["customer"] = "REDACTED"
            ticket_info["issue"] = "REDACTED"

        ticket_list.append(ticket_info)

    return {
        "total_tickets": len(ticket_list),
        "authorized": sum(
            ticket["access"] == "AUTHORIZED"
            for ticket in ticket_list
        ),
        "restricted": sum(
            ticket["access"] == "RESTRICTED"
            for ticket in ticket_list
        ),
        "tickets": ticket_list
    }

@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):
    result = secure_read_ticket(ticket_id)

    if not result["allowed"]:
        raise HTTPException(
            status_code=403,
            detail=result["reason"]
        )

    return result["data"]


@app.get("/agent/{ticket_id}")
def agent_endpoint(ticket_id: int):
    return run_agent(ticket_id)


@app.get("/logs")
def view_logs():
    return {
        "total_events": len(get_activity_logs()),
        "events": get_activity_logs()
    }



class EmailRequest(BaseModel):
    recipient: str
    subject: str
    body: str


@app.post("/email")
def email_endpoint(request: EmailRequest):

    result = secure_send_email(
        recipient=request.recipient,
        subject=request.subject,
        body=request.body
    )

    if not result["allowed"]:
        raise HTTPException(
            status_code=403,
            detail=result["reason"]
        )

    return result["data"]


class WorkflowReadRequest(BaseModel):
    workflow_id: str
    ticket_id: int


class WorkflowSendRequest(BaseModel):
    workflow_id: str
    ticket_id: int
    recipient: str


@app.post("/workflow/read")
def workflow_read_endpoint(request: WorkflowReadRequest):

    result = workflow_read(
        request.workflow_id,
        request.ticket_id
    )

    if not result["allowed"]:
        raise HTTPException(
            status_code=403,
            detail=result["reason"]
        )

    return result["data"]


@app.post("/workflow/send")
def workflow_send_endpoint(request: WorkflowSendRequest):

    result = workflow_send(
        request.workflow_id,
        request.ticket_id,
        request.recipient
    )

    if not result["allowed"]:
        raise HTTPException(
            status_code=403,
            detail=result["reason"]
        )

    return result["data"]


# -----------------------------------------
# LLM-powered Agent Endpoint
# -----------------------------------------

class AgentRequest(BaseModel):
    prompt: str


@app.post("/llm/execute")
def llm_execute_endpoint(request: AgentRequest):
    """Execute an LLM-proposed action through AEGIS."""

    return execute_agent_request(request.prompt)
