from datetime import datetime

from memory import (
    ensure_company_bank,
    retain_call,
)


DEMO_CALLS = [
    {
        "company": "Northwind Logistics",
        "call_id": "northwind-call-01",
        "timestamp": datetime.fromisoformat(
            "2026-09-01T10:00:00"
        ),
        "notes": (
            "Initial discovery call. Northwind Logistics "
            "operates a distributed sales and operations team. "
            "They want a centralized platform with role-based "
            "access, reporting, and easy onboarding. "
            "The VP of Sales is the primary business sponsor."
        ),
    },

    {
        "company": "Northwind Logistics",
        "call_id": "northwind-call-02",
        "timestamp": datetime.fromisoformat(
            "2026-09-05T11:00:00"
        ),
        "notes": (
            "Pricing discussion. The CFO objected to the "
            "per-seat pricing model because the customer has "
            "many occasional users. The CFO asked whether "
            "an annual contract with predictable pricing "
            "could be offered."
        ),
    },

    {
        "company": "Northwind Logistics",
        "call_id": "northwind-call-03",
        "timestamp": datetime.fromisoformat(
            "2026-09-10T14:00:00"
        ),
        "notes": (
            "Competitive discussion. The customer mentioned "
            "Salesforce as an alternative being evaluated. "
            "The customer wants clear evidence that our "
            "workflow can be adopted without a long "
            "implementation."
        ),
    },

    {
        "company": "Northwind Logistics",
        "call_id": "northwind-call-04",
        "timestamp": datetime.fromisoformat(
            "2026-09-15T15:00:00"
        ),
        "notes": (
            "Security review. The customer requested security "
            "documentation, including information about data "
            "protection and access controls. The security team "
            "needs this before the deal can move to final review."
        ),
    },

    {
        "company": "Northwind Logistics",
        "call_id": "northwind-call-05",
        "timestamp": datetime.fromisoformat(
            "2026-09-20T16:00:00"
        ),
        "notes": (
            "Commitment from the sales representative: send "
            "the requested security report and documentation "
            "to the customer. The customer has not yet "
            "confirmed that the security review is complete."
        ),
    },
]


def main() -> None:

    for call in DEMO_CALLS:

        ensure_company_bank(
            call["company"]
        )

        result = retain_call(
            company=call["company"],
            call_notes=call["notes"],
            call_id=call["call_id"],
            call_timestamp=call["timestamp"],
        )

        print(
            f"Stored {call['call_id']}: "
            f"success={result['success']}, "
            f"items={result['items_count']}"
        )


if __name__ == "__main__":
    main()