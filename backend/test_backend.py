from datetime import datetime

from backend.agent import ask_agent
from backend.memory import (
    health_check,
    recall_memories,
    retain_call,
)


TEST_COMPANY = "DealMemory Integration Test"


def main() -> None:

    print(
        "1. Hindsight API version:",
        health_check()
    )

    retain_call(
        company=TEST_COMPANY,
        call_id="integration-test-01",
        call_notes=(
            "Integration test memory: the CFO of the "
            "test customer rejected per-seat pricing "
            "and requested annual pricing."
        ),
        call_timestamp=datetime.fromisoformat(
            "2026-09-28T10:00:00"
        ),
    )

    print("2. Retain: OK")

    memories = recall_memories(
        company=TEST_COMPANY,
        query=(
            "What pricing issue did the CFO raise?"
        ),
    )

    print(
        "3. Recall returned",
        len(memories),
        "result(s)."
    )

    if not memories:
        raise RuntimeError(
            "Recall returned no memories. "
            "Check Hindsight credentials, bank creation, "
            "and available Hindsight credits."
        )

    print(
        "   Top memory:",
        memories[0]["text"]
    )

    with_memory = ask_agent(
        company=TEST_COMPANY,
        query=(
            "What is the main pricing concern?"
        ),
        use_memory=True,
    )

    print("4. Groq + Hindsight: OK")
    print(
        "   Answer:",
        with_memory["answer"]
    )

    without_memory = ask_agent(
        company=TEST_COMPANY,
        query=(
            "What is the main pricing concern?"
        ),
        use_memory=False,
    )

    print(
        "5. Groq memory-off path: OK"
    )

    print(
        "   Answer:",
        without_memory["answer"]
    )

    print(
        "\nIntegration test completed successfully."
    )


if __name__ == "__main__":
    main()

# from memory import retain_call

retain_call(
    company="Northwind Logistics",
    call_id="northwind-new-call",
    call_notes=(
        "New call update: the customer now prefers "
        "annual pricing instead of the earlier per-seat model."
    ),
)
# from agent import ask_agent

result = ask_agent(
    company="Northwind Logistics",
    query="What's blocking this deal?",
    use_memory=True,
)

print(result["answer"])