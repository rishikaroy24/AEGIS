
from app.security import secure_read_ticket


def run_agent(ticket_id: int):
    result = secure_read_ticket(ticket_id)

    if not result["allowed"]:
        return {
            "ticket_id": ticket_id,
            "status": "blocked",
            "reason": result["reason"]
        }

    ticket = result["data"]

    if "error" in ticket:
        return {"error": "Ticket not found"}

    response = (
        f"Customer {ticket['customer']} reported: "
        f"{ticket['issue']}. "
        f"Current status: {ticket['status']}."
    )

    return {
        "ticket_id": ticket_id,
        "status": "allowed",
        "agent_response": response
    }
