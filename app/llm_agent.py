
import json
import requests
from app.security import secure_read_ticket

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen2.5:3b"


def plan_agent_action(user_request: str):
    """Use the local LLM to propose an action."""

    system_prompt = """
You are an action planner for AEGIS.

You do not have access to customer tickets.
Never invent customer details.
Never claim that an action has been executed.

Choose exactly one action:
- read_ticket
- send_email
- unsupported

Return only a JSON object with these fields:
{
    "action": "read_ticket",
    "ticket_id": 105,
    "recipient": null
}

For send_email, provide a ticket_id and recipient.
For unsupported requests, set action to unsupported,
ticket_id to null, and recipient to null.

Do not include explanations or markdown.
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

def execute_agent_request(user_request: str):
    """
    Plan an action with the LLM, validate its structure,
    and execute only through the AEGIS security gateway.
    """

    try:
        proposal = plan_agent_action(user_request)
    except (requests.RequestException, ValueError, KeyError) as error:
        return {
            "allowed": False,
            "reason": f"LLM planning failed: {error}"
        }

    if not isinstance(proposal, dict):
        return {
            "allowed": False,
            "reason": "Invalid LLM action proposal"
        }

    action = proposal.get("action")
    ticket_id = proposal.get("ticket_id")

    # Validate the action and ticket ID
    if action != "read_ticket":
        return {
            "allowed": False,
            "reason": "Action not supported by this executor"
        }

    if type(ticket_id) is not int:
        return {
            "allowed": False,
            "reason": "Invalid ticket ID"
        }

    # The LLM cannot bypass the security gateway
    result = secure_read_ticket(ticket_id)

    return {
        "proposal": proposal,
        "allowed": result["allowed"],
        "result": result.get("data"),
        "reason": result.get("reason")
    }
