"""AEGIS dashboard: editorial-plum UI; all actions use existing FastAPI routes."""
import html
import uuid
from pathlib import Path
from styles.theme import apply_theme, THEMES, SHIELD_SVG , show_aegis_footer
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AEGIS | Agent Security", page_icon=str(Path(__file__).resolve().parent / "assets" / "aegis-mark.png"), layout="wide", initial_sidebar_state="expanded")

# Sidebar navigation and theme selection
# Sidebar branding
logo_path = Path(__file__).resolve().parent / "assets" / "aegis-mark.png"

with st.sidebar:
    st.image(str(logo_path), width=48)

    st.markdown(
        '<div class="aegis-sideword">aegis.</div>'
        '<div class="aegis-eyebrow">CONTROL STUDIO</div>',
        unsafe_allow_html=True
    )
st.sidebar.caption("AI action governance · local demo")
st.sidebar.divider()
page = st.sidebar.radio(
    "Workspace", ["Overview", "Agent Playground", "Ticket Explorer", "Security Logs"],
    key="navigation",
)
st.sidebar.divider()
mode = st.sidebar.radio("Appearance", ["Light", "Dark"], horizontal=True, key="theme_mode")
apply_theme(mode)
theme = THEMES[mode]
st.sidebar.caption("AEGIS · Local security MVP")


def heading(kicker: str, title: str, description: str):
    st.markdown(
        f'<div class="aegis-hero aegis-entrance">'
        f'<div class="aegis-eyebrow">{html.escape(kicker)}</div>'
        f'<h1>{html.escape(title)}</h1>'
        f'<div class="aegis-tagline">{html.escape(description)}</div></div>',
        unsafe_allow_html=True,
    )


def section(title, meta=""):
    st.markdown(
        f'<div class="aegis-section"><span class="aegis-section-title">{html.escape(title)}</span>'
        f'<span class="aegis-muted">{html.escape(meta)}</span></div>',
        unsafe_allow_html=True,
    )


def mini_card(label, value, note="", tone="neutral"):
    tone = tone if tone in {'neutral', 'gold', 'rose', 'sage'} else 'neutral'
    st.markdown(
        f'<div class="aegis-mini-card aegis-mini-card--{tone} aegis-entrance">'
        f'<div class="aegis-mini-card-title">{html.escape(str(label))}</div>'
        f'<div class="aegis-mini-card-value">{html.escape(str(value))}</div>'
        f'<div class="aegis-mini-card-caption">{html.escape(str(note))}</div></div>',
        unsafe_allow_html=True,
    )


def stat_card(label, value, tone="total"):
    """Presentation-only stat card; numeric values come from the original API."""
    if tone not in {"total", "allowed", "blocked"}:
        tone = "total"
    st.markdown(
        f'<div class="aegis-stat aegis-stat--{tone}">'
        f'<div class="aegis-stat-label">{html.escape(str(label))}</div>'
        f'<div class="aegis-stat-value">{html.escape(str(value))}</div>'
        '</div>',
        unsafe_allow_html=True,
    )


def api_get(path, timeout=5):
    r = requests.get(f"{API_URL}{path}", timeout=timeout)
    r.raise_for_status()
    return r.json()


def api_post(path, data, timeout=8):
    r = requests.post(f"{API_URL}{path}", json=data, timeout=timeout)
    return r



def show_overview():

    # ==========================================
    # PAGE HEADER
    # ==========================================

    heading(
        "THE CONTROL ROOM",
        "Security, with intention.",
        "A focused workspace to observe AI agent decisions, "
        "enforce policies, and understand every permitted "
        "or blocked action."
    )

    # ==========================================
    # BACKEND HEALTH CHECK
    # ==========================================

    health_ok = False

    try:
        health_ok = (
            api_get("/health").get("status") == "healthy"
        )

    except requests.RequestException:
        pass

    # ==========================================
    # SYSTEM HEALTH & ENVIRONMENT CARDS
    # ==========================================

    status_col, environment_col = st.columns(
        2,
        gap="medium"
    )

    with status_col:

        with st.container(border=True):

            st.markdown("### System Health")
            st.caption("BACKEND CONNECTION")

            if health_ok:
                st.success("Backend operational")

            else:
                st.error("Backend unavailable")

            st.caption("FastAPI · localhost:8000")

            st.caption(
                "LLM availability is checked separately "
                "when an agent instruction is executed."
            )

    with environment_col:

        with st.container(border=True):

            st.markdown("### Environment")
            st.caption("LOCAL AI RUNTIME")

            st.markdown("**Qwen 2.5 (3B)**")
            st.caption("Local inference via Ollama")

            st.markdown("**FastAPI + Streamlit**")
            st.caption(
                "Security gateway and interactive dashboard"
            )

    # ==========================================
    # SECURITY ANALYTICS
    # ==========================================

    section(
        "Security at a glance",
        "CURRENT BACKEND LOGS"
    )

    if st.button(
        "Refresh analytics",
        key="refresh_overview"
    ):
        st.rerun()

    try:

        events = api_get("/logs").get("events", [])

        allowed = sum(
            event.get("decision") == "ALLOWED"
            for event in events
        )

        blocked = sum(
            event.get("decision") == "BLOCKED"
            for event in events
        )

        # ======================================
        # SECURITY METRIC CARDS
        # ======================================

        col1, col2, col3 = st.columns(
            3,
            gap="medium"
        )

        with col1:
            stat_card("Total events", len(events), "total")

        with col2:
            stat_card("Allowed actions", allowed, "allowed")

        with col3:
            stat_card("Blocked actions", blocked, "blocked")

        # ======================================
        # ACTIVITY AND DECISION PANELS
        # ======================================

        left, right = st.columns(
            [1, 1.25],
            gap="large"
        )

        with left:

            with st.container(border=True):

                section(
                    "Decision balance",
                    "AUDIT SNAPSHOT"
                )

                if events:

                    decision_counts = [
                        {
                            "Decision": "Allowed",
                            "Count": allowed
                        },
                        {
                            "Decision": "Blocked",
                            "Count": blocked
                        }
                    ]

                    st.bar_chart(
                        decision_counts,
                        x="Decision",
                        y="Count",
                        color=theme["accent"]
                    )

                    st.caption(
                        "Counts reflect logged security events, "
                        "not all rejected LLM proposals."
                    )

                else:

                    st.info(
                        "No security events recorded yet. "
                        "Try reading a ticket in the "
                        "Agent Playground."
                    )

        with right:

            with st.container(border=True):

                section(
                    "Latest activity",
                    "MOST RECENT 5"
                )

                if events:

                    recent_events = events[-5:][::-1]

                    # Use a read-only HTML table so all audit entries can
                    # consistently render in Times New Roman. Escape every
                    # backend-supplied value before inserting it into HTML.
                    columns = (
                        ("timestamp", "Timestamp"),
                        ("action", "Action"),
                        ("ticket_id", "Ticket ID"),
                        ("decision", "Decision"),
                        ("reason", "Reason"),
                    )
                    headers = "".join(
                        f"<th scope='col'>{html.escape(label)}</th>"
                        for _, label in columns
                    )
                    rows = []
                    for event in recent_events:
                        cells = "".join(
                            f"<td>{html.escape(str(event.get(key) if event.get(key) is not None else '—'))}</td>"
                            for key, _ in columns
                        )
                        rows.append(f"<tr>{cells}</tr>")
                    st.markdown(
                        """<style>
                        .aegis-activity-scroll {
                            overflow-x: auto; max-width: 100%;
                            border-radius: 12px;
                            border: 1px solid rgba(120, 76, 63, .20);
                        }
                        .aegis-activity-table {
                            border-collapse: collapse;
                            width: 100%; min-width: 650px;
                            font-family: "Times New Roman", Times, serif !important;
                            font-size: 1rem;
                        }
                        .aegis-activity-table th,
                        .aegis-activity-table td {
                            font-family: "Times New Roman", Times, serif !important;
                            padding: 10px 12px; text-align: left;
                            border-bottom: 1px solid rgba(120, 76, 63, .14);
                            white-space: nowrap;
                        }
                        .aegis-activity-table th {
                            background: #F7E8DF; color: #72263B;
                            font-weight: 700;
                        }
                        .aegis-activity-table td {
                            background: #FFF9F5; color: #4D2732;
                        }
                        .aegis-activity-table tbody tr:hover td {
                            background: #FFE8D2;
                        }
                        .aegis-activity-table td:last-child {
                            white-space: normal; min-width: 180px;
                        }
                        </style>"""
                        + "<div class='aegis-activity-scroll'>"
                        + "<table class='aegis-activity-table'>"
                        + "<thead><tr>" + headers + "</tr></thead>"
                        + "<tbody>" + "".join(rows) + "</tbody>"
                        + "</table></div>",
                        unsafe_allow_html=True,
                    )

                else:

                    st.caption(
                        "Security activity will appear here "
                        "once actions are evaluated."
                    )

    except requests.RequestException as error:

        st.warning(
            f"Security analytics unavailable: {error}"
        )

    # ==========================================
    # HOW AEGIS WORKS
    # ==========================================

    section(
        "How AEGIS works",
        "ONE ACTION AT A TIME"
    )

    step1, step2, step3 = st.columns(
        3,
        gap="medium"
    )

    with step1:

        mini_card(
            "01 · Propose",
            "LLM Planner",
            "Qwen converts natural-language instructions "
            "into structured action proposals.",
            tone="gold"
        )

    with step2:

        mini_card(
            "02 · Verify",
            "Policy Gateway",
            "AEGIS validates proposals and checks "
            "ticket permissions and workflow rules.",
            tone="rose"
        )

    with step3:

        mini_card(
            "03 · Record",
            "Audit Trail",
            "Gateway decisions are returned and "
            "recorded when supported by the logging system.",
            tone="sage"
        )

def show_agent_playground():
    if "workflow_id" not in st.session_state:
        st.session_state.workflow_id = str(uuid.uuid4())

    heading("INTERACTIVE LAB", "Agent Playground",
            "Explore how an AI agent proposes an action while AEGIS independently authorizes its execution.")
    tab1, tab2 = st.tabs(["AI Agent Console", "Workflow Simulator"])

    with tab1:
        section("Natural-language execution", "QWEN 2.5 · OLLAMA")
        with st.container(border=True):
            st.caption(f"Workflow  ·  {st.session_state.workflow_id}")
            prompt = st.text_area("Agent instruction", placeholder="Example: Read ticket 105", height=120, key="llm_prompt")
            execute = st.button("Evaluate with AEGIS", type="primary", use_container_width=True, key="llm_run")

        if execute:
            if not prompt.strip():
                st.warning("Enter an instruction before running the agent.")
            else:
                try:
                    with st.spinner("Qwen is generating an action proposal…"):
                        response = api_post(
                            "/llm/execute",
                            {"prompt": prompt, "workflow_id": st.session_state.workflow_id},
                            timeout=120,
                        )
                        response.raise_for_status()
                        st.session_state["last_llm_result"] = response.json()
                        st.session_state["last_llm_workflow"] = st.session_state.workflow_id
                except (requests.RequestException, ValueError) as exc:
                    st.error(f"Agent request failed: {exc}")

        if "last_llm_result" in st.session_state:
            result = st.session_state["last_llm_result"]
            proposal = result.get("proposal") or {}
            section("Proposed action", "LLM OUTPUT")
            a, b, c = st.columns(3)
            with a:
                mini_card("Action", str(proposal.get("action", "Unknown")).replace("_", " ").title(), tone="gold")
            with b:
                mini_card("Ticket", proposal.get("ticket_id") if proposal.get("ticket_id") is not None else "—", tone="rose")
            with c:
                mini_card("Recipient", proposal.get("recipient") or "—", tone="sage")
            with st.expander("Inspect full agent proposal", expanded=False):
                st.json(proposal)

            section("Security decision", "AEGIS POLICY ENGINE")
            with st.container(border=True):
                if st.session_state.get("last_llm_workflow") != st.session_state.workflow_id:
                    st.caption("This result belongs to a previous workflow.")
                if result.get("allowed"):
                    st.success("Action allowed by AEGIS")
                    if result.get("result") is not None:
                        with st.expander("Execution result", expanded=True):
                            st.json(result["result"])
                    else:
                        st.caption("No execution data was returned.")
                else:
                    st.error("Action blocked by AEGIS")
                    st.markdown(f"**Reason:** {result.get('reason') or 'Action denied'}")
                    st.caption("A denial response does not, on its own, establish a full security guarantee.")

    with tab2:
        section("Workflow simulator", "MANUAL POLICY EXERCISES")
        with st.container(border=True):
            st.caption(f"Current workflow  ·  {st.session_state.workflow_id}")
            if st.button("Start new workflow", key="workflow_new"):
                st.session_state.workflow_id = str(uuid.uuid4())
                st.session_state.pop("last_llm_result", None)
                st.rerun()
            c1, c2 = st.columns(2)
            with c1:
                ticket_id = st.selectbox("Customer ticket", list(range(101, 116)), format_func=lambda x: f"Ticket #{x}")
            with c2:
                recipient = st.selectbox("Email recipient", ["support@aegis.test", "manager@aegis.test", "external@example.com"])
            rcol, scol = st.columns(2)
            with rcol:
                read_button = st.button("Read ticket", use_container_width=True)
            with scol:
                send_button = st.button("Send simulated email", use_container_width=True)

        if read_button or send_button:
            path = "/workflow/read" if read_button else "/workflow/send"
            payload = {"workflow_id": st.session_state.workflow_id, "ticket_id": ticket_id}
            if send_button:
                payload["recipient"] = recipient
            try:
                r = api_post(path, payload)
                with st.container(border=True):
                    section("Workflow outcome", "GATEWAY RESPONSE")
                    if r.status_code == 200:
                        st.success("Action allowed")
                        st.json(r.json())
                    elif r.status_code == 403:
                        st.error("Action blocked")
                        st.write(r.json().get("detail", "Access denied"))
                    else:
                        st.warning(f"Unexpected backend response: {r.status_code}")
                        st.text(r.text[:500])
            except requests.RequestException as exc:
                st.error(f"Connection error: {exc}")


def show_ticket_explorer():
    heading("RESOURCE INVENTORY", "Ticket Explorer",
            "Search synthetic support tickets and understand which records are visible under the current policy.")
    try:
        data = api_get("/tickets")
    except requests.RequestException as exc:
        st.error(f"Unable to retrieve tickets: {exc}")
        return
    tickets = data.get("tickets", [])
    a, b, c = st.columns(3)
    with a:
        stat_card("Total tickets", data.get("total_tickets", 0), "total")
    with b:
        stat_card("Authorized", data.get("authorized", 0), "allowed")
    with c:
        stat_card("Restricted", data.get("restricted", 0), "blocked")

    section("Browse tickets", "SEARCH & FILTER")
    with st.container(border=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            search = st.text_input("Search", placeholder="ID, customer or issue…", key="ticket_search").lower()
        with c2:
            status_filter = st.selectbox("Status", ["All", "open", "pending", "closed"])
        with c3:
            access_filter = st.selectbox("Access", ["All", "AUTHORIZED", "RESTRICTED"])

    filtered = []
    for ticket in tickets:
        searchable = f"{ticket.get('ticket_id', '')} {ticket.get('customer', '')} {ticket.get('issue', '')}".lower()
        if (search in searchable and (status_filter == "All" or ticket.get("status") == status_filter)
                and (access_filter == "All" or ticket.get("access") == access_filter)):
            filtered.append(ticket)

    with st.container(border=True):
        st.caption(f"Showing {len(filtered)} of {len(tickets)} records")
        if filtered:
            # Streamlit's dataframe uses a canvas, so CSS font overrides do not
            # consistently affect its cells. Render this read-only ticket table
            # as escaped HTML to retain the desired Times New Roman typography.
            columns = (
                ("ticket_id", "Ticket ID"),
                ("status", "Status"),
                ("access", "Access"),
                ("customer", "Customer"),
                ("issue", "Issue"),
            )
            header = "".join(f"<th scope='col'>{html.escape(label)}</th>" for _, label in columns)
            rows = []
            for ticket in filtered:
                cells = "".join(
                    f"<td>{html.escape(str(ticket.get(key, '—')))}</td>"
                    for key, _ in columns
                )
                rows.append(f"<tr>{cells}</tr>")
            st.markdown(
                """<style>
                .aegis-ticket-scroll {
                    max-height: 390px; overflow: auto; width: 100%;
                    border: 1px solid rgba(120, 76, 63, .20);
                    border-radius: 12px;
                }
                .aegis-ticket-table {
                    width: 100%; border-collapse: separate; border-spacing: 0;
                    font-family: 'Times New Roman', Times, serif !important;
                    font-size: 1rem; line-height: 1.4;
                }
                .aegis-ticket-table th, .aegis-ticket-table td {
                    font-family: 'Times New Roman', Times, serif !important;
                    padding: 10px 12px; text-align: left;
                    border-right: 1px solid rgba(120, 76, 63, .12);
                    border-bottom: 1px solid rgba(120, 76, 63, .12);
                    white-space: normal;
                }
                .aegis-ticket-table th {
                    position: sticky; top: 0; z-index: 1;
                    background: #F7E8DF; color: #72263B;
                    font-weight: 700; font-size: 1.02rem;
                }
                .aegis-ticket-table td { background: #FFF9F5; color: #4D2732; }
                .aegis-ticket-table tbody tr:hover td { background: #FFE8D2; }
                .aegis-ticket-table td:first-child { text-align: right; font-weight: 700; }
                .aegis-ticket-table td:last-child { min-width: 200px; }
                .aegis-ticket-table th:last-child, .aegis-ticket-table td:last-child {
                    border-right: 0;
                }
                @media (prefers-reduced-motion: no-preference) {
                    .aegis-ticket-table td { transition: background .18s ease; }
                }
                </style>"""
                + "<div class='aegis-ticket-scroll'><table class='aegis-ticket-table'>"
                + "<thead><tr>" + header + "</tr></thead><tbody>"
                + "".join(rows) + "</tbody></table></div>",
                unsafe_allow_html=True,
            )
        else:
            st.info("No tickets match these filters.")

    section("Ticket details", "POLICY-AWARE PREVIEW")
    with st.container(border=True):
        if not filtered:
            st.caption("Choose different filters to inspect a ticket.")
            return
        selected = st.selectbox("Select a ticket", [t["ticket_id"] for t in filtered],
                                format_func=lambda x: f"Ticket #{x}")
        ticket = next(t for t in filtered if t["ticket_id"] == selected)
        if ticket.get("access") == "RESTRICTED":
            st.error("Restricted — customer details and issue text are redacted.")
        else:
            st.success("Authorized within the configured ticket scope")
            a, b, c = st.columns(3)
            with a:
                mini_card("Ticket", selected)
            with b:
                mini_card("Customer", ticket.get("customer", "—"))
            with c:
                mini_card("Status", str(ticket.get("status", "—")).title())
            st.markdown("**Issue**")
            st.write(ticket.get("issue", "—"))


def show_security_logs():
    heading("AUDIT & OBSERVABILITY", "Security Logs",
            "Trace authorization decisions and review the events that AEGIS recorded during this backend session.")
    if st.button("Refresh logs", key="refresh_logs"):
        st.rerun()
    try:
        events = api_get("/logs").get("events", [])
    except requests.RequestException as exc:
        st.error(f"Unable to retrieve logs: {exc}")
        return

    allowed = sum(e.get("decision") == "ALLOWED" for e in events)
    blocked = sum(e.get("decision") == "BLOCKED" for e in events)
    a, b, c = st.columns(3)
    with a:
        stat_card("Total events", len(events), "total")
    with b:
        stat_card("Allowed actions", allowed, "allowed")
    with c:
        stat_card("Blocked actions", blocked, "blocked")

    section("Authorization history", "IN-MEMORY AUDIT TRAIL")
    with st.container(border=True):
        if not events:
            st.info("No events yet. Run ticket actions to populate the audit trail.")
        else:
            f1, f2 = st.columns([1, 2])
            with f1:
                decision_filter = st.selectbox("Decision", ["All", "ALLOWED", "BLOCKED"])
            with f2:
                query = st.text_input("Search events", placeholder="Ticket ID, action or reason").lower()
            visible = [e for e in events if
                       (decision_filter == "All" or e.get("decision") == decision_filter) and
                       (not query or query in " ".join(str(v) for v in e.values()).lower())]
            st.caption(f"{len(visible)} matching events · newest first")
            if visible:
                st.dataframe(visible[::-1], use_container_width=True, hide_index=True)
            else:
                st.info("No events match those filters.")
            st.caption(
    "Audit events are stored in memory and reset when FastAPI restarts. "
    "Gateway decisions and instrumented LLM proposal rejections are recorded."
)


ROUTES = {
    "Overview": show_overview,
    "Agent Playground": show_agent_playground,
    "Ticket Explorer": show_ticket_explorer,
    "Security Logs": show_security_logs,
}

ROUTES[page]()

show_aegis_footer()