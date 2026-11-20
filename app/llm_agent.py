
import json
import requests

from app.security import secure_read_ticket


OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen2.5:3b"

ALLOWED_ACTIONS = {
    "read_ticket",
    "send_email",
    "unsupported"
}


def plan_agent_action(user_request: str):
    """Ask the local LLM to propose an action."""

    system_prompt = """
You are an action planner for AEGIS.

You do not have access to customer tickets.
Never invent customer details.
Never claim an action has been executed.

Choose exactly one action:
- read_ticket
- send_email
- unsupported

Return only a JSON object with exactly these fields:
{
    "action": "read_ticket",
    "ticket_id": 105,
    "recipient": null
}

Rules:
1. For read_ticket, provide a ticket_id.
2. For send_email, provide a ticket_id and recipient.
3. For unsupported, set ticket_id and recipient to null.
4. Never invent a ticket ID or email recipient.
5. Never include explanations or markdown.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "stream": False,
            "format": "json",
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_request
                }
            ],
            "options": {
                "temperature": 0
            }
        },
        timeout=120
    )

    response.raise_for_status()

    content = response.json()["message"]["content"]

    return json.loads(content)


def validate_agent_proposal(proposal):
    """
    Validate the LLM's proposed action.
    Never trust the LLM's output directly.
    """

    if not isinstance(proposal, dict):
        return False, "Invalid action proposal"

    required_fields = {
        "action",
        "ticket_id",
        "recipient"
    }

    if set(proposal.keys()) != required_fields:
        return False, "Invalid proposal structure"

    action = proposal["action"]
    ticket_id = proposal["ticket_id"]
    recipient = proposal["recipient"]

    if action not in ALLOWED_ACTIONS:
        return False, "Unknown action"

    if action == "unsupported":
        if ticket_id is not None or recipient is not None:
            return False, "Invalid unsupported action"
        return True, "Unsupported action recognized"

    if type(ticket_id) is not int or ticket_id <= 0:
        return False, "Invalid ticket ID"

    if action == "read_ticket":
        if recipient is not None:
            return False, "Unexpected recipient"
        return True, "Valid read request"

    if action == "send_email":
        if not isinstance(recipient, str):
            return False, "Invalid recipient"

        if not recipient.strip() or "@" not in recipient:
            return False, "Invalid email address"

        return True, "Valid email action proposal"

    return False, "Invalid action"


def execute_agent_request(user_request: str):
    """
    Plan, validate and execute an action
    exclusively through the AEGIS security gateway.
    """

    try:
        proposal = plan_agent_action(user_request)

    except (
        requests.RequestException,
        ValueError,
        KeyError,
        TypeError
    ) as error:
        return {
            "allowed": False,
            "reason": f"LLM planning failed: {error}"
        }

    valid, validation_reason = validate_agent_proposal(
        proposal
    )

    if not valid:
        return {
            "proposal": proposal,
            "allowed": False,
            "reason": validation_reason
        }

    action = proposal["action"]
    ticket_id = proposal["ticket_id"]

    # Unsupported actions are denied safely
    if action == "unsupported":
        return {
            "proposal": proposal,
            "allowed": False,
            "reason": "Requested action is unsupported"
        }

    # Ticket access always passes through AEGIS
    if action == "read_ticket":

        result = secure_read_ticket(ticket_id)

        return {
            "proposal": proposal,
            "allowed": result["allowed"],
            "result": result.get("data"),
            "reason": result.get("reason")
        }

    # Email execution remains blocked until
    # the secure email gateway is integrated
    if action == "send_email":

        return {
            "proposal": proposal,
            "allowed": False,
            "reason": (
                "Email execution requires "
                "the AEGIS secure email gateway"
            )
        }

    return {
        "proposal": proposal,
        "allowed": False,
        "reason": "Action denied"
    }
