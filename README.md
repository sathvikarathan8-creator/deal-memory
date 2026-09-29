# DealMemory

**AI Sales Call Memory Assistant**

DealMemory is an AI-powered sales-call preparation assistant that helps
a sales representative prepare for the next customer call by recalling
relevant information from previous sales conversations.

The project uses **Hindsight** as its persistent memory layer, **Groq**
as the LLM provider, and **Streamlit** as the user interface.

> **Core workflow:** Retain sales-call information → Recall relevant
> history → Generate actionable preparation → Retain new call outcomes
> for future preparation.

------------------------------------------------------------------------

## 1. Overview

Sales representatives may need to remember information distributed
across multiple customer conversations, including:

-   Customer requirements
-   Pricing objections
-   Competitors being considered
-   Decision-maker concerns
-   Customer preferences
-   Security or other review requirements
-   Commitments and pending follow-ups
-   Changes over the course of a deal

DealMemory provides a focused workflow for this problem.

A representative selects a company and asks a question such as:

> "What's blocking this deal?"

The application retrieves relevant memories from Hindsight and provides
those memories to the LLM. The LLM then generates a concise answer based
on the available evidence.

New call information can also be retained through the application. Later
questions can therefore use the updated history.

------------------------------------------------------------------------

## 2. Problem

A stateless AI assistant does not automatically maintain useful context
from earlier customer interactions.

For a sales representative preparing for a later call, important
information may have been discussed several conversations earlier.
Without persistent memory, the representative may need to reconstruct
that context manually.

DealMemory addresses this by making persistent sales-call memory a
central part of the agent workflow.

The project follows the HackwithHyderabad 3.0 guidance to keep the scope
focused around one workflow, one persona, and one clear value
proposition while demonstrating how Hindsight memory affects agent
behavior over time.

------------------------------------------------------------------------

## 3. Solution

### Persona

**Sales Representative**

### Workflow

**Prepare for the next customer call**

### Value Proposition

**Turn past sales conversations into actionable preparation for the next
customer call.**

### Memory Loop

``` text
Previous Sales Call
       |
       v
    RETAIN
       |
       v
Hindsight Memory
       |
       v
     RECALL
       |
       v
Relevant Customer Context
       |
       v
Groq LLM
       |
       v
Pre-call Answer
       |
       v
New Sales Call
       |
       +--------------------+
                            |
                            v
                         RETAIN
```

Hindsight is part of the main question-answering path: recalled
customer-specific information is supplied to the LLM before it generates
the answer.

------------------------------------------------------------------------

## 4. Example Scenario

The current demonstration uses **Northwind Logistics** as synthetic/demo
customer data.

The seeded demonstration history contains five sales calls covering:

1.  Initial requirements and the primary business sponsor
2.  A CFO objection to per-seat pricing and a request for annual pricing
3.  Salesforce being mentioned as an alternative
4.  A request for security documentation
5.  A sales-representative commitment to send the requested security
    documentation

A representative can ask questions such as:

``` text
Who is the competitor?
What's blocking this deal?
What pricing concern did the CFO raise?
What should I know before my next call?
```

Hindsight retrieves relevant memories, and the LLM uses those memories
to generate the response.

A new call can subsequently be added through the **Retain a New Call**
section. For example:

``` text
Customer now prefers annual pricing and wants predictable yearly billing.
```

That information is retained in Hindsight and can be recalled in later
preparation.

------------------------------------------------------------------------

## 5. Key Features

### Persistent Sales-Call Memory

Sales-call information is retained in Hindsight and associated with the
relevant company memory bank.

### Contextual Recall

When a representative asks a question, the application retrieves
relevant Hindsight memories instead of relying only on the current
question.

### Memory ON/OFF Comparison

The interface provides a Hindsight memory toggle, allowing comparison
between:

-   A response generated without customer-specific memories
-   A response generated using recalled Hindsight memories

### New Call Retention

The application provides a workflow for entering a new call and storing
it as additional memory.

### Evidence-Based Responses

The agent prompt instructs the LLM to use the supplied Hindsight
memories as the source of customer-specific facts and not invent
customer information.

### Memories Recalled

The interface displays the memories retrieved for a question, making the
memory contribution visible.

------------------------------------------------------------------------

## 6. Architecture

``` text
                         +----------------------+
                         |      Streamlit UI    |
                         |      frontend/       |
                         +----------+-----------+
                                    |
                       ask_agent()  |  retain_call()
                                    |
                                    v
                         +----------------------+
                         |       Backend        |
                         |                      |
                         |      agent.py        |
                         |      memory.py       |
                         +-----+----------+-----+
                               |          |
                         Recall|          |Retain
                               |          |
                               v          v
                     +-----------+   +-----------+
                     | Hindsight |   | Hindsight |
                     |  Recall   |   |  Retain   |
                     +-----+-----+   +-----+-----+
                           |               |
                           +-------+-------+
                                   |
                                   v
                         Customer Memory
                              History
                                   |
                                   v
                              Groq LLM
                                   |
                                   v
                             Final Answer
```

### Component Responsibilities

  -----------------------------------------------------------------------
  Component                           Responsibility
  ----------------------------------- -----------------------------------
  Streamlit                           User interface and interaction

  `backend/agent.py`                  Agent prompt, Hindsight recall
                                      integration, and Groq generation

  `backend/memory.py`                 Hindsight client, memory-bank
                                      management, retain, recall,
                                      reflect, and health check

  `backend/seed.py`                   Inserts the predefined Northwind
                                      demonstration calls into Hindsight

  `backend/test_backend.py`           Tests Hindsight connectivity,
                                      retain, recall, and Groq
                                      integration

  `data/deals.json`                   Demo data used by the frontend

  `.env`                              Local API credentials and
                                      configuration

  `requirements.txt`                  Python dependencies
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 7. Technology Stack

### Application

-   Python
-   Streamlit

### Agent / LLM

-   Groq
-   Default configured model: `openai/gpt-oss-120b`

### Memory

-   Hindsight
-   Python client: `hindsight-client==0.10.1`
-   Hindsight Cloud API endpoint: `https://api.hindsight.vectorize.io`

### Configuration

-   `python-dotenv` for environment-variable loading

------------------------------------------------------------------------

## 8. Project Structure

``` text
DealMemory/
│
├── backend/
│   ├── __init__.py
│   ├── memory.py
│   ├── agent.py
│   ├── seed.py
│   └── test_backend.py
│
├── frontend/
│   └── app.py
│
├── data/
│   └── deals.json
│
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md
```

### `backend/memory.py`

Manages the Hindsight integration, including:

-   Company memory-bank creation/initialization
-   Retaining sales-call information
-   Recalling relevant memories
-   Hindsight reflection support
-   Hindsight API health/version checking

Company names are converted into stable bank IDs using a slug-based
naming scheme, for example:

``` text
Northwind Logistics
        ↓
deal-northwind-logistics
```

The memory bank is configured for sales-call information such as
requirements, objections, competitors, commitments, decision makers,
preferences, risks, and changes over time.

### `backend/agent.py`

Connects Hindsight memory with Groq.

Main interface:

``` python
ask_agent(
    company="Northwind Logistics",
    query="What's blocking this deal?",
    use_memory=True,
)
```

When memory is enabled:

1.  The question is sent to Hindsight Recall.
2.  Relevant memories are retrieved.
3.  The memories are formatted into the LLM prompt.
4.  Groq generates the answer.
5.  The function returns the answer and recalled memories.

### `backend/seed.py`

Inserts the predefined Northwind Logistics demonstration calls into
Hindsight.

Run:

``` powershell
python backend\seed.py
```

The presence of the same information in `data/deals.json` does not
itself populate Hindsight. `seed.py` performs the actual Retain
operations.

### `backend/test_backend.py`

Verifies:

-   Hindsight API connectivity
-   Retain
-   Recall
-   Groq + Hindsight answering
-   Memory-disabled agent behavior

Run:

``` powershell
python backend  est_backend.py
```

### `frontend/app.py`

Provides:

-   Company selection
-   Hindsight memory toggle
-   Question input
-   AI-generated call preparation
-   Recalled-memory display
-   New-call retention workflow
-   Deal snapshot information from demo data

### `data/deals.json`

Contains demo deal information used by the frontend.

It is separate from Hindsight's persistent memory. Hindsight is
populated through the backend Retain workflow.

------------------------------------------------------------------------

## 9. Hindsight Memory Design

Each company is represented by a Hindsight memory bank.

Example:

``` text
Northwind Logistics
        |
        v
deal-northwind-logistics
        |
        +-- Call 01
        +-- Call 02
        +-- Call 03
        +-- Call 04
        +-- Call 05
        +-- New retained calls
```

The memory bank is configured with a sales-focused retention mission so
that durable information from customer-call notes can be extracted and
retained.

### Retain

Stores information from a sales call:

``` python
retain_call(
    company="Northwind Logistics",
    call_id="northwind-call-06",
    call_notes="Customer now prefers annual pricing.",
)
```

### Recall

Retrieves information relevant to a question:

``` python
recall_memories(
    company="Northwind Logistics",
    query="What is blocking this deal?",
)
```

### Reflect

The backend also contains a `reflect_memory()` helper for Hindsight
reflection. The core question-answering path currently uses Recall
directly.

------------------------------------------------------------------------

## 10. Agent Behavior

The agent is instructed to:

-   Use supplied Hindsight memories as the source of customer-specific
    facts
-   Avoid inventing customer facts
-   State when something is not known from the available history
-   Prioritize objections and blockers
-   Consider decision makers and their concerns
-   Consider competitors
-   Consider customer preferences
-   Consider pending commitments
-   Consider changes since earlier calls
-   Give concise, actionable answers
-   Separate facts from suggestions

This keeps generated answers grounded in recalled customer history.

------------------------------------------------------------------------

## 11. Installation

### Prerequisites

The project requires:

-   Python
-   A Hindsight API key
-   A Groq API key

### 1. Open the project

``` powershell
cd DealMemory
```

### 2. Create a virtual environment

``` powershell
python -m venv .venv
```

### 3. Activate it

``` powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution for the current session:

``` powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

``` powershell
python -m pip install -r requirements.txt
```

------------------------------------------------------------------------

## 12. Environment Configuration

Create `.env` in the project root:

``` env
HINDSIGHT_API_URL=https://api.hindsight.vectorize.io
HINDSIGHT_API_KEY=your_hindsight_api_key
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

`.env.example` is provided as a template.

### Security

Do not commit `.env` to GitHub.

Recommended `.gitignore` entries:

``` gitignore
.env
.venv/
__pycache__/
*.pyc
```

Keep API keys private and out of source code.

------------------------------------------------------------------------

## 13. Running the Backend Test

From the project root:

``` powershell
python backend  est_backend.py
```

A successful test verifies:

``` text
Hindsight API
     ↓
Retain
     ↓
Recall
     ↓
Groq + Hindsight
     ↓
Memory-disabled comparison
```

The exact response text depends on the memories and API responses
available at runtime.

------------------------------------------------------------------------

## 14. Loading the Demo Memory

Populate Hindsight with the predefined Northwind Logistics calls:

``` powershell
python backend\seed.py
```

Then start the application:

``` powershell
streamlit run frontendpp.py
```

------------------------------------------------------------------------

## 15. Running the Application

Run from the **DealMemory project root**:

``` powershell
streamlit run frontendpp.py
```

The frontend imports the backend through:

``` python
from backend.agent import ask_agent
from backend.memory import retain_call
```

The frontend does not directly call Hindsight or Groq. Those
integrations remain inside the backend.

------------------------------------------------------------------------

## 16. Using the Application

### Step 1 --- Select a company

Select:

``` text
Northwind Logistics
```

### Step 2 --- Choose memory behavior

Use the **Use Hindsight memory** toggle to control whether Hindsight
Recall is performed before answer generation.

### Step 3 --- Ask a question

Examples:

``` text
Who is the competitor?
```

``` text
What's blocking this deal?
```

``` text
What pricing concern did the CFO raise?
```

``` text
What should I know before my next call?
```

### Step 4 --- Review the answer

The application displays a call-preparation response generated from the
available evidence.

### Step 5 --- Review recalled memories

The **Memories Recalled** section shows the Hindsight memories retrieved
for the question.

### Step 6 --- Retain a new call

Use the **Retain a New Call** section to enter new customer information.

Example:

``` text
Call ID:
northwind-call-06
```

``` text
Call notes:
Customer now prefers annual pricing and wants predictable yearly billing.
```

After retention, later questions can retrieve the new information.

------------------------------------------------------------------------

## 17. Demonstrating the Memory Effect

The memory toggle can be used to compare a response without Hindsight
context against a response using recalled customer history.

### Memory OFF

Ask:

``` text
What's blocking this deal?
```

The model does not receive Hindsight memories.

### Memory ON

Ask the same question.

The model receives relevant memories from previous calls and can use
them to produce customer-specific preparation.

### Retain New Information

Add a new call containing an updated customer preference or deal status.

Then ask a related preparation question again.

The workflow becomes:

``` text
Memory OFF
     ↓
Limited customer context

Memory ON
     ↓
Relevant historical context

New call retained
     ↓
Updated Hindsight memory

Future question
     ↓
Updated customer-specific preparation
```

This before/after behavior demonstrates the central role of Hindsight in
the project.

------------------------------------------------------------------------

## 18. Data and Demo Approach

The current Northwind Logistics scenario is synthetic/demo data created
for the project.

It is not presented as real customer data.

The implementation uses a small, focused scenario rather than attempting
to build a complete CRM or sales platform.

The scope focuses on one workflow:

> **Preparing a sales representative for the next customer call.**

------------------------------------------------------------------------

## 19. Scope

### Included

-   Sales-call memory
-   Company-specific Hindsight memory banks
-   Hindsight Retain
-   Hindsight Recall
-   Groq-based response generation
-   Memory ON/OFF comparison
-   Recalled-memory visibility
-   New-call retention
-   Streamlit interface
-   Seeded demonstration data
-   Backend integration testing

### Not included

The current project does not attempt to provide:

-   A complete CRM
-   Salesforce integration
-   Email integration
-   Calendar integration
-   Voice transcription
-   Authentication
-   A multi-agent architecture
-   A large external sales dataset
-   A full production sales-management platform

These exclusions keep the implementation focused on the memory-powered
sales-call preparation workflow.

------------------------------------------------------------------------

## 20. API Boundaries

The frontend communicates with the backend through two main functions.

### Ask the agent

``` python
result = ask_agent(
    company="Northwind Logistics",
    query="What's blocking this deal?",
    use_memory=True,
)
```

The returned result contains:

``` python
{
    "answer": "...",
    "memories": [...],
    "company": "...",
    "memory_enabled": True,
}
```

### Retain a new call

``` python
retain_call(
    company="Northwind Logistics",
    call_id="northwind-call-06",
    call_notes="Customer now prefers annual pricing.",
)
```

Keeping these operations behind backend functions means the frontend
does not need to directly manage Hindsight or Groq API interactions.

------------------------------------------------------------------------

## 21. Design Principles

### Focused Workflow

The application is designed around one primary job: preparing a sales
representative for the next customer call.

### Memory-Centered Architecture

Hindsight is part of the main question-answering path rather than an
unrelated add-on.

### Grounded Generation

Customer-specific facts supplied to the LLM come from recalled memory.

### Visible Memory

The UI exposes the memories recalled for a question so the role of
persistent memory can be inspected.

### Incremental Learning

New call information can be retained and subsequently recalled.

### Clear Separation of Responsibilities

The frontend handles interaction, while the backend handles agent and
memory integration.

------------------------------------------------------------------------

## 22. Troubleshooting

### `ModuleNotFoundError: No module named 'memory'`

Use package-qualified imports:

``` python
from backend.memory import recall_memories
```

and:

``` python
from backend.agent import ask_agent
```

Make sure `backend/__init__.py` exists.

### `ModuleNotFoundError: No module named 'dotenv'`

Install the project dependencies:

``` powershell
python -m pip install -r requirements.txt
```

### No demo companies found

Check that:

``` text
data/deals.json
```

exists in the project root.

The frontend resolves the data file relative to the project root.

### Northwind has no Hindsight memories

The demo data in `data/deals.json` does not automatically populate
Hindsight.

Run:

``` powershell
python backend\seed.py
```

Then test Recall:

``` powershell
python backend  est_backend.py
```

### Hindsight authentication errors

Check:

``` env
HINDSIGHT_API_KEY=...
```

in `.env`.

Verify that the key is valid and has the required access.

### Groq authentication errors

Check:

``` env
GROQ_API_KEY=...
```

in `.env`.

------------------------------------------------------------------------

## 23. Current Status

The project implements the complete demonstration workflow:

-   Hindsight API connectivity
-   Hindsight memory retention
-   Hindsight memory recall
-   Groq-based answer generation
-   Memory-enabled and memory-disabled paths
-   Seeded sales-call history
-   New-call retention
-   Streamlit interface
-   Recalled-memory display
-   Backend integration testing

The project is intended as a focused demonstration of a memory-enabled
sales-call preparation agent rather than a complete production CRM
system.

------------------------------------------------------------------------

## 24. References

### Hindsight

-   Documentation: https://hindsight.vectorize.io/
-   GitHub: https://github.com/vectorize-io/hindsight
-   Hindsight Cloud: https://ui.hindsight.vectorize.io

### Groq

-   https://groq.com/

### Streamlit

-   https://streamlit.io/

------------------------------------------------------------------------

## 25. Summary

DealMemory is a focused AI sales-call preparation assistant built around
persistent memory.

Its central workflow is:

``` text
RETAIN
  ↓
Remember past sales-call information
  ↓
RECALL
  ↓
Retrieve relevant customer context
  ↓
GENERATE
  ↓
Produce actionable call preparation
  ↓
RETAIN
  ↓
Learn from the next customer interaction
```

The key behavior is not simply generating another AI response. It is
using accumulated customer-specific memory so that future preparation
can incorporate information from previous interactions and newly
retained calls.
