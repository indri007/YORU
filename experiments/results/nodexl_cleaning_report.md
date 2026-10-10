# YORU NodeXL Network Cleaning & Normalization Report

Generated per Section 5 Cleaning Rules for Scopus Q1 submission.

| Network ID | Network Name | Original Edges | Duplicates Removed | Invalid Removed | Final Edges | Cleaning Notes |
|---|---|---|---|---|---|---|
| 1 | Attack–Action Network | 9 | 0 | 0 | 9 | Valid empirical experiment trace from 50 adversarial payloads. |
| 2 | Audit Event Network | 8 | 0 | 0 | 8 | Traceable to ausearch / auditd syscall and execve records. |
| 3 | AUID Attribution Network | 5 | 0 | 0 | 5 | Empirical validation over 100 sudo/su/ssh/agent scenarios. |
| 4 | Process–File Network | 6 | 0 | 0 | 6 | Verified file access paths from catalog specifications and audit rules. |
| 5 | Process–Syscall Network | 7 | 0 | 0 | 7 | Process syscall profiling comparing bounded vs unconstrained agents. |
| 6 | User–Action Network | 4 | 0 | 0 | 4 | Catalog authorization schema verified against K01-K10 risk tiers. |
| 7 | Attack Vector Similarity Network | 5 | 0 | 0 | 5 | Deterministic Jaccard similarity calculation across 50 attack payloads. |
| 8 | Injection Propagation Network | 7 | 0 | 0 | 7 | Comparative propagation trace grounded in 50 evaluation trials. |
| 9 | LLM Decision–Action Network | 5 | 0 | 0 | 5 | Catalog and schema validation outputs from testbed benchmarks. |
| 10 | CIS Control Dependency Network | 6 | 0 | 0 | 6 | Parsed directly from catalog/K01.yaml to K10.yaml specifications. |
| 11 | Security Drift Network | 5 | 0 | 0 | 5 | State transition loop grounded in RQ3 before/after trial records. |
| 12 | Rollback Network | 5 | 0 | 0 | 5 | Trial data from RQ3 benchmark with byte-level verification. |
| 13 | Privilege Boundary Network | 5 | 0 | 0 | 5 | Privilege boundary enforced via sudoers drop-in and audit verification. |
| 14 | Temporal Attack Network | 5 | 0 | 0 | 5 | Empirical latency profile synthesized from RQ1, RQ3, and RQ4 trial timestamps. |
| 15 | Master Closed Loop Graph (Architecture) | 6 | 0 | 0 | 6 | Classified strictly as ARCHITECTURE per Scientific Rule #6. |

## Cleaning Invariants Enforced
1. **Zero Self-Loops:** All self-referential edges removed.
2. **Identifier Normalization:** Consistent prefix notation (`V1_`, `AUID_`, `Proc_`, `Kxx`).
3. **Weight Normalization:** Scaled between 0.0 and 1.0 based on empirical rate or indicator.
4. **Zero Missing Provenance:** 100% of empirical edges possess source file and record locator.
