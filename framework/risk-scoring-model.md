# AI Agent Risk Scoring Model
> Version 1.0 | `framework/risk-scoring-model.md`

---

## Purpose

Not all AI agents carry the same risk. A fully autonomous agent processing restricted financial data in production is fundamentally more dangerous than a copilot summarizing public documentation. The risk scoring model provides a quantitative, consistent basis for classifying agents at registration — determining the level of governance scrutiny required before activation.

The score is calculated automatically at registration and cannot be self-reported. It drives the governance response: which agents require security team sign-off, which trigger enhanced monitoring, and which need threat models before deployment.

---

## Scoring Dimensions

Four dimensions are assessed at registration. Each is independently measurable and non-overlapping — together they capture the full governance risk surface of an AI agent.

### 1. Autonomy Level (30% weight, max 30 points)

How independently does the agent act? An agent that requires human approval before every action is low risk. An agent that plans, executes, and adapts without human intervention is high risk.

| Level | Description | Points |
|---|---|---|
| 1 | Human approves every action | 6 |
| 2 | Human reviews outputs before action | 12 |
| 3 | Human monitors but does not approve | 18 |
| 4 | Human notified after action | 24 |
| 5 | Fully autonomous — no human in loop | 30 |

### 2. Data Classification (30% weight, max 30 points)

What is the highest sensitivity of data the agent may access? Higher sensitivity means higher consequence if the agent is compromised or misbehaves.

| Classification | Description | Points |
|---|---|---|
| Public | Publicly available data only | 0 |
| Internal | Internal business data, not regulated | 10 |
| Confidential | Sensitive business data, access restricted | 20 |
| Restricted | Regulated data — PII, financial, medical | 30 |

### 3. Deployment Environment (25% weight, max 25 points)

Where is the agent running? A development agent operates on test data with limited blast radius. A production agent operates on live systems with real consequences.

| Environment | Description | Points |
|---|---|---|
| Development | Test environment, no production data | 5 |
| Staging | Pre-production, limited real data | 15 |
| Production | Live environment, real data and systems | 25 |

### 4. External Exposure (15% weight, max 15 points)

Does the agent interact with external users, systems, or APIs? External exposure increases the attack surface — a prompt injection attack requires external input to trigger.

| Exposure | Points |
|---|---|
| False — internal only | 0 |
| True — external facing | 15 |

---

## Score Calculation

```
risk_score = (autonomy_level × 6)
           + classification_score
           + environment_score
           + exposure_score
```

Maximum possible score: **100**

All four dimensions use fixed lookup values enforced at the API layer — invalid inputs are rejected before scoring occurs.

### Implementation

```python
def calculate_risk_score(autonomy_level: int, data_classification: str,
                          external_exposure: bool, deployment_env: str) -> int:
    score = 0
    score += autonomy_level * 6
    classification_scores = {
        "public": 0, "internal": 10,
        "confidential": 20, "restricted": 30
    }
    score += classification_scores[data_classification.lower()]
    if external_exposure:
        score += 15
    env_scores = {
        "development": 5, "staging": 15, "production": 25
    }
    score += env_scores[deployment_env.lower()]
    return min(score, 100)
```

---

## Risk Levels

| Score | Level | Governance Response |
|---|---|---|
| 0 – 30 | Low | Standard registration, owner sign-off |
| 31 – 60 | Medium | Owner + team lead sign-off |
| 61 – 80 | High | Security team sign-off required |
| 81 – 100 | Critical | Security team sign-off + threat model required |

---

## Sample Agent Profiles

### Profile 1 — HR Policy Copilot (Low Risk)
> Assists employees with HR policy questions. Human reviews all responses.

| Dimension | Value | Score |
|---|---|---|
| Autonomy level | 2 — human reviews outputs | 12 |
| Data classification | Internal | 10 |
| Deployment env | Production | 25 |
| External exposure | False | 0 |
| **Total** | | **47 — Medium** |

---

### Profile 2 — Finance Reconciliation Agent (Critical Risk)
> Autonomously reconciles invoices and matches payments against restricted financial records.

| Dimension | Value | Score |
|---|---|---|
| Autonomy level | 5 — fully autonomous | 30 |
| Data classification | Restricted | 30 |
| Deployment env | Production | 25 |
| External exposure | True | 15 |
| **Total** | | **100 — Critical** |

---

### Profile 3 — Internal Document Summarizer (Low Risk)
> Summarizes internal meeting notes for a development team. Human in the loop.

| Dimension | Value | Score |
|---|---|---|
| Autonomy level | 1 — human approves every action | 6 |
| Data classification | Internal | 10 |
| Deployment env | Development | 5 |
| External exposure | False | 0 |
| **Total** | | **21 — Low** |

---

### Profile 4 — Customer Support Agent (High Risk)
> Handles customer queries autonomously, accesses confidential customer records, external facing.

| Dimension | Value | Score |
|---|---|---|
| Autonomy level | 4 — human notified after action | 24 |
| Data classification | Confidential | 20 |
| Deployment env | Production | 25 |
| External exposure | True | 15 |
| **Total** | | **84 — Critical** |

---

## Governance Actions by Risk Level

| Risk Level | Registration | Activation | Monitoring | Recertification |
|---|---|---|---|---|
| Low | Owner sign-off | Standard certify | Standard baseline | 90-day cadence |
| Medium | Owner + team lead | Standard certify | Standard baseline | 90-day cadence |
| High | Security team sign-off | Security certify | Enhanced monitoring | 60-day cadence |
| Critical | Security team + threat model | Security certify | Continuous monitoring | 30-day cadence |

> **Note:** High and Critical recertification cadences (60/30 days) are policy recommendations. The current prototype enforces a 90-day cadence for all agents. Risk-based cadence scheduling is a planned v2.0 feature.

---

## Design Decisions

**Why four dimensions?**

These four dimensions are independently measurable, non-overlapping, and collectively capture the full governance risk surface. Agent type was considered as a fifth dimension but excluded because it overlaps significantly with autonomy level — both measure behavioral risk. Adding it would double-count that dimension and inflate scores. Agent type is captured as metadata for filtering and reporting purposes.

**Why these weights?**

Autonomy and data classification carry equal weight (30% each) because they represent the two primary risk vectors — *how* the agent acts and *what* it can access. Deployment environment (25%) reflects the operational consequence of a failure. External exposure (15%) reflects attack surface but is binary, so its maximum contribution is appropriately lower.

**Why not self-reported scores?**

The score is calculated by the system from declared attributes — not submitted by the registrant. This prevents gaming. The declared attributes themselves (autonomy level, data classification) are subject to policy review for high-risk agents.

---

## Limitations and Future Work

- **Static scoring** — the score is calculated at registration and not automatically recalculated when the agent's behavior changes. Dynamic re-scoring based on observed behavior is a v2.0 consideration.
- **Self-declared inputs** — autonomy level and data classification are declared by the registrant. High and Critical agents require security team validation of these declarations.
- **Binary external exposure** — external exposure is currently a boolean. A graduated scale (internal / partner-facing / public-facing) would improve precision.
- **No historical benchmarking** — the scoring model is not yet calibrated against real incident data. Weights were set based on GRC judgment and should be validated empirically over time.

---

*Document version: 1.0 | Last updated: April 2026 | Owner: Rushikesh Muley*
*Related: [`lifecycle-model.md`](./lifecycle-model.md) | [`compliance-mapping.md`](./compliance-mapping.md)*
