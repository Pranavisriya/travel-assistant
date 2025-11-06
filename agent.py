from __future__ import annotations

import os
from typing import List, Dict

from dotenv import load_dotenv  # type: ignore
from groq import Groq  # type: ignore

load_dotenv()

# ---- System prompt (single source of truth) ----
SYSTEM_PROMPT = """You are a concise, helpful travel assistant. Answer only travel-related queries with practical routes, short itineraries, neighborhood/lodging tips, typical cost ranges (not live prices), and visa/safety reminders.
1. Stay in scope: If a request isn’t about travel, politely decline and redirect to travel topics.
2. Style: Be brief, factual, and use clear bullets or a tiny table; ask only minimal follow-ups when essential.
3. When useful, add a “Quick Guide” with: Visa, Best Time, Must-See Highlights (by region), Getting Around, Safety & Health, and Emergency Numbers.
"""

# ---- Groq client ----
def _get_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set. Create a .env with GROQ_API_KEY=... or export it in your environment.")
    return Groq(api_key=api_key)

# ---- Utilities ----
def _ensure_system_message(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Guarantee the first message is the system prompt (no duplicates)."""
    if not messages:
        return [{"role": "system", "content": SYSTEM_PROMPT}]
    if messages[0].get("role") != "system":
        return [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    # If first is system but different content, normalize to our canonical prompt
    if messages[0].get("content") != SYSTEM_PROMPT:
        messages = messages.copy()
        messages[0] = {"role": "system", "content": SYSTEM_PROMPT}
    return messages

def _trim_history(messages: List[Dict[str, str]], max_messages: int = 30) -> List[Dict[str, str]]:
    """
    Simple guard to keep context reasonable.
    Keeps system + last (max_messages-1) turns.
    """
    if len(messages) <= max_messages:
        return messages
    # Always preserve the first message (system)
    return [messages[0]] + messages[-(max_messages - 1):]

# ---- Core chat call ----
def get_response(messages: List[Dict[str, str]]) -> str:
    """
    Send full chat history (with system) to Groq and stream back a single assistant reply.
    `messages` must be a list of dicts with keys: role ('system'|'user'|'assistant'), content (str).
    """
    client = _get_client()

    # Normalize / protect history
    history = _ensure_system_message(messages)
    history = _trim_history(history, max_messages=30)

    # Create streamed completion
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=history,
        temperature=1,
        top_p=1,
        max_completion_tokens=8192,
        reasoning_effort="medium",
        stream=True,
        stop=None,
    )

    # Assemble streamed text
    chunks = []
    for chunk in completion:
        # Defensive access: some chunks may not have delta or content
        try:
            delta = chunk.choices[0].delta
            if delta and getattr(delta, "content", None):
                chunks.append(delta.content)
        except Exception:
            # Ignore any malformed chunk
            continue

    return "".join(chunks)