
from datetime import datetime, timezone
from app.tools import read_ticket, send_email


# Tickets accessible to the support agent
ALLOWED_TICKETS = set(range(101, 111))

# Tickets 111–115 remain restricted


# Stores security events while the server is running
activity_logs = []


# Track tickets accessed within each workflow
workflow_history = {}


def track_ticket_access(workflow_id: str, ticket_id: int):
    """Record a ticket after authorized access."""

    if workflow_id not in workflow_history:
        workflow_history[workflow_id] = set()

    workflow_history[workflow_id].add(ticket_id)




def secure_read_ticket(ticket_id: int):
    allowed = ticket_id in ALLOWED_TICKETS

    if not allowed:
        activity_logs.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": "read_ticket",
            "ticket_id": ticket_id,
            "decision": "BLOCKED",
            "reason": "Ticket outside authorized scope"
        })

        return {
            "allowed": False,
            "reason": "Access denied by AEGIS policy"
        }

    ticket = read_ticket(ticket_id)

    if "error" in ticket:
        return {
            "allowed": False,
            "reason": "Ticket not found"
        }

    activity_logs.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": "read_ticket",
        "ticket_id": ticket_id,
        "decision": "ALLOWED",
        "reason": "Ticket access permitted"
    })

    return {
        "allowed": True,
        "data": ticket
    }



def get_activity_logs():
    return activity_logs


def secure_send_email(
    recipient: str,
    subject: str,
    body: str
):
    """Check email permissions before executing the tool."""

    approved_recipients = {
        "support@aegis.test",
        "manager@aegis.test"
    }

    # Normalize the address for comparison
    recipient = recipient.strip().lower()

    allowed = recipient in approved_recipients

    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": "send_email",
        "recipient": recipient,
        "decision": "ALLOWED" if allowed else "BLOCKED",
        "reason": (
            "Recipient is authorized"
            if allowed
            else "Unauthorized email recipient"
        )
    }

    activity_logs.append(log_entry)

    if not allowed:
        return {
            "allowed": False,
            "reason": "AEGIS blocked an unauthorized email"
        }

    return {
        "allowed": True,
        "data": send_email(recipient, subject, body)
    }
    

def workflow_read(workflow_id: str, ticket_id: int):
    """Read a ticket and record successful access."""

    result = secure_read_ticket(ticket_id)

    if not result["allowed"]:
        return result

    if "error" in result["data"]:
        return {
            "allowed": False,
            "reason": "Ticket not found"
        }

    track_ticket_access(workflow_id, ticket_id)

    return result


def workflow_send(
    workflow_id: str,
    ticket_id: int,
    recipient: str
):
    """Send a summary only after an authorized read."""

    accessed = workflow_history.get(workflow_id, set())

    if ticket_id not in accessed:
        activity_logs.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": "workflow_send",
            "ticket_id": ticket_id,
            "decision": "BLOCKED",
            "reason": "Ticket not previously accessed"
        })

        return {
            "allowed": False,
            "reason": "Read the ticket first"
        }

    # Recheck ticket permissions
    if ticket_id not in ALLOWED_TICKETS:
        return {
            "allowed": False,
            "reason": "Ticket access revoked"
        }

    ticket = read_ticket(ticket_id)

    if "error" in ticket:
        return {
            "allowed": False,
            "reason": "Ticket not found"
        }

    subject = f"Ticket {ticket_id} Summary"

    body = (
        f"Customer {ticket['customer']} reported: "
        f"{ticket['issue']}."
    )

    return secure_send_email(recipient, subject, body)
