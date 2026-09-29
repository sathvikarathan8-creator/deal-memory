import json
import sys
from pathlib import Path
from datetime import datetime

import streamlit as st

# Project root
ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.agent import ask_agent
from backend.memory import retain_call


DATA_FILE = ROOT_DIR / "data" / "deals.json"


def load_demo_data():
    if not DATA_FILE.exists():
        return {"companies": []}

    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


st.set_page_config(
    page_title="DealMemory",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 DealMemory")
st.caption(
    "Prepare for the next customer call using persistent sales-call memory."
)

data = load_demo_data()
companies = data.get("companies", [])

if not companies:
    st.error("No demo companies found in data/deals.json.")
    st.stop()

company_names = [
    company["name"]
    for company in companies
]

# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.header("Deal")

    selected_company = st.selectbox(
        "Select company",
        company_names,
    )

    memory_enabled = st.toggle(
        "Use Hindsight memory",
        value=True,
        help="Turn off to compare the agent with and without memory.",
    )

    selected_data = next(
        company
        for company in companies
        if company["name"] == selected_company
    )

    st.divider()

    st.subheader("Deal snapshot")

    st.write(
        selected_data.get(
            "description",
            ""
        )
    )

    st.metric(
        "Recorded calls",
        len(
            selected_data.get(
                "calls",
                []
            )
        ),
    )


# -----------------------------
# Call preparation
# -----------------------------

st.subheader(
    f"Prepare for {selected_company}"
)

query = st.text_area(
    "What do you want to know before the next call?",
    value="What's blocking this deal?",
    height=100,
    placeholder=(
        "Ask about objections, competitors, "
        "commitments, decision makers, or preferences..."
    ),
)

if st.button(
    "Prepare me",
    type="primary",
    use_container_width=True,
):

    if not query.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Preparing your call brief..."
        ):

            try:

                result = ask_agent(
                    company=selected_company,
                    query=query,
                    use_memory=memory_enabled,
                )

                st.session_state[
                    "last_result"
                ] = result

            except Exception as exc:

                st.error(
                    f"Could not prepare the call: {exc}"
                )


# -----------------------------
# Agent response
# -----------------------------

result = st.session_state.get(
    "last_result"
)

if result:

    st.divider()

    left, right = st.columns(
        [2, 1]
    )

    with left:

        st.subheader(
            "Call preparation"
        )

        st.write(
            result["answer"]
        )

    with right:

        st.subheader(
            "Memories Recalled"
        )

        memories = result.get(
            "memories",
            []
        )

        if not memory_enabled:

            st.info(
                "Memory is OFF. "
                "No Hindsight memories were recalled."
            )

        elif not memories:

            st.info(
                "No relevant memories were found."
            )

        else:

            for index, memory in enumerate(
                memories,
                start=1
            ):

                memory_text = (
                    memory
                    .get("text", "")
                    .strip()
                )

                if memory_text:

                    with st.container(
                        border=True
                    ):

                        st.caption(
                            f"Memory {index}"
                        )

                        st.write(
                            memory_text
                        )


# -----------------------------
# Retain new call
# -----------------------------

st.divider()

st.subheader(
    "Retain a New Call"
)

st.write(
    "Add the latest customer interaction. "
    "It will be stored in Hindsight and "
    "can influence future call preparation."
)

with st.form(
    "new_call_form",
    clear_on_submit=True
):

    call_id = st.text_input(
        "Call ID",
        placeholder="northwind-call-06",
    )

    call_notes = st.text_area(
        "Call notes",
        placeholder=(
            "Example: Customer now prefers annual "
            "pricing and asked for an updated proposal."
        ),
        height=140,
    )

    submitted = st.form_submit_button(
        "Save call to memory",
        type="primary",
    )

    if submitted:

        if (
            not call_id.strip()
            or not call_notes.strip()
        ):

            st.warning(
                "Call ID and call notes are required."
            )

        else:

            try:

                with st.spinner(
                    "Saving call to Hindsight..."
                ):

                    response = retain_call(
                        company=selected_company,
                        call_id=call_id.strip(),
                        call_notes=call_notes.strip(),
                        call_timestamp=datetime.now(),
                    )

                st.success(
                    "Call successfully stored in Hindsight."
                )

            except Exception as exc:

                st.error(
                    f"Could not save the call: {exc}"
                )


st.caption(
    "DealMemory uses Hindsight for persistent memory "
    "and Groq for response generation."
)