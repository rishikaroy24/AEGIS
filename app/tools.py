
# Synthetic customer-support records


# Synthetic customer-support records
# All customers and scenarios are fictional.

tickets = {
    101: {
        "customer": "Alice",
        "issue": "Order not delivered",
        "status": "open"
    },
    102: {
        "customer": "Bob",
        "issue": "Received damaged product",
        "status": "pending"
    },
    103: {
        "customer": "Charlie",
        "issue": "Refund not processed",
        "status": "closed"
    },
    104: {
        "customer": "Diana",
        "issue": "Incorrect item delivered",
        "status": "open"
    },
    105: {
        "customer": "Ethan",
        "issue": "Delivery delayed",
        "status": "pending"
    },
    106: {
        "customer": "Fiona",
        "issue": "Duplicate payment charged",
        "status": "open"
    },
    107: {
        "customer": "George",
        "issue": "Unable to track shipment",
        "status": "closed"
    },
    108: {
        "customer": "Hannah",
        "issue": "Replacement request",
        "status": "pending"
    },
    109: {
        "customer": "Isaac",
        "issue": "Warranty claim rejected",
        "status": "open"
    },
    110: {
        "customer": "Julia",
        "issue": "Missing item from order",
        "status": "pending"
    },
    111: {
        "customer": "Kevin",
        "issue": "Subscription cancellation",
        "status": "closed"
    },
    112: {
        "customer": "Luna",
        "issue": "Incorrect billing amount",
        "status": "open"
    },
    113: {
        "customer": "Mason",
        "issue": "Account access problem",
        "status": "pending"
    },
    114: {
        "customer": "Nora",
        "issue": "Refund request for cancelled order",
        "status": "open"
    },
    115: {
        "customer": "Oliver",
        "issue": "Package marked delivered but missing",
        "status": "pending"
    }
}


def read_ticket(ticket_id: int):
    """Retrieve a customer-support ticket."""
    return tickets.get(
        ticket_id,
        {"error": "Ticket not found"}
    )


# Simulated email outbox
sent_emails = []


def send_email(recipient: str, subject: str, body: str):
    """Simulate sending an email without using a real service."""

    email = {
        "recipient": recipient,
        "subject": subject,
        "body": body,
        "status": "sent"
    }

    sent_emails.append(email)

    return email
