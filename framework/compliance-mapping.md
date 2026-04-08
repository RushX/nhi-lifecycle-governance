# AI Agent Identity Lifecycle: Compliance Mapping
> Version 1.0 | `framework/compliance-mapping.md`

---

## Purpose

This document maps every control in the AI Agent Identity Lifecycle Model to four compliance frameworks:

- **NIST AI RMF**: AI Risk Management Framework (NIST, 2023)
- **ISO/IEC 42001**: AI Management Systems Standard (ISO, 2023)
- **SOC 2 Type II**: Trust Services Criteria (AICPA)
- **EU AI Act**: Regulation (EU) 2024/1689, high-risk AI system obligations

The mapping enables organizations to demonstrate that lifecycle governance controls satisfy existing audit and regulatory obligations: without building a separate compliance program for AI agents.

---

## How to Read This Document

Each lifecycle stage has its own mapping table. Columns are:

| Column | Description |
|---|---|
| Control ID | References the control register in `lifecycle-model.md` |
| Control Description | Brief description of the control |
| NIST AI RMF | Applicable function and subcategory |
| ISO 42001 | Applicable clause |
| SOC 2 | Applicable Trust Services Criteria |
| EU AI Act | Applicable article or obligation |

Where a control satisfies multiple requirements within the same framework, all references are listed.

---

## Stage 1: Register

### Control Mapping

| Control ID | Control Description | NIST AI RMF | ISO 42001 | SOC 2 | EU AI Act |
|---|---|---|---|---|---|
| C-REG-01 | No agent receives credentials without a registry entry | GOVERN 1.1: Policies and processes for AI risk management established | Clause 6.1.2: AI risk assessment process | CC6.1: Logical access security | Art. 9: Risk management system |
| C-REG-02 | Every agent must have a named human owner | GOVERN 1.2: Accountability for AI risk management assigned | Clause 5.3: Roles and responsibilities | CC1.2: Management oversight | Art. 9(8): Human oversight obligations |
| C-REG-03 | Autonomy level ≥ 3 requires completed threat model | MAP 1.1: Context established for AI risk assessment | Clause 6.1.2: Threat and risk analysis | CC3.1: Risk identification | Art. 9(2): Risk identification for high-risk AI |
| C-REG-04 | All agents must declare an end-of-life date | GOVERN 1.4: AI lifecycle governance policies established | Clause 8.4: AI system lifecycle management | CC6.5: Logical access revocation | Art. 13: Transparency obligations |
| C-REG-05 | Shadow agents must be registered or decommissioned | MAP 1.5: Organizational risk exposure identified | Clause 8.2: AI system inventory | CC6.1: Access restrictions | Art. 9: Risk management system |

### Framework Notes

**NIST AI RMF:** The GOVERN function requires organizations to establish policies and assign accountability before AI systems operate. Registration directly instantiates GOVERN 1.1 and 1.2 by creating an enforceable record of ownership and policy acknowledgment at the point of agent creation.

**ISO 42001:** Clause 6.1 requires a systematic risk assessment process. Registration is the trigger for that process, no assessment can occur for an agent that isn't formally identified.

**SOC 2:** CC6.1 requires logical access security measures including identification and authentication of users and devices. AI agents are devices/services requiring the same treatment.

**EU AI Act:** Article 9 requires a risk management system for high-risk AI systems. Registration establishes the minimum data required to classify an agent and trigger the appropriate level of risk management.

---

## Stage 2: Provision

### Control Mapping

| Control ID | Control Description | NIST AI RMF | ISO 42001 | SOC 2 | EU AI Act |
|---|---|---|---|---|---|
| C-PRO-01 | Human credentials prohibited; service accounts required | MANAGE 1.1: AI risk treatments implemented | Clause 8.4: AI system operational controls | CC6.3: Access restrictions enforced | Art. 9(7): Technical controls for high-risk AI |
| C-PRO-02 | Policy engine must approve all provisioning | GOVERN 2.1: Policies enforced across AI lifecycle | Clause 8.4: Operational planning and control | CC6.3: Authorized access only | Art. 9: Risk management controls |
| C-PRO-03 | Tool-call scope explicitly whitelisted; deny-by-default | MANAGE 2.2: Mechanisms to achieve AI risk goals implemented | Clause 8.4: Access control for AI systems | CC6.3: Least privilege enforced | Art. 9(2)(b): Risk mitigation measures |
| C-PRO-04 | All credentials must carry expiration dates | MANAGE 1.3: AI risk responses monitored | Clause 9.1: Monitoring and measurement | CC6.3: Credential lifecycle management | Art. 9(7): Technical safeguards |
| C-PRO-05 | Separation of duties enforced at provisioning | GOVERN 1.1: Organizational practices for AI risk | Clause 6.1.2: Risk treatment options | CC6.3: Access restriction controls | Art. 9(8): Human oversight measures |

### Framework Notes

**NIST AI RMF:** The MANAGE function covers implementing treatments for identified risks. Least-privilege provisioning and policy enforcement are the primary treatments for the over-provisioning risk identified in MAP and MEASURE stages.

**ISO 42001:** Clause 8.4 covers operational control of AI systems, including access management. The requirement to control what an AI system can access and do is explicit in the standard's operational planning requirements.

**SOC 2:** CC6.3 requires that access is restricted to authorized users and that access is granted on a need-to-know basis. The deny-by-default tool-call whitelist directly satisfies this criterion for AI agent identities.

**EU AI Act:** Article 9(2)(b) requires risk mitigation measures to be applied to high-risk AI systems. Least-privilege provisioning is a technical risk mitigation measure that reduces the blast radius of a compromised or misbehaving agent.

---

## Stage 3: Monitor

### Control Mapping

| Control ID | Control Description | NIST AI RMF | ISO 42001 | SOC 2 | EU AI Act |
|---|---|---|---|---|---|
| C-MON-01 | Behavioral baseline within 7 days of deployment | MEASURE 2.1: AI risk measurement approaches established | Clause 9.1: Performance monitoring | CC7.2: Anomaly detection | Art. 9(2): Ongoing risk monitoring |
| C-MON-02 | Scope violations result in immediate blocking | MANAGE 2.4: AI risk response mechanisms operational | Clause 10.1: Continual improvement triggers | CC7.3: Response to identified anomalies | Art. 9(7): Technical protective measures |
| C-MON-03 | Owner departure triggers suspension within 24 hours | GOVERN 4.1: Organizational teams assigned AI accountability | Clause 5.3: Roles, responsibilities, authorities | CC7.2: Monitoring for anomalies | Art. 9(8): Human oversight maintained |
| C-MON-04 | Audit logs are append-only and tamper-evident | MEASURE 2.5: AI risk measurement results documented | Clause 9.1: Evidence of monitoring results | CC7.2: Audit log integrity | Art. 12: Record keeping obligations |
| C-MON-05 | Dormant agents flagged for retirement after 30 days | MANAGE 4.1: AI risks monitored over time | Clause 9.1: Continual monitoring | CC6.5: Access removal for inactive accounts | Art. 9: Risk management system |

### Framework Notes

**NIST AI RMF:** The MEASURE function is the most directly relevant here, it covers establishing metrics, collecting data, and identifying when AI systems deviate from expected behavior. Controls C-MON-01 through C-MON-05 collectively implement the MEASURE function for AI agent identities.

**ISO 42001:** Clause 9.1 requires organizations to monitor, measure, analyze, and evaluate their AI management system. Behavioral monitoring with documented baselines and alert thresholds is the operational implementation of this clause.

**SOC 2:** CC7.2 requires detection of and response to security events. The behavioral baseline and anomaly detection controls directly satisfy this criterion, particularly for detecting scope violations and ownership changes.

**EU AI Act:** Article 12 introduces explicit record-keeping obligations for high-risk AI systems, logs must be maintained automatically and must enable post-hoc reconstruction of the system's operation. C-MON-04's append-only audit log directly satisfies this requirement.

---

## Stage 4: Recertify

### Control Mapping

| Control ID | Control Description | NIST AI RMF | ISO 42001 | SOC 2 | EU AI Act |
|---|---|---|---|---|---|
| C-REC-01 | No agent active beyond 90 days without recertification | GOVERN 4.1: AI risk governance reviewed periodically | Clause 9.3: Management review | CC6.3: Periodic access reviews | Art. 9(2): Ongoing risk management |
| C-REC-02 | Recertification requires a human decision | GOVERN 6.1: Human oversight of AI maintained | Clause 5.1: Leadership and human oversight | CC1.2: Management oversight of controls | Art. 14: Human oversight measures |
| C-REC-03 | Excess permissions removed before certification completes | MANAGE 4.1: AI risk treatments updated | Clause 10.2: Corrective action | CC6.3: Access restrictions maintained | Art. 9(2)(b): Risk mitigation maintained |
| C-REC-04 | Failed recertification triggers immediate suspension | MANAGE 2.4: Response to AI risk events | Clause 10.1: Nonconformity and corrective action | CC7.3: Response to control failures | Art. 9(7): Protective measures enforced |
| C-REC-05 | All recertification events logged with approver identity | MEASURE 2.5: AI risk documentation maintained | Clause 9.1: Documented evidence of reviews | CC4.1: Monitoring and reporting | Art. 12: Record keeping obligations |

### Framework Notes

**NIST AI RMF:** GOVERN 4.1 specifically addresses organizational oversight and periodic review of AI risk governance. The 90-day recertification cadence operationalizes this requirement with a concrete, auditable schedule.

**ISO 42001:** Clause 9.3 requires management review of the AI management system at planned intervals. Recertification is the agent-level implementation of this requirement: each agent undergoes its own management review on a defined cadence.

**SOC 2:** CC6.3 requires periodic reviews of access to ensure it remains appropriate. The recertification checklist directly maps to this criterion, with the added requirement that excess permissions be removed before the review is marked complete.

**EU AI Act:** Article 14 is the most significant here: it requires that high-risk AI systems be designed to allow effective human oversight. The requirement that recertification cannot be auto-approved (C-REC-02) directly implements Article 14's human oversight mandate.

---

## Stage 5: Retire

### Control Mapping

| Control ID | Control Description | NIST AI RMF | ISO 42001 | SOC 2 | EU AI Act |
|---|---|---|---|---|---|
| C-RET-01 | Credential revocation within 24 hours of trigger | MANAGE 2.4: AI risk response executed | Clause 8.4: Operational control at end-of-life | CC6.5: Access removed upon termination | Art. 9(7): Technical safeguards enforced |
| C-RET-02 | Secrets accessed by agent rotated at retirement | MANAGE 1.3: Risk treatments verified | Clause 8.4: AI system decommissioning controls | CC6.5: Credential lifecycle completion | Art. 9(2): Risk elimination at end-of-life |
| C-RET-03 | Audit trail preserved for full retention period | MEASURE 2.5: Documentation retained | Clause 9.1: Evidence retention | CC7.2: Audit log retention | Art. 12(1): Log retention obligations |
| C-RET-04 | Post-retirement verification within 7 days | MANAGE 4.2: AI risk treatment effectiveness verified | Clause 9.1: Verification of controls | CC6.5: Access removal verified | Art. 9: Risk management closure |
| C-RET-05 | Retirement record is immutable after sealing | MEASURE 2.5: AI risk records integrity maintained | Clause 9.1: Integrity of documented information | CC7.2: Audit log integrity | Art. 12: Record keeping integrity |

### Framework Notes

**NIST AI RMF:** The MANAGE function includes explicit requirements to verify that risk treatments have been effective. Post-retirement verification (C-RET-04) is the closure step that confirms the MANAGE cycle is complete for a retired agent.

**ISO 42001:** Clause 8.4 covers the full AI system lifecycle including decommissioning. The retirement checklist operationalizes the standard's requirement that end-of-life be managed in a controlled and documented manner.

**SOC 2:** CC6.5 requires that access is removed when no longer needed. The 24-hour revocation SLA (C-RET-01) and post-retirement verification (C-RET-04) together provide the evidence required to satisfy CC6.5 in an audit.

**EU AI Act:** Article 12(1) requires that high-risk AI systems automatically generate logs that are retained for the appropriate period. C-RET-03 and C-RET-05 together satisfy this by preserving the audit trail and ensuring it cannot be modified after the agent is retired.

---

## Cross-Framework Summary

### Coverage by Framework

| Lifecycle Stage | NIST AI RMF | ISO 42001 | SOC 2 | EU AI Act |
|---|:---:|:---:|:---:|:---:|
| Register | GOVERN 1.1, 1.2, 1.4 / MAP 1.1, 1.5 | 5.3, 6.1.2, 8.2, 8.4 | CC1.2, CC3.1, CC6.1, CC6.5 | Art. 9, 13 |
| Provision | GOVERN 2.1 / MANAGE 1.1, 1.3, 2.2 | 6.1.2, 8.4, 9.1 | CC6.3 | Art. 9 |
| Monitor | GOVERN 4.1 / MANAGE 2.4, 4.1 / MEASURE 2.1, 2.5 | 5.3, 9.1, 10.1 | CC7.2, CC7.3 | Art. 9, 12 |
| Recertify | GOVERN 4.1, 6.1 / MANAGE 2.4, 4.1 / MEASURE 2.5 | 5.1, 9.1, 9.3, 10.1, 10.2 | CC1.2, CC4.1, CC6.3, CC7.3 | Art. 9, 12, 14 |
| Retire | MANAGE 1.3, 2.4, 4.2 / MEASURE 2.5 | 8.4, 9.1 | CC6.5, CC7.2 | Art. 9, 12 |

### Key Observations

**1. NIST AI RMF provides the broadest coverage.**
All four NIST AI RMF functions (GOVERN, MAP, MEASURE, MANAGE) are addressed across the five lifecycle stages. This confirms the lifecycle model is comprehensive relative to the most widely adopted AI risk framework.

**2. EU AI Act Article 12 (record keeping) is the most consistently implicated obligation.**
Audit logging requirements appear in Monitor, Recertify, and Retire stages. Organizations subject to the EU AI Act should prioritize immutable audit logging as the single highest-value compliance control.

**3. SOC 2 CC6.3 and CC6.5 are the most frequently satisfied criteria.**
Access restriction and access removal are the SOC 2 criteria most directly addressed by lifecycle governance. This makes the framework immediately relevant for organizations pursuing or maintaining SOC 2 Type II certification.

**4. ISO 42001 Clause 9.1 spans four of five stages.**
Monitoring and measurement requirements appear throughout the lifecycle. Organizations implementing ISO 42001 should treat lifecycle governance as the primary operational mechanism for satisfying Clause 9.

---

## Regulatory Timeline Reference

| Framework | Status | Key Deadline |
|---|---|---|
| NIST AI RMF | Active: voluntary | No mandatory deadline; widely adopted |
| ISO 42001 | Active: certifiable | No mandatory deadline; certification available now |
| SOC 2 Type II | Active: audit-driven | Continuous; annual audit cycles |
| EU AI Act | Active: phased enforcement | High-risk AI obligations fully enforceable August 2026 |

> **Note:** The EU AI Act's high-risk AI system obligations become fully enforceable in August 2026. Organizations deploying AI agents in regulated contexts should treat this lifecycle framework as a compliance prerequisite for that deadline.

---

*Document version: 1.0 | Last updated: April 2026 | Owner: Rushikesh Muley*
*Related: [`lifecycle-model.md`](./lifecycle-model.md) | [`risk-scoring-model.md`](./risk-scoring-model.md)*
