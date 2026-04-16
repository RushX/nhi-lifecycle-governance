# AI Agent Identity Lifecycle Governance Framework
> Governance, risk controls, and lifecycle enforcement for AI agent identities in the enterprise.

![Status](https://img.shields.io/badge/status-in%20progress-yellow)
![Framework](https://img.shields.io/badge/framework-NIST%20AI%20RMF-blue)
![Standard](https://img.shields.io/badge/standard-ISO%2042001-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Why I Built This

I started exploring this problem after noticing that most enterprise AI governance conversations focus on model risk and output quality, but nobody was talking about what happens to the agent identity after deployment. The joiner-mover-leaver gap felt like the most concrete, underexplored risk. This project is my attempt to make that problem actionable.

---

## The Problem

Traditional IAM and IGA platforms were designed for humans. When AI agents enter the enterprise, they create governance blind spots that existing tooling cannot address:

| Problem | Impact |
|---|---|
| No centralized agent registry | No visibility into what agents exist or who owns them |
| Ad-hoc provisioning with broad permissions | Violation of least-privilege; audit exposure |
| No recertification process | Access drift; stale entitlements persist indefinitely |
| Orphaned agents after owner departure | Unowned identities with live access to sensitive systems |
| No audit trail of agent actions | Compliance failures under SOC 2, GDPR, EU AI Act |

**The scale of the problem:**
- 91% of organizations are already using AI agents — but only 10% have a governance strategy *(Okta, 2026)*
- Only 22% treat AI agents as independent, identity-bearing entities *(Gravitee, 2026)*
- 97% of organizations that experienced an AI-related breach had no AI access controls in place *(IBM, 2025)*
- Shadow AI breaches cost $670,000 more on average than standard incidents *(IBM, 2025)*

---

## Overview

This project addresses the governance gap by treating AI agents as a **distinct identity class** — applying the same joiner-mover-leaver discipline used for human identities, extended to the unique risk profile of autonomous agents.

**This repository contains:**
- A 5-stage AI agent identity lifecycle model
- A compliance control mapping (NIST AI RMF, ISO 42001, SOC 2, EU AI Act)
- A quantitative risk scoring model for agent classification
- Policy templates for registration, provisioning, and retirement
- A working prototype: agent registry API with lifecycle enforcement and audit logging

---

## The 5-Stage Lifecycle Model

```
┌─────────────┐    ┌──────────────┐    ┌────────────┐    ┌──────────────┐    ┌─────────────┐
│ 1. REGISTER │--->│ 2. PROVISION │--->│ 3. MONITOR │--->│ 4. RECERTIFY │--->│ 5. RETIRE   │
└─────────────┘    └──────────────┘    └────────────┘    └──────────────┘    └─────────────┘
                                              │                  │
                                              └──── loop back ───┘
                                         (access re-evaluated every
                                          90 days or on trigger event)
```

---

## Architecture

![System Architecture](./docs/architecture-diagram.png)

---

## Repository Structure

```
agentic-identity-governance/
│
├── framework/
│   ├── lifecycle-model.md              # 5-stage model with 26 controls
│   ├── compliance-mapping.md           # NIST AI RMF / ISO 42001 / SOC 2 / EU AI Act
│   ├── risk-scoring-model.md           # Quantitative risk scoring model
│   ├── failure-scenarios.md            # Real documented incidents
│   └── policies/
│       └── agent-registration-policy.md
│
├── prototype/
│   ├── api/                            # FastAPI agent registry
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── lifecycle.py                # State machine + risk scoring
│   │   ├── audit.py                    # Audit trail logging
│   │   └── routers/agents.py
│   └── README.md
│
├── docs/
│   ├── architecture-diagram.png
│   ├── executive-brief.md
│   └── demo/                           # Demo scenario screenshots
│
└── README.md
```

---

## Compliance Mapping

Controls are mapped across four frameworks:

| Lifecycle Stage | NIST AI RMF | ISO 42001 | SOC 2 | EU AI Act |
|---|---|---|---|---|
| Register | GOVERN 1.1, MAP 1.1 | Clause 6.1, 8.4 | CC6.1 | Art. 9, 13 |
| Provision | MANAGE 1.1, MAP 5.1 | Clause 8.4, 9.1 | CC6.3 | Art. 9 |
| Monitor | MEASURE 2.1, 2.5 | Clause 9.1, 10.1 | CC7.2, CC7.3 | Art. 9, 12 |
| Recertify | GOVERN 4.1, MANAGE 4.1 | Clause 9.3, 10.2 | CC6.3 | Art. 9, 12, 14 |
| Retire | MANAGE 2.4, MAP 3.5 | Clause 8.4, 10.1 | CC6.5 | Art. 9, 12 |

> **EU AI Act deadline:** High-risk AI system obligations become fully enforceable **August 2026**. This framework addresses the governance gap that creates compliance exposure.

---

## Market Validation

This framework was developed independently. The market has since confirmed the direction:

**Vendor landscape (2025–2026):**

| Vendor | Product | Launch |
|---|---|---|
| Saviynt | Identity Security for AI | March 2026 |
| Microsoft | Entra Agent ID | April 2026 |
| Okta | Okta for AI Agents | April 2026 |
| SailPoint | Agent Identity Security | 2025 |
| ConductorOne | NHI + AI Agent Governance | 2025 |
| CrowdStrike | AI Agent Management | 2026 |
| IBM | Agentic AI Identity Management | 2026 |

Every major IGA and identity vendor is now shipping agentic identity products. The question is no longer *whether* enterprises need this governance — it's *who inside the organization builds it*.

This project is an open-source reference implementation that any organization can understand, audit, and adapt — without an enterprise license.

---

## Demo

See [`prototype/README.md`](./prototype/README.md) for the full demo scenario and setup instructions.

**Demo screenshots:** [`docs/demo/`](./docs/demo/)

**Loom walkthrough:** *(coming soon)*

---

## References

- [NIST AI Risk Management Framework](https://www.nist.gov/artificial-intelligence)
- [ISO/IEC 42001 — AI Management Systems](https://www.iso.org/standard/81230.html)
- [Saviynt — Managing AI Agent Lifecycles](https://saviynt.com/blog/ai-agent-lifecycle-management)
- [SailPoint — Securing AI Agents](https://www.sailpoint.com/identity-library/securing-ai-agents)
- [IBM Cost of a Data Breach Report 2025](https://newsroom.ibm.com/2025-07-30-ibm-report)
- [EU AI Act — Official Text](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689)
- [OWASP Top 10 for Agentic AI Applications 2026](https://owasp.org)

---

## Planned UI Features
- Overdue recertification dashboard — agents where `last_reviewed` > 90 days flagged visually
- Risk heatmap — agents plotted by risk score and status
- Owner dashboard — all agents owned by a specific user

## Planned Integrations
- IdP webhook — owner departure triggers automatic agent suspension (Okta, Azure AD, Entra ID)
- HR system sync — owner status continuously validated against HR records

---

## Notes

> `registered_by` and `performed_by` are passed in the request body as a simplification. In production these would be derived from the authenticated user session.

> Status `registered` has been replaced by `pending_review` as the initial agent state. Full document update in progress. See `prototype/api/lifecycle.py` for current implementation.

---

*Last updated: April 2026 | Author: Rushikesh Muley | MS Cybersecurity, Northeastern University*
