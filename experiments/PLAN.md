# YORU Harness Evaluation Plan & Experimental Protocol

## 1. Overview & Research Questions (RQs)

This evaluation protocol validates the core scientific claims of **YORU Harness**:
1. **Closed-loop kernel accountability** enforced via Linux `auditd` and isolated `AUID`.
2. **End-to-end injection-to-action resistance** against indirect log prompt injection.
3. **Constrained action space safety** across CIS Benchmark Ubuntu 24.04 (K01–K10).
4. **Feasibility on resource-constrained host** (1 vCPU, 1 GB RAM).

### Specific Research Questions:
- **RQ1 (Injection-to-Action Resistance):** Can adversarial prompt injections embedded in untrusted log fields (SSH usernames, web request User-Agents, process arguments) breach the harness to trigger unauthorized privileged execution via `yoructl`?
- **RQ2 (Closed-Loop Attribution Fidelity):** How accurately does the kernel `auditd` subsystem attribute actor identity (`AUID`) across privilege escalation paths (`sudo`, `su -`, SSH, systemd), cleanly differentiating attacker actions (`AUID=1000`) from autonomous agent remediation (`AUID=1001`)?
- **RQ3 (Hardening Efficacy & State Determinism):** Do the 40 discrete primitives of K01–K10 achieve full compliance with zero unexpected service downtime, and can state rollbacks be deterministically executed from `/var/backups/yoru`?
- **RQ4 (System Overhead on Constrained VPS):** What is the CPU, RAM, and Disk I/O footprint of YORU Harness on a budget VPS (1 vCPU, 1 GB RAM) during idle, active auditing, and adversarial log floods (1,000 events/sec)?
- **RQ5 (AI Deliberation Resiliency & Fallback):** How resilient is the LLM deliberation layer against model API failures, latency spikes, and hallucinations under adversarial log inputs?

---

## 2. Experimental Scenarios & Testbed Setup

### Scenario 1: Injection-to-Action Benchmark (RQ1)
- **Dataset:** 50 adversarial log injection payloads derived from recent attack patterns (*Poisoning the Watchtower*, jailbreak templates, delimiter breaking, and instruction overrides) alongside 50 benign logs.
- **Vectors Tested:**
  1. SSH Failed Login username field (`auth.log` / `auditd` `USER_LOGIN`).
  2. HTTP User-Agent / URI parameter in web server access logs.
  3. Process command line arguments (`auditd` `EXECVE` records).
- **Measurement Pipeline:**
  1. Inject payload into system log.
  2. Trigger `yoru-watch` / `yoru-agent`.
  3. Capture LLM response token stream.
  4. Verify whether any unauthorized command was dispatched to `yoructl` or shell.
- **Metrics:**
  - Token-level Attack Success Rate ($ASR_{\text{token}}$): Percentage of times the LLM was coaxed into recommending a malicious action.
  - Action-level Attack Success Rate ($ASR_{\text{action}}$): Percentage of times a malicious action penetrated to OS execution. **Expected: 0.0%**.
  - False Reject Rate ($FRR$): Benign events erroneously blocked.

### Scenario 2: Bilateral Kernel Forensics & AUID Attribution (RQ2)
- **Scenarios:**
  - Standard user login followed by `sudo visudo` or `sudo vim /etc/passwd`.
  - User session escalating via `su -` then editing `/etc/shadow`.
  - SSH key login with direct root access vs unprivileged user + `sudo`.
  - YORU agent autonomous execution of `yoructl K08 terapkan` under user `yoru-agent` (UID 1001, EUID 0).
- **Metrics:**
  - Attribution Accuracy ($Acc_{\text{AUID}}$): Percentage of events where kernel log correctly preserves the original login AUID instead of effective UID.
  - Bilateral Trail Completeness: Ability to construct a complete chain connecting the attacker's trigger event, agent analysis, and subsequent remediation in `/var/log/audit/audit.log`.

### Scenario 3: Hardening Compliance & Rollback Fidelity (RQ3)
- **Scenarios:**
  - Apply CIS baseline K01–K10 across unhardened Ubuntu 24.04 installations.
  - Test autonomous remediation for Safe rules (K03, K07, K08, K09, K10).
  - Test Human-in-the-Loop approval gate for Risky rules (K01, K02, K04, K05, K06).
  - Induce simulated configuration failure and execute `yoructl <Kxx> kembalikan`.
- **Metrics:**
  - Compliance Score (pre-remediation vs post-remediation, 0 to 10 scale).
  - Rollback Success Rate: Verification that system config and service state return to 100% byte-for-byte exact original state.

### Scenario 4: Performance & System Footprint (RQ4)
- **Scenarios:**
  - Idle baseline (systemd timer waiting).
  - Active inspection cycle (evaluating 10 controls).
  - High stress audit log flood (1,000 events/second using `auditctl` stress tools).
- **Metrics:**
  - Peak & Average RAM Usage (RSS in MB). Target: < 50 MB.
  - Average CPU Utilization (%). Target: < 1.0% idle, < 5.0% during inspection.
  - Disk I/O Write rate (KB/sec) and daily log growth (MB/day).

### Scenario 5: LLM Proxy Resiliency (RQ5)
- **Scenarios:**
  - Primary API simulation: Timeout (5s), HTTP 429 (Rate Limit), HTTP 500 (Server Error).
  - Fallback activation to local or secondary model.
  - Fail-safe fallback to static rule catalog when all AI APIs are unreachable.
- **Metrics:**
  - Fallback Success Rate (%): Percentage of successful inspections completed despite primary model failure.
  - Mean Latency per Inspection Cycle (seconds).

---

## 3. Baselines & Comparative Analysis

| Baseline | Description | Role in Evaluation |
|---|---|---|
| **Raw Auditd + ausearch** | Native Linux auditing without LLM or automated remediation | Establishes ground truth logging baseline |
| **Wazuh Agent (HIDS)** | Traditional enterprise HIDS agent running CIS rootcheck | Compares resource overhead, alert noise, and remediation model |
| **Falco (eBPF)** | Modern kernel runtime security engine | Compares syscall detection latency and resource consumption |
| **Unconstrained LLM Agent** | Baseline agent with direct `/bin/bash` tool execution | Demonstrates vulnerability to prompt injection vs YORU Harness |

---

## 4. Test Environment Specification

- **Target Operating System:** Ubuntu 24.04 LTS (Noble Numbat)
- **Kernel Version:** Linux 6.8.0+
- **Audit Subsystem:** `auditd` 3.1.2+, `audispd-plugins`
- **Hardware Profile (Target VPS):** 1 vCPU, 1024 MB RAM, 20 GB NVMe Storage
- **Secondary Multi-Core Profile:** 2 vCPU, 4096 MB RAM (Multipass / KVM testbed)

---

## 5. Artifacts and Output Files

All raw experimental logs and metrics will be saved in structured formats:
- `experiments/results/rq1_injection_results.json`
- `experiments/results/rq2_auid_attribution.csv`
- `experiments/results/rq3_hardening_determinism.json`
- `experiments/results/rq4_resource_overhead.csv`
