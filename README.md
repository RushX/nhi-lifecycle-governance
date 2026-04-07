# AI Agent Identity Lifecycle Governance Framework
> Governance, risk controls, and lifecycle enforcement for AI agent identities in the enterprise.

![Status](https://img.shields.io/badge/status-in%20progress-yellow)
![Framework](https://img.shields.io/badge/framework-NIST%20AI%20RMF-blue)
![Standard](https://img.shields.io/badge/standard-ISO%2042001-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🧭 Overview

Enterprises are deploying AI agents: copilots, autonomous services, MCP servers, custom GPTs at rapid scale. Unlike traditional software, these agents act autonomously, hold persistent access to sensitive systems, and make decisions at machine speed.

Yet most organizations have **no formal identity lifecycle governance** for them.

This project addresses that gap by treating AI agents as a **distinct identity class**, applying the same joiner-mover-leaver discipline used for human identities, extended to the unique risk profile of autonomous agents.

**This repository contains:**
- A 5-stage AI agent identity lifecycle model
- A compliance control mapping (NIST AI RMF, ISO 42001, SOC 2)
- A quantitative risk scoring model for agent classification
- Policy templates for registration, provisioning, and retirement
- A working prototype: agent registry API with lifecycle enforcement and audit logging

---

## ❗ The Problem

Traditional IAM and IGA platforms were designed for humans. When AI agents enter the enterprise, they create governance blind spots that existing tooling cannot address:

| Problem | Impact |
|---|---|
| No centralized agent registry | No visibility into what agents exist or who owns them |
| Ad-hoc provisioning with broad permissions | Violation of least-privilege; audit exposure |
| No recertification process | Access drift; stale entitlements persist indefinitely |
| Orphaned agents after owner departure | Unowned identities with live access to sensitive systems |
| No audit trail
