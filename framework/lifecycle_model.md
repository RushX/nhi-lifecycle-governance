# AI Agent Identity Lifecycle Model
> Version 1.0 | Framework Document | `framework/lifecycle-model.md`

---

## Purpose

This document defines the five-stage identity lifecycle model for AI agents operating in enterprise environments. It establishes the governance controls, entry/exit criteria, responsible parties, and failure modes for each stage.

The model is designed to be framework-agnostic and maps directly to NIST AI RMF, ISO 42001, SOC 2, and EU AI Act obligations. See [`compliance-mapping.md`](./compliance-mapping.md) for the full control mapping.

---

## Market Context

This lifecycle model was developed independently. In March 2026, Saviynt launched **Identity Security for AI**, a commercial product whose three pillars: Posture Management, Identity Lifecycle Management, and Runtime Authorization; align closely with the controls defined here. This convergence confirms the framework's direction without having been derived from any vendor's implementation.

One concept from Saviynt's product worth noting is the **Runtime Authorization Gateway**: an intent-aware layer that evaluates what an agent is *trying to do* at execution time before allowing the action. This extends the Monitor stage of this framework and is reflected in control C-MON-02 (scope violations result in immediate blocking). A full runtime authorization layer is noted as a future extension of this framework.

---

## Guiding Principles

This lifecycle model is built on four foundational principles:

**1. AI agents are identities, not applications.**
They must be governed with the same rigor applied to human employees and service accounts (including onboarding, access reviews, and offboarding). The difference is scale and speed: an AI agent can act on thousands of systems in the time it takes a human to complete one task.

**2. Lifecycle governance must be proactive, not reactive.**
Traditional security responds after an incident. This model enforces controls at the point of creation, provisioning, and operation (before exposure becomes a breach).

**3. Applying Least previlage principle.**
Every agent is provisioned with the minimum access required to perform its declared function. No standing permissions. There should not be a "we'll narrow it later."

**4. Using zero standing permissions (just in time access).**
Agents receive just-in-time access scoped to each task. No permanent credentials. No broad standing access provisioned for convenience. Access is granted at execution time and expires when the task completes.

**5. Every action must be attributable.**
An agent without an owner, an audit trail, or a declared use case is a liability. Governance requires that every agent action can be traced to a registered identity, a responsible human, and a business justification.

---

## The Five-Stage Lifecycle

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

---

## Stage 1: Register

### Definition
Registration is the act of formally creating an AI agent identity in the enterprise registry before any access is granted. No agent may receive enterprise credentials, connect to internal systems, or process organizational data without a valid registry entry.

Registration is the hub of the lifecycle, every subsequent stage depends on the integrity of the information captured here. Upon successful registration, the agent is automatically placed in `pending_review` status. No agent transitions to `active` without explicit human certification — enforcing the ITGC change approval gate at the system level.

### Trigger Events
- A team requests deployment of a new AI agent, copilot, or autonomous service
- An existing third-party tool is granted access to enterprise systems via API
- An AI agent framework (e.g. LangChain, AutoGPT, Microsoft Copilot) is connected to internal data sources

### Required Registration Attributes

| Attribute | Description | Required |
|---|---|:---:|
| `agent_id` | Globally unique cryptographic identifier | Yes |
| `agent_name` | Human-readable display name | Yes |
| `agent_type` | Category: copilot / autonomous / API-connected / workflow | Yes |
| `owner_id` | Employee ID of the accountable human owner | Yes |
| `owner_email` | Current email for notifications and review requests | Yes |
| `business_unit` | Owning team or department | Yes |
| `use_case` | Declared business purpose (max 200 chars) | Yes |
| `data_classification` | Highest sensitivity of data the agent may access | Yes |
| `autonomy_level` | Scale: 1 (human-in-loop) to 5 (fully autonomous) | Yes |
| `external_exposure` | Boolean: does agent face external users or systems? | Yes |
| `framework` | Underlying agent framework (LangChain, Copilot, custom, etc.) | Yes |
| `deployment_env` | Production / staging / development | Yes |
| `eol_date` | Declared end-of-life or renewal date | Yes |
| `risk_score` | Calculated at registration (see Risk Scoring Model) | Auto |
| `status` | Lifecycle state: pending_review / active / suspended / retired | Auto |
| `created_at` | Timestamp of registration | Auto |
| `last_reviewed` | Timestamp of most recent recertification | Auto |

### Entry Criteria
- Business justification documented
- Human owner identified and confirmed
- Use case declared and approved by security team for risk classification ≥ Medium
- Threat model completed (required for autonomy_level ≥ 3 or data_classification = Confidential/Restricted)

### Exit Criteria (gate to Provision)
- All required attributes populated
- Risk score calculated
- Owner has acknowledged governance obligations
- For High/Critical risk agents: security team sign-off obtained

### Key Controls
- **C-REG-01:** No agent may receive enterprise credentials without a registry entry
- **C-REG-02:** Every agent must have a named human owner at registration time
- **C-REG-03:** Agents with autonomy_level ≥ 3 require a completed threat model
- **C-REG-04:** All agents must declare an end-of-life date or renewal trigger
- **C-REG-05:** Shadow agents detected by discovery scanning must be retroactively registered or immediately decommissioned

### Failure Modes Addressed
- Shadow AI (unregistered agents with enterprise data access) (**Samsung 2023**)
- Agents with no declared owner (orphan risk from day one)
- Agents without threat modeling, prompt injection exposure (**CVE-2025-32711**)

---

## Stage 2: Provision

### Definition
Provisioning is the controlled assignment of access, credentials, and tool-call scope to a registered agent. Provisioning enforces least privilege at the point of deployment, the agent receives only what it needs for its declared use case, nothing more.

Provisioning is policy-enforced: an automated policy engine validates every access request against the agent's registered use case and risk score before credentials are issued.

### Trigger Events
- Successful completion of Stage 1 (Registration)
- Approved request to expand an existing agent's access scope
- Agent migration to a new environment (e.g. staging → production)

### Provisioning Controls

#### Access Scoping
Every agent is provisioned with:
- **Service identity credentials**: dedicated service account or API key scoped to the agent (never reusing human user credentials)
- **Permission set**: minimum read/write permissions required for the declared use case
- **Tool-call whitelist**: explicit list of APIs, endpoints, and data stores the agent may call
- **Network egress scope**: outbound connections restricted to declared integrations only
- **Data classification ceiling**: agent may not access data above its registered classification level

#### Policy Enforcement at Provisioning
Before any credential is issued, the policy engine checks:

| Policy Rule | Check |
|---|---|
| Scope alignment | Requested permissions match declared use case |
| Least privilege | No standing admin or write access to production without justification |
| Separation of duties | Agent with write access to data store may not also trigger deployments |
| Data ceiling | Access to Restricted/Confidential data requires autonomy_level ≤ 2 OR human-in-loop checkpoint |
| External exposure | Internet-facing agents may not have direct access to internal databases |
| Credential type | Human credentials forbidden; service accounts or short-lived tokens required |

#### Provisioning Record
All provisioning events are written to the audit log:
- Credentials issued (type, scope, expiry)
- Policy checks performed and results
- Approvals obtained (with approver ID and timestamp)
- Access granted (system, permission level, effective date)

### Entry Criteria
- Valid registry entry (Stage 1 complete)
- Policy engine validation passed
- High-risk agents (risk_score ≥ 61) require explicit security team sign-off before status transitions to active. This is a process control — the state machine permits the transition but policy requires documented approval.

### Exit Criteria (gate to Monitor)
- Service credentials issued and logged
- Tool-call scope documented
- Agent owner notified of provisioned access
- Monitoring baseline scheduled for T+7 days post-deployment

### Key Controls
- **C-PRO-01:** Human credentials are prohibited for agent provisioning; service accounts or short-lived tokens required
- **C-PRO-02:** Policy engine must approve all provisioning requests; manual overrides require CISO-level authorization
- **C-PRO-03:** Tool-call scope must be explicitly whitelisted; deny-by-default for unlisted endpoints
- **C-PRO-04:** Credentials must carry expiration dates; no non-expiring credentials for any agent
- **C-PRO-05:** Separation of duties enforced at provisioning time


### Failure Modes Addressed
- Over-provisioned agents with excess write access (**EchoLeak CVE-2025-32711**)
- Agents provisioned on human credentials that persist after owner departure
- Broad scope API keys used for convenience (**IBM Breach Report 2025**)
- Missing separation of duties enabling privilege escalation (**LangChain CVE 2025**)

---

## Stage 3: Monitor

### Definition
Monitoring is the continuous observation of an agent's behavior against its declared use case, provisioned scope, and established behavioral baseline. Monitoring is not periodic (it is continuous and event-driven).

The goal of monitoring is to detect three classes of deviation:
1. **Behavioral anomalies**: the agent is doing something outside its established pattern
2. **Scope violations**: the agent is accessing resources outside its provisioned whitelist
3. **Ownership changes**: the agent's owner has departed, changed roles, or lost authority

### Monitoring Dimensions

#### Behavioral Baseline
Established during the first 7 days post-deployment. The baseline captures:
- Typical query patterns (frequency, data types, volume)
- Normal API call patterns (which endpoints, what frequency)
- Standard output types and destinations
- Regular operational hours and load patterns

Deviations beyond 2 standard deviations from baseline trigger an alert.

#### Scope Monitoring
Continuous comparison of actual agent activity against the provisioned tool-call whitelist:

| Event Type | Alert Threshold | Response |
|---|---|---|
| Unlisted API call attempted | Any occurrence | Immediate block + alert |
| Data classification ceiling exceeded | Any occurrence | Immediate block + alert |
| Network egress to undeclared endpoint | Any occurrence | Block + alert |
| Unusual data volume (read) | >3× baseline | Alert owner |
| Unusual data volume (write) | >2× baseline | Alert owner + security |
| Query pattern shift | >2σ from baseline | Alert owner |

#### Ownership Monitoring
The registry is continuously synced against the HR/IdP system:

| Owner Status Change | Trigger |
|---|---|
| Owner deactivated in IdP | Agent status → `pending_review` within 24 hours |
| Owner role change (department move) | Recertification triggered |
| Owner on extended leave (>30 days) | Delegate owner assignment required |
| No owner found (orphan detected) | Agent suspended pending reassignment |

#### Audit Logging
Every agent action is written to an immutable audit log:
- Timestamp
- Agent ID
- Action type
- Target system/resource
- Data classification of accessed resource
- Outcome (success/failure/blocked)
- Policy rule invoked (if applicable)

Audit logs are append-only, tamper-evident, and retained per applicable compliance requirements (minimum 12 months for SOC 2; 36 months for GDPR-scoped agents).

### Entry Criteria
- Provisioning complete (Stage 2 complete)
- Monitoring tooling connected and baseline scheduled
- Alert routing configured (owner + security team)

### Exit Criteria (gate to Recertify)
- 90 days elapsed since last certification OR trigger event detected
- Monitoring summary report generated for recertification review

### Key Controls
- **C-MON-01:** Behavioral baseline established within 7 days of deployment
- **C-MON-02:** Scope violations result in immediate blocking, not just alerting
- **C-MON-03:** Owner departure triggers agent suspension within 24 hours
- **C-MON-04:** Audit logs are append-only and cannot be modified by the agent or its owner
- **C-MON-05:** Dormant agents (no activity for 30 days) are flagged for retirement review
- **C-MON-06:** Agents in `pending_review` status are suspended from action execution until explicitly cleared by an authorized reviewer
### Failure Modes Addressed
- Orphaned agents continuing to operate after owner departure (**Samsung 2023 / IBM 2025**)
- Prompt injection exfiltration going undetected (**EchoLeak CVE-2025-32711**)
- No audit trail for compliance obligations (**IBM Breach Report 2025**)
- Agents accessing systems outside declared scope (**LangChain CVE 2025**)

---

## Stage 4: Recertify

### Definition
Recertification is the periodic, structured review of an agent's continued authorization to operate. It verifies that the agent's access remains appropriate, its owner remains accountable, and its risk profile has not changed materially since last review.

Recertification occurs on a **90-day cadence** for all active agents, and is also triggered by specific events regardless of cadence.

The key distinction from monitoring: monitoring is continuous and automated. Recertification requires a human decision (an owner must actively confirm that the agent should continue operating with its current access).

### Cadence and Triggers

| Trigger | Recertification Type |
|---|---|
| 90-day elapsed | Standard periodic review |
| Owner departure or role change | Emergency review |
| Risk score increase (≥10 points) | Risk-driven review |
| Security incident involving the agent | Post-incident review |
| Major change to agent capabilities | Change-driven review |
| Regulatory audit preparation | Compliance-driven review |
| Agent inactivity (>30 days) | Dormancy review |

### Recertification Checklist

The assigned owner (or delegate) must complete the following for each review:

**Access Review**
- [ ] Current permission set reviewed against current use case
- [ ] Tool-call whitelist verified as still necessary
- [ ] Any permissions granted since last review justified and confirmed
- [ ] Excess permissions identified and submitted for removal

**Risk Re-assessment**
- [ ] Autonomy level still accurately reflects agent behavior
- [ ] Data classification ceiling still appropriate
- [ ] External exposure profile unchanged or updated
- [ ] Risk score recalculated; material changes escalated

**Operational Review**
- [ ] Agent is still actively used (not dormant)
- [ ] Business use case still valid and current
- [ ] Owner is still the appropriate accountable party
- [ ] End-of-life date reviewed and extended if appropriate

**Compliance Review**
- [ ] No open security findings from monitoring period
- [ ] Audit log reviewed for anomalies
- [ ] Regulatory obligations still met

### Recertification Outcomes

| Outcome | Action |
|---|---|
| **Certified** | Agent continues; next review scheduled; certification logged |
| **Certified with modifications** | Access trimmed; policy updated; agent continues |
| **Deferred** | Owner unable to review; delegate assigned; 14-day grace period |
| **Failed** | Agent suspended immediately; security team notified; retirement initiated |

### Entry Criteria
- 90-day cadence reached OR trigger event fired
- Monitoring summary report available for review
- Owner or delegate identified and notified

### Exit Criteria (gate back to Monitor OR to Retire)
- Owner or delegate has completed and signed the recertification checklist
- All identified excess permissions removed
- Recertification outcome logged with timestamp and approver

### Key Controls
- **C-REC-01:** No agent may remain active beyond 90 days without a completed recertification
- **C-REC-02:** Recertification requires a human decision, it cannot be auto-approved
- **C-REC-03:** Excess permissions identified during review must be removed before recertification is marked complete
- **C-REC-04:** Agents that fail recertification are suspended immediately, not at next scheduled maintenance
- **C-REC-05:** All recertification events are logged with the approver's identity and timestamp

### Failure Modes Addressed
- Access drift: permissions that accumulate over time without review (**IBM Breach Report 2025**)
- Agents excluded from access review cycles (**EchoLeak / SOC 2 finding pattern**)
- No human accountability for continued agent operation
- Dormant agents with live credentials (**Zombie agent pattern**)

---

## Stage 5: Retire

### Definition
Retirement is the controlled, permanent decommissioning of an AI agent identity. It ensures that all access is revoked, all credentials are invalidated, and a complete audit record is preserved.

Retirement is not optional: every agent must eventually retire. The goal is to ensure retirement happens in a controlled, documented manner rather than through abandonment.

### Trigger Events
- Project or use case ends
- Agent fails recertification
- Agent replaced by a successor system
- Owner-initiated retirement
- Mandatory EOL date reached
- Security incident requiring immediate decommission

### Retirement Checklist

**Access Revocation (must complete within 24 hours of trigger)**
- [ ] All API keys and service account credentials invalidated
- [ ] OAuth tokens and session tokens revoked
- [ ] Tool-call whitelist entries removed from policy engine
- [ ] Network egress rules removed
- [ ] All downstream system integrations disconnected

**Credential Rotation**
- [ ] Any secrets the agent had access to are rotated
- [ ] Shared credentials the agent used are changed
- [ ] Key management system updated to reflect revocation

**Registry Update**
- [ ] Agent status set to `retired`
- [ ] Retirement reason documented
- [ ] Successor agent ID linked (if applicable)
- [ ] EOL record sealed with timestamp and approving party

**Audit Trail Preservation**
- [ ] All monitoring logs archived per retention policy
- [ ] Final recertification record preserved
- [ ] Retirement checklist stored in immutable audit record
- [ ] Compliance-required retention period confirmed and set

**Post-Retirement Verification (T+7 days)**
- [ ] Confirm credentials no longer active in identity provider
- [ ] Confirm no residual access in connected systems
- [ ] Confirm audit trail accessible and complete

### Entry Criteria
- Retirement trigger event confirmed
- Owner or security team has authorized retirement
- Successor system identified (if applicable)

### Exit Criteria (terminal — no further stages)
- All credentials invalidated and confirmed inactive
- Audit trail archived and retention period set
- Retirement record sealed in registry

### Key Controls
- **C-RET-01:** Credential revocation must be completed within 24 hours of retirement trigger
- **C-RET-02:** Secrets accessed by the agent must be rotated at retirement
- **C-RET-03:** Audit trail must be preserved for the full retention period before archive
- **C-RET-04:** Post-retirement verification must confirm no residual access within 7 days
- **C-RET-05:** Retirement record is immutable (it cannot be deleted or modified after sealing)

### Failure Modes Addressed
- Zombie agents: credentials left active after project ends (**IBM Breach Report 2025**)
- Credential exposure via leaked config files with stale service account keys
- No audit record of what the agent did during its operational life
- Orphaned integrations remaining connected after agent decommission

---

## Lifecycle Summary Table

| Attribute | Register | Provision | Monitor | Recertify | Retire |
|---|---|---|---|---|---|
| **Primary goal** | Create identity | Assign access | Observe behavior | Validate authorization | Revoke access |
| **Trigger** | Deployment request | Registration complete | Provisioning complete | 90-day cadence / event | EOL / failure / request |
| **Human decision required** | Owner + Security | Policy engine + approvals | Automated (alerts to humans) | Owner / delegate | Owner / Security |
| **Key output** | Registry entry | Credentials + scope | Audit log + alerts | Certification record | Retirement record |
| **Failure → action** | Block deployment | Block provisioning | Alert + block violation | Suspend agent | Immediate revocation |
| **NIST AI RMF** | GOVERN 1.1, MAP 1.1 | MANAGE 1.1, MAP 5.1 | MEASURE 2.1, 2.5 | GOVERN 4.1, MANAGE 4.1 | MANAGE 2.4, MAP 3.5 |
| **ISO 42001** | Clause 6.1, 8.4 | Clause 8.4, 9.1 | Clause 9.1, 10.1 | Clause 9.3, 10.2 | Clause 8.4, 10.1 |
| **SOC 2** | CC6.1 | CC6.3 | CC7.2, CC7.3 | CC6.3 | CC6.5 |

---

## Appendix: Control Register

All controls referenced in this document, indexed for traceability:

| Control ID | Stage | Description |
|---|---|---|
| C-REG-01 | Register | No agent receives credentials without a registry entry |
| C-REG-02 | Register | Every agent must have a named human owner |
| C-REG-03 | Register | Autonomy level ≥ 3 requires threat model |
| C-REG-04 | Register | All agents must declare an EOL date |
| C-REG-05 | Register | Shadow agents must be registered or decommissioned |
| C-REG-06 | Register | Agent status automatically set to `pending_review` on registration — activation requires explicit human certification |
| C-PRO-01 | Provision | Human credentials prohibited; service accounts required |
| C-PRO-02 | Provision | Policy engine must approve all provisioning |
| C-PRO-03 | Provision | Tool-call scope explicitly whitelisted; deny-by-default |
| C-PRO-04 | Provision | All credentials must carry expiration dates |
| C-PRO-05 | Provision | Separation of duties enforced at provisioning |
| C-MON-01 | Monitor | Behavioral baseline within 7 days of deployment |
| C-MON-02 | Monitor | Scope violations result in immediate blocking |
| C-MON-03 | Monitor | Owner departure triggers suspension within 24 hours |
| C-MON-04 | Monitor | Audit logs are append-only and tamper-evident |
| C-MON-05 | Monitor | Dormant agents flagged for retirement after 30 days |
| C-MON-06 | Monitor | Agents in pending_review blocked from execution until cleared |
| C-REC-01 | Recertify | No agent active beyond 90 days without recertification |
| C-REC-02 | Recertify | Recertification requires a human decision |
| C-REC-03 | Recertify | Excess permissions removed before certification completes |
| C-REC-04 | Recertify | Failed recertification triggers immediate suspension |
| C-REC-05 | Recertify | All recertification events logged with approver identity |
| C-RET-01 | Retire | Credential revocation within 24 hours of trigger |
| C-RET-02 | Retire | Secrets accessed by agent rotated at retirement |
| C-RET-03 | Retire | Audit trail preserved for full retention period |
| C-RET-04 | Retire | Post-retirement verification within 7 days |
| C-RET-05 | Retire | Retirement record is immutable after sealing |

---

*Document version: 1.0 | Last updated: April 2026 | Owner: Rushikesh Muley*  
*Next review: July 2026 | Related: [`compliance-mapping.md`](./compliance-mapping.md) | [`risk-scoring-model.md`](./risk-scoring-model.md)*
