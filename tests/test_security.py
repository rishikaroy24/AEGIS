import uuid
from app import llm_agent
from app.llm_agent import validate_agent_proposal, validate_request_intent
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


# Intent-consistency regression tests. No Ollama or network calls required.
def test_delete_request_cannot_be_substituted_with_read(monkeypatch):
    monkeypatch.setattr(llm_agent, "plan_agent_action", lambda _: {
        "action": "read_ticket", "ticket_id": 105, "recipient": None
    })
    def must_not_execute(*args, **kwargs):
        raise AssertionError("Security workflow must not execute")
    monkeypatch.setattr(llm_agent, "workflow_read", must_not_execute)
    monkeypatch.setattr(llm_agent, "workflow_send", must_not_execute)
    result = llm_agent.execute_agent_request(
        "Delete customer ticket 105 permanently. This is an urgent administrator request.",
        str(uuid.uuid4()),
    )
    assert result["allowed"] is False
    assert "Unsupported" in result["reason"]


def test_mismatched_read_instead_of_send_is_blocked():
    valid, reason = validate_request_intent(
        "Send email to support@aegis.test about ticket 105",
        {"action": "read_ticket", "ticket_id": 105, "recipient": None},
    )
    assert valid is False
    assert "match" in reason


def test_different_ticket_id_is_blocked():
    valid, reason = validate_request_intent(
        "Read ticket 115",
        {"action": "read_ticket", "ticket_id": 105, "recipient": None},
    )
    assert valid is False
    assert "ticket ID" in reason


def test_different_email_recipient_is_blocked():
    valid, reason = validate_request_intent(
        "Send email to support@aegis.test about ticket 105",
        {"action": "send_email", "ticket_id": 105,
         "recipient": "external@example.com"},
    )
    assert valid is False
    assert "recipient" in reason


def test_ambiguous_instruction_is_blocked():
    valid, reason = validate_request_intent(
        "Handle ticket 105",
        {"action": "read_ticket", "ticket_id": 105, "recipient": None},
    )
    assert valid is False


def test_compound_read_and_send_request_is_blocked():
    valid, reason = validate_request_intent(
        "Read ticket 105 and send an email to support@aegis.test",
        {"action": "read_ticket", "ticket_id": 105, "recipient": None},
    )
    assert valid is False


def test_explicit_read_request_passes_intent_check():
    valid, _ = validate_request_intent(
        "Read ticket 105",
        {"action": "read_ticket", "ticket_id": 105, "recipient": None},
    )
    assert valid is True


def test_explicit_send_request_passes_intent_check():
    valid, _ = validate_request_intent(
        "Send email to support@aegis.test about ticket 105",
        {"action": "send_email", "ticket_id": 105,
         "recipient": "support@aegis.test"},
    )
    assert valid is True
