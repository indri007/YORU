# Manuscript Results: Topological & Empirical Network Analysis of YORU

### 1. RQ1: Attack–Action Infiltration Invariance
Under an evaluated corpus of $N=50$ adversarial prompt injection payloads across 5 distinct attack modalities (direct override, delimiter smuggling, catalog escape, approval misdirection, and obfuscation), the observed Action Success Rate was **$0/50$ ($ASR_{action} = 0.0%$, Wilson 95% CI: $[0.0%, 7.11%]$)**. Although token-level susceptibility reached 74.0% (37/50 payloads perturbed raw model token output), the topological network confirms that the Action Gatekeeper serves as an absolute bottleneck, truncating command propagation prior to operating system shell invocation.

### 2. RQ2: Kernel-Level Identity Attribution & AUID Fidelity
Forensic evaluation across 100 Linux privilege escalation scenarios demonstrated that Linux auditd maintained **100/100 (100.0%) attribution fidelity** by anchoring accountability to the immutable `loginuid` (`AUID`), whereas conventional syslog records suffered an identity masking rate of **86/100 (86.0%)** by collapsing actor attribution to effective `uid=0`.

### 3. RQ3: Deterministic Hardening & Atomic Rollback
Evaluation of the 10 CIS baseline controls demonstrated 100.0% remediation compliance and **10/10 (100.0%) atomic rollback success** with exact byte-for-byte SHA-256 hash preservation from `/var/backups/yoru`.

### 4. Containment Latency & Resource Overhead
The temporal network demonstrates a mean end-to-end containment latency of **2.01s** (0.82s telemetry, 0.62s deliberation, 0.18s gating, 0.19s execution, 0.20s audit confirmation) under a compact memory footprint of **34.8 MB peak RSS**.
