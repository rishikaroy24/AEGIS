import uuid
from app.llm_agent import validate_agent_proposal
from app.security import (
    secure_read_ticket,
    workflow_read,
    workflow_send
)


def test_restricted_ticket_access():
    result = secure_read_ticket(115)

    assert result["allowed"] is False
    assert result.get("data") is None
    
def test_authorized_ticket_access():
    result = secure_read_ticket(105)

    assert result["allowed"] is True
    assert result.get("data") is not None


def test_another_restricted_ticket():
    result = secure_read_ticket(111)

    assert result["allowed"] is False
    assert result.get("data") is None


def test_email_without_read():
    workflow_id = str(uuid.uuid4())

    result = workflow_send(
        workflow_id,
        105,
        "support@aegis.test"
    )

    assert result["allowed"] is False
    assert result.get("reason") is not None


def test_email_after_read():
    workflow_id = str(uuid.uuid4())

    read_result = workflow_read(
        workflow_id,
        105
    )

    assert read_result["allowed"] is True

    send_result = workflow_send(
        workflow_id,
        105,
        "support@aegis.test"
    )

    assert send_result["allowed"] is True


def test_workflow_isolation():
    workflow_a = str(uuid.uuid4())
    workflow_b = str(uuid.uuid4())

    read_result = workflow_read(
        workflow_a,
        105
    )

    assert read_result["allowed"] is True

    send_result = workflow_send(
        workflow_b,
        105,
        "support@aegis.test"
    )

    assert send_result["allowed"] is False


def test_unauthorized_email_recipient():
    workflow_id = str(uuid.uuid4())

    read_result = workflow_read(workflow_id, 105)
    assert read_result["allowed"] is True

    send_result = workflow_send(
        workflow_id,
        105,
        "external@example.com"
    )

    assert send_result["allowed"] is False
    assert send_result.get("data") is None


def test_restricted_ticket_cannot_enable_email():
    workflow_id = str(uuid.uuid4())

    read_result = workflow_read(workflow_id, 115)

    assert read_result["allowed"] is False

    send_result = workflow_send(
        workflow_id,
        115,
        "support@aegis.test"
    )

    assert send_result["allowed"] is False
    assert send_result.get("data") is None


def test_unknown_llm_action():
    proposal = {
        "action": "delete_ticket",
        "ticket_id": 105,
        "recipient": None
    }

    valid, reason = validate_agent_proposal(proposal)

    assert valid is False


def test_invalid_llm_ticket_id():
    proposal = {
        "action": "read_ticket",
        "ticket_id": "105",
        "recipient": None
    }

    valid, reason = validate_agent_proposal(proposal)

    assert valid is False


def test_extra_llm_parameters():
    proposal = {
        "action": "read_ticket",
        "ticket_id": 105,
        "recipient": None,
        "admin_override": True
    }

    valid, reason = validate_agent_proposal(proposal)

    assert valid is False
