# YORU Evaluation Plan

## 1. Research Questions (RQs)
- **RQ1:** How accurately does YORU detect critical activities (K01–K10) without generating excessive false positives?
- **RQ2:** How reliable is AUID-based actor attribution after privilege escalation (`sudo`, `su`, `ssh`)?
- **RQ3:** What is the system overhead introduced by YORU?
- **RQ4:** How accurate, factual, and resilient is the AI proxy summary mechanism?

## 2. Experimental Scenarios
### RQ1: Detection Accuracy (K01-K10)
- **Malicious/Anomalous (Positive):** 50 scripted privilege escalations, config file edits (e.g., `/etc/passwd`), and unauthorized executions.
- **Normal (Negative):** 50 standard user actions, including package updates (`apt-get upgrade`) to trigger known false positives.
- **Metrics:** Precision, Recall, F1-Score, False Positive Rate (FPR) per rule.

### RQ2: Attribution Reliability (AUID)
- **Scenarios:** Users escalating via `sudo`, `sudo -i`, `su -`, SSH logins, cron jobs, and systemd services.
- **Metrics:** Attribution Accuracy (percentage of times the correct original user ID is extracted vs. effective user ID).

### RQ3: System Overhead
- **Scenarios:** Idle state vs. High load (1000 events/sec).
- **Baselines:** System without YORU, system with raw `auditd`, system with Wazuh/Falco.
- **Metrics:** CPU Usage (%), RAM (MB), Disk I/O (MB/s), Log Size (MB/hr).

### RQ4: AI Proxy Efficacy
- **Scenarios:** Process 100 complex audit logs through the LLM.
- **Metrics:** Factuality (vs. ground truth), Hallucination Rate, Latency (ms/req), Cost ($/req), Fallback Success Rate (simulating primary API outage).
- **Evaluation:** Evaluated by $\ge$ 2 human raters using Cohen's kappa for inter-rater agreement.

## 3. Baselines & Ablation Studies
- **Baselines:** Raw `auditd` + `ausearch`, Falco, Wazuh.
- **Ablation 1:** YORU without AI summarization.
- **Ablation 2:** YORU without AUID enrichment.

## 4. Environment
- **OS:** Ubuntu 24.04 LTS
- **Auditd Version:** `[DATA PENDING]`
- **YORU Commit:** `[DATA PENDING]`
- **Hardware:** `[DATA PENDING: e.g., 2 vCPU, 4GB RAM]`

## 5. Automated Scripts
- A suite of bash scripts to replay audit events and collect `dstat` / `top` metrics into CSV files (located in `experiments/scripts/` - TBD).
