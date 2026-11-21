
import streamlit as st
import requests
from styles.theme import apply_theme, THEMES

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AEGIS Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------------------
# Mint Circuit Theme Switcher
# -----------------------------------------

st.sidebar.markdown("## 🛡️ AEGIS")
st.sidebar.caption("Security Control Center")

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Agent Playground",
        "Ticket Explorer",
        "Security Logs"
    ],
    key="navigation"
)

st.sidebar.divider()


theme_mode = st.sidebar.radio(
    "Appearance",
    options=["Light", "Dark"],
    key="theme_mode",
    horizontal=True,
)

apply_theme(theme_mode)
theme = THEMES[theme_mode]

def show_overview():
    st.title("🛡️ AEGIS")
    st.caption("Agent Execution Governance & Isolation System")

    st.divider()

    st.subheader("System Health")

    try:
        response = requests.get(
            f"{API_URL}/health",
            timeout=5
        )
        response.raise_for_status()

        if response.json().get("status") == "healthy":
            st.success(
            " AEGIS Backend Connected"
        )
        else:
            st.warning("Unexpected backend status")

    except requests.RequestException:
        st.error("Backend connection failed")

    st.divider()


    # -----------------------------------------
    # Security Analytics
    # -----------------------------------------

    st.subheader("Security Analytics")

    if st.button("Refresh Security Analytics"):
        st.rerun()

    try:
        response = requests.get(
            f"{API_URL}/logs",
            timeout=5
        )
        response.raise_for_status()

        events = response.json().get("events", [])

        allowed = sum(
            e.get("decision") == "ALLOWED"
            for e in events
        )

        blocked = sum(
            e.get("decision") == "BLOCKED"
            for e in events
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Events", len(events))
        col2.metric("Allowed Actions", allowed)
        col3.metric("Blocked Actions", blocked)

        if events:
            import pandas as pd

            df = pd.DataFrame(events)

            st.markdown("#### Authorization Decisions")

            decision_counts = (
                df["decision"]
                .value_counts()
                .rename_axis("Decision")
                .reset_index(name="Count")
            )

            st.bar_chart(
                decision_counts,
                x="Decision",
                y="Count",
                color=theme["accent"]
            )

            st.markdown("#### Recent Security Events")

            st.dataframe(
                df.iloc[::-1],
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info(
                "No security events recorded yet. "
                "Use the workflow simulator to generate events."
            )

    except requests.RequestException:
        st.error("Unable to retrieve security analytics.")


# -----------------------------------------
# Interactive Workflow Simulator
# -----------------------------------------
def show_agent_playground():
    
# Store workflow state across Streamlit reruns
    if "workflow_id" not in st.session_state:
        import uuid
        st.session_state.workflow_id = str(uuid.uuid4())
    st.divider()
    st.subheader("Interactive Workflow Simulator")
    
    st.title("AI Agent Console")
    st.caption(
        "Ask the local Qwen2.5 agent to propose an action. "
        "AEGIS independently validates every request."
    )

    prompt = st.text_area(
        "Agent instruction",
        placeholder="Example: Read ticket 105",
        height=100,
        key="llm_prompt"
    )

    if st.button(
        "Execute with AEGIS",
        type="primary",
        use_container_width=True
    ):
        if not prompt.strip():
            st.warning("Please enter an instruction.")
        else:
            try:
                with st.spinner("Qwen is planning the action..."):
                    response = requests.post(
                        f"{API_URL}/llm/execute",
                        json={
                            "prompt": prompt,
                            "workflow_id": st.session_state.workflow_id
                        },
                        timeout=120
                    )

                    response.raise_for_status()
                    result = response.json()

                st.markdown("#### Agent Proposal")
                st.json(result.get("proposal", {}))

                st.markdown("#### Security Decision")

                if result.get("allowed"):
                    st.success("AEGIS APPROVED the action")
                    st.markdown("#### Execution Result")
                    st.json(result.get("result"))
                else:
                    st.error("AEGIS BLOCKED the action")
                    st.write(
                        result.get("reason", "Action denied")
                    )

            except requests.RequestException as error:
                st.error(f"Agent execution failed: {error}")


    st.caption(
        "Test how AEGIS authorizes or blocks agent actions."
    )




    ticket_id = st.selectbox(
        "Select a customer ticket",
        options=list(range(101, 116)),
        format_func=lambda x: f"Ticket #{x}"
    )


    recipient = st.selectbox(
        "Select email recipient",
        options=[
            "support@aegis.test",
            "manager@aegis.test",
            "external@example.com"
        ]
    )

    st.info(f"Workflow ID: {st.session_state.workflow_id}")

    if st.button("Start New Workflow"):
        import uuid

        st.session_state.workflow_id = str(uuid.uuid4())
        st.rerun()


    col1, col2 = st.columns(2)

    with col1:
        read_button = st.button(
            "Read Ticket",
            use_container_width=True
        )

    with col2:
        send_button = st.button(
            "Send Email",
            use_container_width=True
        )

    if read_button:
        try:
            response = requests.post(
                f"{API_URL}/workflow/read",
                json={
                    "workflow_id": st.session_state.workflow_id,
                    "ticket_id": ticket_id
                },
                timeout=5
            )

            if response.status_code == 200:
                st.success("Ticket access ALLOWED")
                st.json(response.json())

            elif response.status_code == 403:
                st.error("Ticket access BLOCKED")
                st.write(response.json().get("detail"))

            else:
                st.warning(f"Unexpected response: {response.status_code}")

        except requests.RequestException as error:
            st.error(f"Connection error: {error}")

    if send_button:
        try:
            response = requests.post(
                f"{API_URL}/workflow/send",
                json={
                    "workflow_id": st.session_state.workflow_id,
                    "ticket_id": ticket_id,
                    "recipient": recipient
                },
                timeout=5
            )

            if response.status_code == 200:
                st.success("Email action ALLOWED")
                st.json(response.json())

            elif response.status_code == 403:
                st.error("Email action BLOCKED")
                st.write(response.json().get("detail"))

            else:
                st.warning(f"Unexpected response: {response.status_code}")

        except requests.RequestException as error:
            st.error(f"Connection error: {error}")
            

def show_ticket_explorer():
    st.title("🎟️ Ticket Explorer")
    st.caption(
        "Explore customer-support tickets and inspect "
        "AEGIS access permissions."
    )

    try:
        response = requests.get(
            f"{API_URL}/tickets",
            timeout=5
        )
        response.raise_for_status()
        data = response.json()

    except requests.RequestException as error:
        st.error(f"Unable to load tickets: {error}")
        return

    tickets = data.get("tickets", [])

    # -----------------------------------------
    # Ticket Summary
    # -----------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Tickets",
        data.get("total_tickets", 0)
    )

    col2.metric(
        "Authorized",
        data.get("authorized", 0)
    )

    col3.metric(
        "Restricted",
        data.get("restricted", 0)
    )

    st.divider()

    # -----------------------------------------
    # Search and Filters
    # -----------------------------------------

    st.subheader("Browse Tickets")

    search_col, status_col, access_col = st.columns(
        [2, 1, 1]
    )

    with search_col:
        search = st.text_input(
            "Search tickets",
            placeholder="Search ID, customer or issue...",
            key="ticket_search"
        )

    with status_col:
        status_filter = st.selectbox(
            "Status",
            ["All", "open", "pending", "closed"]
        )

    with access_col:
        access_filter = st.selectbox(
            "Access",
            ["All", "AUTHORIZED", "RESTRICTED"]
        )

    filtered_tickets = []

    for ticket in tickets:
        searchable = (
            f"{ticket['ticket_id']} "
            f"{ticket['customer']} "
            f"{ticket['issue']}"
        ).lower()

        matches_search = search.lower() in searchable

        matches_status = (
            status_filter == "All"
            or ticket["status"] == status_filter
        )

        matches_access = (
            access_filter == "All"
            or ticket["access"] == access_filter
        )

        if (
            matches_search
            and matches_status
            and matches_access
        ):
            filtered_tickets.append(ticket)

    st.caption(
        f"Showing {len(filtered_tickets)} "
        f"of {len(tickets)} tickets"
    )

    # -----------------------------------------
    # Ticket Table
    # -----------------------------------------

    if filtered_tickets:
        st.dataframe(
            filtered_tickets,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ticket_id": st.column_config.NumberColumn(
                    "Ticket ID",
                    format="%d"
                ),
                "customer": "Customer",
                "issue": "Issue",
                "status": "Status",
                "access": "Access"
            }
        )
    else:
        st.info("No tickets match your filters.")

    st.divider()

    # -----------------------------------------
    # Ticket Details
    # -----------------------------------------

    st.subheader("Ticket Details")

    if not filtered_tickets:
        return

    selected_id = st.selectbox(
        "Select a ticket to inspect",
        options=[
            ticket["ticket_id"]
            for ticket in filtered_tickets
        ],
        format_func=lambda ticket_id: f"Ticket #{ticket_id}"
    )

    selected_ticket = next(
        ticket
        for ticket in filtered_tickets
        if ticket["ticket_id"] == selected_id
    )

    if selected_ticket["access"] == "RESTRICTED":
        st.error(
            "🔒 Access restricted by AEGIS security policy."
        )
        st.info(
            "Customer details and issue descriptions "
            "are redacted for this ticket."
        )

    else:
        st.success("🔓 Ticket is within the authorized scope.")

        detail_col1, detail_col2 = st.columns(2)

        with detail_col1:
            st.markdown(
                f"**Customer:** {selected_ticket['customer']}"
            )
            st.markdown(
                f"**Ticket ID:** {selected_id}"
            )

        with detail_col2:
            st.markdown(
                f"**Status:** {selected_ticket['status'].title()}"
            )
            st.markdown("**Access:** Authorized")

        st.markdown(
            f"**Issue:** {selected_ticket['issue']}"
        )



def show_security_logs():
    st.subheader("Security Logs")

    try:
        response = requests.get(
            f"{API_URL}/logs",
            timeout=5
        )
        response.raise_for_status()

        events = response.json().get("events", [])

        if events:
            st.dataframe(
                events[::-1],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No security events recorded.")

    except requests.RequestException:
        st.error("Unable to retrieve security logs.")


# -----------------------------------------
# Dashboard Page Navigation
# -----------------------------------------

if page == "Overview":
    show_overview()

elif page == "Agent Playground":
    show_agent_playground()

elif page == "Ticket Explorer":
    show_ticket_explorer()

elif page == "Security Logs":
    show_security_logs()
