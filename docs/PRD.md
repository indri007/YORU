# Product Requirements Document (PRD)

## Overview
YORU is a lightweight Linux security auditing tool designed to track critical configuration changes and provide AI-assisted attribution for system administrators and small security teams.

## Problem Statement
When a user escalates privileges via `sudo` or `su` and modifies a critical system file, standard logging often attributes the action to `root`. This loss of forensic trail makes it difficult to hold individuals accountable. Additionally, raw `auditd` logs are verbose and difficult to interpret without specialized knowledge.

## Goals
- Attribute critical file modifications to the authenticated user via `auid` (runtime validation pending).
- Run autonomously as a lightweight `systemd` daemon.
- Provide a human-readable dashboard and alert system.
- Ensure resilience against environment failures (e.g., AI proxy fallbacks).

## Non-Goals
- Full Endpoint Detection and Response (EDR) capabilities.
- Real-time network traffic interception.
- Support for non-Linux operating systems (e.g., Windows, macOS) in production.

## Target Personas
1. **System Administrator:** Needs to know who changed a configuration file when something breaks.
2. **SOC Analyst:** Requires high-signal alerts.
3. **Auditor/Researcher:** Demands reproducible evidence of compliance controls (e.g., K08 rules).

## User Stories
- *As a sysadmin, I want to see the original username of the person who edited `/etc/passwd` so that I can hold them accountable even if they used `sudo`.*
- *As a SOC analyst, I want to view a dashboard of recent security events so I can quickly assess the health of my fleet.*

## Requirements
- **FR-01:** The system MUST parse `auditd` logs to extract `auid`.
- **FR-02:** The system MUST be manageable via `systemd` (`yoru-watch.service`, `yoru-web.service`).
- **FR-03:** The AI proxy MUST support fallback models if the primary model is unavailable.

## Security & Privacy
- The system must NOT expose sensitive credentials in logs or dashboards.
- API keys must be securely stored (e.g., `/etc/yoru/web.env` with `600` permissions).
