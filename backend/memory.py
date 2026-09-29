import os
import re
from datetime import datetime
from typing import Any

from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

HINDSIGHT_API_URL = os.getenv(
    "HINDSIGHT_API_URL",
    "https://api.hindsight.vectorize.io",
)

HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")

if not HINDSIGHT_API_KEY:
    raise RuntimeError(
        "HINDSIGHT_API_KEY is not set. Put it in your .env file."
    )


_client = Hindsight(
    base_url=HINDSIGHT_API_URL,
    api_key=HINDSIGHT_API_KEY,
    timeout=60.0,
)


def get_client() -> Hindsight:
    """Return the shared Hindsight client."""
    return _client


def company_to_bank_id(company: str) -> str:
    """Convert a company name into a stable Hindsight bank ID."""
    slug = re.sub(
        r"[^a-z0-9]+",
        "-",
        company.strip().lower()
    ).strip("-")

    if not slug:
        raise ValueError(
            "Company name must contain at least one alphanumeric character."
        )

    return f"deal-{slug}"


def ensure_company_bank(company: str) -> str:
    """
    Create/update the Hindsight memory bank used for one company.
    """
    if not company.strip():
        raise ValueError("Company name cannot be empty.")

    bank_id = company_to_bank_id(company)

    _client.create_bank(
        bank_id=bank_id,
        name=f"DealMemory - {company}",
        background=(
            f"This memory bank stores sales-call experiences for "
            f"the company {company}. "
            "Use memories about requirements, objections, competitors, "
            "commitments, decision makers, preferences, risks, "
            "and changes in the deal."
        ),
        retain_mission=(
            "Extract durable sales knowledge from customer-call notes, "
            "especially requirements, objections, competitors, "
            "commitments, decision makers, preferences, risks, "
            "and changes over time."
        ),
        reflect_mission=(
            f"Help a sales representative prepare for future calls "
            f"with {company} using the company's accumulated "
            "sales-call memories."
        ),
    )

    return bank_id


def retain_call(
    company: str,
    call_notes: str,
    call_id: str,
    call_timestamp: datetime | None = None,
) -> dict[str, Any]:
    """
    Store one customer-call experience in Hindsight.
    """
    if not call_notes.strip():
        raise ValueError("Call notes cannot be empty.")

    if not call_id.strip():
        raise ValueError("call_id cannot be empty.")

    bank_id = ensure_company_bank(company)

    response = _client.retain(
        bank_id=bank_id,
        content=call_notes,
        context=f"Sales call with {company}",
        timestamp=call_timestamp,
        document_id=call_id,
        metadata={
            "company": company,
            "record_type": "sales_call",
        },
        tags=["sales-call"],
        update_mode="replace",
        retain_async=False,
    )

    return response.to_dict()


def recall_memories(
    company: str,
    query: str,
    max_tokens: int = 3000,
) -> list[dict[str, Any]]:
    """
    Retrieve memories relevant to a sales-preparation question.
    """
    if not query.strip():
        raise ValueError("Query cannot be empty.")

    bank_id = ensure_company_bank(company)

    response = _client.recall(
        bank_id=bank_id,
        query=query,
        max_tokens=max_tokens,
        budget="mid",
        include_chunks=False,
    )

    return [
        result.to_dict()
        for result in response.results
    ]


def reflect_memory(
    company: str,
    query: str,
) -> str:
    """
    Optional Hindsight Reflect helper for deeper synthesis.
    """
    if not query.strip():
        raise ValueError("Query cannot be empty.")

    bank_id = ensure_company_bank(company)

    response = _client.reflect(
        bank_id=bank_id,
        query=query,
        budget="low",
        context=(
            "Preparing a sales representative for "
            "the next customer call."
        ),
        include_facts=True,
    )

    return response.text


def health_check() -> str:
    """Return the connected Hindsight API version."""
    version = _client.get_version()
    return version.api_version