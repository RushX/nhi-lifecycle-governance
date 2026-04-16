# AI Agent Identity Registry — Prototype
I started exploring this problem after noticing that most enterprise AI governance conversations focus on model risk and output quality, but nobody was talking about what happens to the agent identity after deployment

As the enterprise system are adopting the use of AI Agents for automating the environment. It becomes necessary to implement the agentic AI's lifecycle to facilitate the security through governance by design. This prototype is the representation of the AI agent Identity Lifecycle Governance. It shows a demo how identity is managed through different stages of the governance

## The problem it solves
Managing Identity and accountability of autonomous/semiautonomus becomes a problem considering:
- Autonomous agents make decisions at machine speed with no human in the loop, who is accountable when something goes wrong?
- Risk is varied with multiple things in picture, autonomy, public exposure, environment, data it handles. 
- periodic access review is necessary to comply with different frameworks.

This prototype works on helps with
- Ownership management
- Risk Classification
- Audit trail 

Ultimately can help growing enterprise/business to keep up with governance side of things while adapting to agentic AI

## How it works
```
┌─────────────┐    ┌──────────────┐    ┌────────────┐    ┌──────────────┐    ┌─────────────┐
│ 1. REGISTER │--->│ 2. PROVISION │--->│ 3. MONITOR │--->│ 4. RECERTIFY │--->│ 5. RETIRE   │
└─────────────┘    └──────────────┘    └────────────┘    └──────────────┘    └─────────────┘
                                              │                  │
                                              └──── loop back ───┘
                                              (access re-evaluated
                                               every 90 days or on
                                               trigger event)
```

The system starts from registering the agent into a registry along with the details necessary to govern the AI
such as registered by, owner, type, data handled, autonomy, environment, end of life date.
At registration, a risk score is automatically calculated based on autonomy level, data classification, external exposure, and deployment environment — determining the level of governance scrutiny required.

Registering the agent it is approved by security team after identifying risk associated with it

Periodic review of the agent is done to monitor and recertify the agent working and access review through logs and audit trails

If the agent reaches end of life it can be sent to retired stage



## Tech stack
- FastAPI
- uvicorn
- PostgreSQL
- SQLAlchemy
- Pydantic
- Python 3.12

## Running locally

### Prerequisites
- Python 3.12+
- PostgreSQL 18+

### Setup
```bash
git clone https://github.com/RushX/nhi-lifecycle-governance
cd prototype/api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Configure environment
Create a `.env` file in `prototype/api/`:
```
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/agent_registry
```
### Create database
```bash
psql -U postgres
CREATE DATABASE agent_registry;
\q
```

### Run
```bash
uvicorn main:app --reload
```

API runs at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/agents/` | Register a new AI agent |
| GET | `/agents/` | List all registered agents |
| GET | `/agents/{agent_id}` | Get a specific agent |
| PATCH | `/agents/{agent_id}/status` | Update lifecycle state |
| POST | `/agents/{agent_id}/certify` | Record recertification |
| GET | `/agents/{agent_id}/audit` | Get complete audit trail |

## Demo scenario
Full interactive documentation available at `/docs` when running locally.

### The story
Acme Corp deploys an autonomous finance agent to reconcile their invoices. The agent is registered, scored as critical risk, reviewed and activated by the security team, recertified, then suspended when the owner departs.

### Step 1 — Register the agent
`POST /agents/` — agent is initially registered with calculated risk score 100, level critical, status is kept to be registered.

### Step 2 — Invalid transition blocked
`PATCH /agents/{id}/status` — attempt to move directly to `pending_review` returns 400. State machine enforces valid transitions only.

### Step 3 — Security team activation
`PATCH /agents/{id}/status` — security team reviews critical risk agent 
and moves to `active` with documented reason.

### Step 4 — Recertification
`POST /agents/{id}/certify` — 90-day review completed. 
`last_reviewed` timestamp populated. Clock resets.

### Step 5 — Owner departure
`PATCH /agents/{id}/status` — IdP system suspends agent when owner 
departs organization. Automated governance response.

### Step 6 — Audit trail
`GET /agents/{id}/audit` — complete chronological history of every 
governance action, fully attributed, tamper-evident.

### Screenshots
See `docs/demo/` for screenshots of each step.

## Known limitations

- `registered_by` and `performed_by` are self-reported in the request body — 
  in production these would be derived from an authenticated user session
- Orphan detection is not automated — in production this would be triggered 
  by a webhook from the IdP (Okta, Azure AD) when an owner's account is deactivated
- Overdue recertification is not scheduled — in production a background job 
  would automatically flag agents where `last_reviewed` exceeds 90 days
- No authentication layer — all endpoints are open for demo purposes
- Single tenant — no multi-organization support

## Planned extensions

- **v2.0 — MCP server governance** — extend the registry to govern MCP servers 
  as a distinct identity class alongside AI agents
- **LLM-based policy evaluation** — use an LLM to evaluate whether an agent's 
  declared use case matches its requested permissions
- **IdP integration** — real-time owner status sync with Okta or Azure AD
- **Scheduled recertification** — background job flagging overdue agents automatically
- **UI dashboard** — risk heatmap, overdue recertification alerts, owner view
- **Multi-tenant support** — organization-level isolation for enterprise deployments