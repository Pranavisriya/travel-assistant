from __future__ import annotations

import streamlit as st  # type: ignore

from agent import get_response, SYSTEM_PROMPT

st.set_page_config(page_title="TravelGPT", page_icon="🗺️")
st.title("TravelGPT: Your Personal Travel Assistant")

# ---- Initialize chat history in session state ----
# We keep messages in the same structure Groq expects: [{role, content}, ...]
if "messages" not in st.session_state:
    st.session_state.messages = []

# Ensure a single system message at the start of the thread
if not st.session_state.messages or st.session_state.messages[0].get("role") != "system":
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages

# ---- Render prior turns (skip showing system in UI) ----
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- Input box ----
if prompt := st.chat_input("Type your travel question..."):
    # 1) Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2) Show user's message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3) Generate assistant reply using full history (memory)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply_text = get_response(st.session_state.messages)

        st.markdown(reply_text)

    # 4) Store assistant reply back into history
    st.session_state.messages.append({"role": "assistant", "content": reply_text})