# Enterprise AI Agent Failure Scenarios
> Real, documented incidents mapped to lifecycle control gaps.

These scenarios are grounded in publicly reported incidents and cited research. Each maps directly to missing controls in the 5-stage AI Agent Identity Lifecycle model.

---

## Scenario 1: The Shadow AI Leak,  Samsung (April 2023)
**Category:** Shadow AI,  Registration & Provisioning Gap  
**Risk Level:** Critical  
**Source:** Bloomberg, TechCrunch, CIO Dive (April–May 2023)

### What Happened
In April 2023, Samsung Electronics allowed engineers at its semiconductor division to use ChatGPT to assist with work tasks. Within 20 days, three separate incidents occurred in which employees submitted sensitive proprietary data to the public ChatGPT service:

- An engineer pasted source code from a semiconductor database into ChatGPT to debug a fault
- A second engineer submitted code for identifying defective equipment to request optimization
- A third employee recorded an internal meeting, converted it to text using NAVER CLOVA, and submitted it to ChatGPT to generate meeting minutes

Because ChatGPT used input data to improve its models, Samsung's proprietary source code and internal meeting content was transmitted to OpenAI's servers,  data the company acknowledged it could not retrieve or delete.

Samsung responded by banning generative AI tools company-wide and capping prompt size at 1,024 bytes per input as an emergency measure.

### Why It Happened
- No policy existed requiring AI tools to be registered or approved before employees connected them to enterprise workflows
- Employees used personal or general-purpose AI tools with no scope restrictions on what data could be submitted
- No DLP controls were in place to detect sensitive data being sent to external AI services
- 68% of professionals in a concurrent Fishbowl survey reported using AI at work without disclosing it to managers,  normalizing shadow AI behavior

### Control Gap in the Lifecycle Model
| Stage | Missing Control |
|---|---|
| Register | No mandatory registration gate before AI tools accessed enterprise data |
| Provision | No data scoping policy; employees used public endpoints with full data access |
| Monitor | No DLP monitoring for data exfiltration via AI prompt submission |

### What This Framework Does
- Registration is a prerequisite,  AI tools cannot process enterprise data without a registry entry and declared use case
- Provisioning policy enforces data classification constraints on what an agent may ingest
- Continuous monitoring flags data matching sensitivity labels being submitted to external AI endpoints

**Reference:** [Samsung bans ChatGPT after employee leak,  TechCrunch, May 2023](https://techcrunch.com/2023/05/02/samsung-bans-use-of-generative-ai-tools-like-chatgpt-after-april-internal-data-leak/)

---

## Scenario 2: The Over-Permissioned Copilot,  EchoLeak / CVE-2025-32711 (June 2025)
**Category:** Excess Privilege & Runtime Monitoring Gap  
**Risk Level:** Critical (CVSS 9.3)  
**Source:** Aim Security, SecurityWeek, The Hacker News (June 2025)

### What Happened
In June 2025, researchers at Aim Security disclosed CVE-2025-32711, dubbed "EchoLeak",  a zero-click vulnerability in Microsoft 365 Copilot. The attack exploited how Copilot was provisioned with broad access across Outlook, SharePoint, OneDrive, and Teams, combined with no isolation of trust boundaries between internal and external content.

An attacker could send a specially crafted email to any M365 user. The email contained hidden adversarial prompts disguised as ordinary business text,  invisible to the human recipient but processed by Copilot as instructions. When the user later asked Copilot a routine question, Copilot's RAG engine retrieved the malicious email as context, executed the hidden instructions, and silently exfiltrated the user's chat history, referenced files, and sensitive organizational data to an attacker-controlled server,  with no user interaction required.

The attack bypassed Microsoft's XPIA (cross-prompt injection attack) classifiers, link redaction mechanisms, and Content Security Policy. Microsoft patched the vulnerability server-side in May 2025. No evidence of exploitation in the wild was found prior to patching.

### Why It Happened
- Copilot was provisioned with access to all content the user could access,  email, SharePoint, Teams, OneDrive,  with no least-privilege scoping by workflow or sensitivity
- No trust boundary enforcement existed between internal trusted content and external untrusted inputs (emails from outside the org)
- No behavioral monitoring was in place to detect Copilot accessing data outside normal usage patterns
- The agent's tool-calling scope was not constrained to declared use cases

### Control Gap in the Lifecycle Model
| Stage | Missing Control |
|---|---|
| Provision | Copilot granted full-scope access rather than least-privilege per declared use case |
| Monitor | No behavioral baseline; no anomaly detection on data access patterns |
| Register | No threat model produced at deployment; prompt injection not assessed as a risk vector |

### What This Framework Does
- Provisioning policy enforces least-privilege: agent access is scoped to the declared workflow, not the full user permission set
- Trust boundary enforcement at the API gateway level prevents untrusted external content from being treated as instructions
- Behavioral monitoring flags access to data outside the agent's declared scope
- Threat modeling (including prompt injection) is a required step in the registration workflow

**Reference:** [EchoLeak: Zero-Click AI Vulnerability in M365 Copilot,  SecurityWeek, June 2025](https://www.securityweek.com/echoleak-ai-attack-enabled-theft-of-sensitive-data-via-microsoft-365-copilot/)  
**CVE:** [CVE-2025-32711,  NVD](https://nvd.nist.gov/vuln/detail/cve-2025-32711)

---

## Scenario 3: Shadow AI at Scale,  IBM Cost of a Data Breach Report (2025)
**Category:** Shadow AI Governance Gap,  Systemic  
**Risk Level:** High  
**Source:** IBM Cost of a Data Breach Report 2025, Ponemon Institute (July 2025)

### What Happened
IBM's 2025 Cost of a Data Breach Report,  based on data from 600 organizations globally,  was the first edition to formally measure AI-specific security incidents. Key findings:

- **13%** of organizations reported a breach of AI models or applications
- Of those breached, **97%** reported not having AI access controls in place
- **1 in 5** organizations reported a breach caused specifically by shadow AI
- Organizations with high levels of shadow AI saw breach costs **$670,000 higher** on average than those with low or no shadow AI
- **63%** of breached organizations either had no AI governance policy or were still developing one at the time of the breach
- Only **34%** of organizations with governance policies performed regular audits for unsanctioned AI

The report concluded that AI adoption is "greatly outpacing AI security and governance" at enterprise scale.

### Why It Happened (Systemic Pattern)
- Business users deployed AI tools without IT or security involvement,  no registration requirement existed
- AI governance policies, where they existed, did not include detection or enforcement mechanisms for unsanctioned agents
- Access controls were not extended to AI models and applications,  the same controls applied to human identities were not applied to AI agents
- Audit processes did not include non-human identities

### Control Gap in the Lifecycle Model
| Stage | Missing Control |
|---|---|
| Register | No enterprise-wide requirement to register AI agents before deployment |
| Provision | AI agents deployed without formal access controls |
| Monitor | No discovery or detection of unsanctioned AI activity |
| Recertify | AI agents not included in periodic access review processes |

### What This Framework Does
- Provides the governance infrastructure that the 63% of organizations lacked at time of breach
- Registration policy creates the mandatory gate missing in shadow AI scenarios
- Discovery scanning detects agents operating outside the registry
- Agents are treated as first-class identities in access certification cycles

**Reference:** [IBM Cost of a Data Breach Report 2025,  IBM Newsroom, July 2025](https://newsroom.ibm.com/2025-07-30-ibm-report-13-of-organizations-reported-breaches-of-ai-models-or-applications,-97-of-which-reported-lacking-proper-ai-access-controls)

---

## Scenario 4: The Prompt Injection Attack Surface,  LangChain CVE (January 2025)
**Category:** Runtime Abuse via Unscoped Tool Access  
**Risk Level:** Critical  
**Source:** DataBahn AI Agent Security CVE Report (February 2026)

### What Happened
In January 2025, a critical vulnerability was disclosed in LangChain,  the most widely used open-source framework for building AI agents, with 847 million downloads affected. The vulnerability combined a serialization flaw with prompt injection, enabling credential exfiltration via HTTP headers.

The attack mechanism: malicious LLM output triggered object instantiation, which then exfiltrated credentials through outbound HTTP calls embedded in response headers. Any enterprise agent built on LangChain and processing untrusted external input was potentially exposed.

The same research report documented a parallel incident with the EmailGPT Gmail extension (CVE, June 2024),  a prompt injection attack via email content leading to system prompt leakage and email manipulation on behalf of the compromised user account.

### Why It Happened
- Agent frameworks were integrated into enterprise workflows without a threat model for prompt injection as a runtime attack vector
- Tool-calling scope was not enforced,  agents could make outbound network calls not declared in their provisioned use case
- No behavioral monitoring existed to detect unexpected outbound connections from agent processes
- Developers integrated open-source agent frameworks without evaluating their security posture or CVE exposure

### Control Gap in the Lifecycle Model
| Stage | Missing Control |
|---|---|
| Register | No security assessment of agent framework dependencies at registration time |
| Provision | Outbound network access not scoped to declared integrations |
| Monitor | No alerting on unexpected outbound connections or environment variable exfiltration |

### What This Framework Does
- Registration workflow includes a security assessment of agent framework and dependency CVEs
- Provisioning policy enforces network egress scoping,  agents may only call declared endpoints
- Runtime monitoring detects outbound connections outside the provisioned scope and triggers alerts

**Reference:** [AI Agent Security Incidents and CVEs,  DataBahn, February 2026](https://www.databahn.ai/blog/ai-agents-security-incidents-and-related-cves-for-enterprise-security-teams)

---

## Scenario 5: Governance Policy Void,  Industry-Wide (2025)
**Category:** Lifecycle Governance Gap,  Systemic  
**Risk Level:** High  
**Source:** IBM 2025 Cost of a Data Breach Report; Adversa AI 2025 Incidents Report

### What Happened
The Adversa AI 2025 AI Security Incidents Report found that 2025 was on track to surpass all prior years combined in AI breach volume. Across 17 real-world case studies,  spanning Microsoft, Amazon Q, OmniGPT, Asana AI, and ElizaOS,  the report identified three recurring failure patterns present across nearly every incident:

1. **Improper validation**,  agents processed untrusted input without sanitization
2. **Infrastructure gaps**,  agents were deployed without security controls appropriate to their access scope
3. **Missing human oversight**,  no monitoring, review, or accountability mechanisms were in place for agent actions

IBM's concurrent data showed that AI-specific breaches cost an average of **$4.80 million per incident**,  higher than the traditional breach average,  and that 60% of AI-related incidents resulted in compromised data while 31% caused operational disruption.

### Why It Happened
- Organizations deployed AI agents faster than governance frameworks could be developed
- Existing IAM and GRC processes did not include AI agents as a governed identity class
- No standard existed for what "secure AI agent deployment" looked like at the enterprise level

### Control Gap in the Lifecycle Model
| Stage | Missing Control |
|---|---|
| Register | AI agents not treated as a formal identity class requiring governance |
| Provision | No security baseline applied at agent deployment |
| Monitor | No human oversight mechanism for agent actions |
| Recertify | No periodic review of whether agent access remained appropriate |
| Retire | No decommissioning process when agents were no longer needed |

### What This Framework Does
- Establishes AI agents as a first-class governed identity,  closing the gap IBM and Adversa AI both identified as the root cause across incidents
- Applies consistent baseline controls at every lifecycle stage
- Creates the human oversight and audit trail mechanisms absent in the documented breaches

**Reference:** [Adversa AI 2025 Security Incidents Report](https://adversa.ai/blog/adversa-ai-unveils-explosive-2025-ai-security-incidents-report-revealing-how-generative-and-agentic-ai-are-already-under-attack/)  
**Reference:** [IBM Cost of a Data Breach 2025](https://newsroom.ibm.com/2025-07-30-ibm-report-13-of-organizations-reported-breaches-of-ai-models-or-applications,-97-of-which-reported-lacking-proper-ai-access-controls)

---

## Summary,  Incident to Control Gap Mapping

| Scenario | Source | Register | Provision | Monitor | Recertify | Retire |
|---|---|:---:|:---:|:---:|:---:|:---:|
| 1. Samsung Shadow AI Leak | Bloomberg/TechCrunch 2023 | X | X | X | | |
| 2. EchoLeak,  M365 Copilot | Aim Security/CVE-2025-32711 | X | X | X | | |
| 3. Shadow AI at Scale | IBM Breach Report 2025 | X | X | X | X | |
| 4. LangChain CVE | DataBahn CVE Report 2025 | X | X | X | | |
| 5. Governance Policy Void | IBM + Adversa AI 2025 | X | X | X | X | X |

> Every documented incident traces back to at least one missing lifecycle control,  and every lifecycle stage is implicated across the five scenarios, validating the framework's coverage.

---

*All incidents are publicly documented. Sources linked above. Last updated: April 2026.*
