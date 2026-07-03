"""
CloudOps AI Assistant
----------------------
A chat app that talks to your published Azure AI Foundry Agent using the
Responses API, chaining turns via previous_response_id (no session/beta
features needed).

Run:
    python -m streamlit run app.py
"""

import os
import re
import streamlit as st
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
PROJECT_ENDPOINT = os.environ["PROJECT_ENDPOINT"]
AGENT_NAME = os.environ["AGENT_NAME"]


@st.cache_resource
def get_openai_client():
    credential = DefaultAzureCredential()
    project_client = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=credential,
        allow_preview=True,
    )
    return project_client.get_openai_client(agent_name=AGENT_NAME)


openai_client = get_openai_client()


def ask(question: str, previous_response_id: str | None) -> tuple[str, str]:
    """Send a question to the agent. Returns (answer_text, response_id)."""
    kwargs = {"input": question}
    if previous_response_id:
        kwargs["previous_response_id"] = previous_response_id

    response = openai_client.responses.create(**kwargs)
    # Strip raw citation markers like [6:0+source] or [10:0+file-abc123_0]
    # that the API embeds inline -- not meaningful to display as-is.
    clean_text = re.sub(r"\u3010[^\u3011]*\u3011", "", response.output_text)
    return clean_text.strip(), response.id


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
st.set_page_config(page_title="CloudOps AI Assistant", page_icon="\u2601\ufe0f")
st.title("\u2601\ufe0f CloudOps AI Assistant")
st.caption(
    "Ask about architecture, migration runbooks, troubleshooting guides, "
    "and operational standards -- grounded in the indexed knowledge base."
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_response_id" not in st.session_state:
    st.session_state.last_response_id = None

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("e.g. What do I do if a Private Endpoint shows Pending?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Asking the agent..."):
            answer, response_id = ask(prompt, st.session_state.last_response_id)
            st.session_state.last_response_id = response_id
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
