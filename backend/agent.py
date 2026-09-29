import os
from typing import Any

from dotenv import load_dotenv
from groq import Groq

from backend.memory import recall_memories

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b",
)

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is not set. Put it in your .env file."
    )


groq_client = Groq(
    api_key=GROQ_API_KEY
)


SYSTEM_PROMPT = """
You are DealMemory, an AI sales-call preparation assistant.

Your job is to help a sales representative prepare for the
next call with a customer company.

Use the supplied Hindsight memories as the source of
customer-specific facts.

Do not invent customer facts.

If the memories do not establish something, say that it is
not known from the available history.

Prioritize:

- current objections or blockers
- decision makers and their concerns
- competitors mentioned
- customer preferences
- commitments that are still pending
- changes since earlier calls

Give a concise, actionable answer.

Separate facts from suggestions.
"""


def _format_memories(
    memories: list[dict[str, Any]]
) -> str:

    if not memories:
        return "No relevant Hindsight memories were found."

    lines = []

    for index, memory in enumerate(
        memories,
        start=1
    ):
        text = memory.get("text", "").strip()

        context = memory.get("context")
        occurred_start = memory.get(
            "occurred_start"
        )

        if not text:
            continue

        details = []

        if context:
            details.append(
                f"context: {context}"
            )

        if occurred_start:
            details.append(
                f"date: {occurred_start}"
            )

        suffix = (
            f" ({'; '.join(details)})"
            if details
            else ""
        )

        lines.append(
            f"{index}. {text}{suffix}"
        )

    return (
        "\n".join(lines)
        if lines
        else "No relevant Hindsight memories were found."
    )


def ask_agent(
    company: str,
    query: str,
    use_memory: bool = True,
) -> dict[str, Any]:
    """
    Public interface for the Streamlit frontend.

    Returns:
        {
            "answer": str,
            "memories": list[dict],
            "company": str,
            "memory_enabled": bool,
        }
    """

    if not company.strip():
        raise ValueError(
            "Company name cannot be empty."
        )

    if not query.strip():
        raise ValueError(
            "Question cannot be empty."
        )

    memories: list[dict[str, Any]] = []

    if use_memory:
        memories = recall_memories(
            company,
            query,
        )

    memory_text = _format_memories(
        memories
    )

    user_prompt = f"""
Company: {company}

Sales representative's question:
{query}

Hindsight memories:
{memory_text}

Answer the representative's question using
only the evidence above.
"""

    completion = (
        groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT.strip(),
                },
                {
                    "role": "user",
                    "content": user_prompt.strip(),
                },
            ],
        )
    )

    answer = (
        completion
        .choices[0]
        .message
        .content
        or ""
    )

    return {
        "answer": answer.strip(),
        "memories": memories,
        "company": company,
        "memory_enabled": use_memory,
    }