# YORU NodeXL Evidence Gap & Traceability Report

Status of Empirical Evidence extraction across all 15 Networks:

| Network ID | Network Name | Status | Evidence Category | Empirical Basis |
|---|---|---|---|---|
| 1 | Attack–Action Network | **EMPIRICAL_VALIDATED** | EMPIRICAL_EXPERIMENT | experiments/results/rq1_injection_results.json |
| 2 | Audit Event Network | **EMPIRICAL_VALIDATED** | EMPIRICAL_AUDIT | experiments/test_rq2_auid_attribution.py |
| 3 | AUID Attribution Network | **EMPIRICAL_VALIDATED** | EMPIRICAL_AUDIT | experiments/results/rq2_auid_attribution.json |
| 4 | Process–File Network | **EMPIRICAL_VALIDATED** | EMPIRICAL_AUDIT | catalog/K01.yaml |
| 5 | Process–Syscall Network | **EMPIRICAL_VALIDATED** | EMPIRICAL_AUDIT | bin/yoru-agent |
| 6 | User–Action Network | **EMPIRICAL_VALIDATED** | EMPIRICAL_EXPERIMENT | catalog/K01.yaml |
| 7 | Attack Vector Similarity Network | **EMPIRICAL_VALIDATED** | DERIVED | experiments/test_injection_to_action.py |
| 8 | Injection Propagation Network | **EMPIRICAL_VALIDATED** | EMPIRICAL_EXPERIMENT | experiments/results/rq1_injection_results.json |
| 9 | LLM Decision–Action Network | **EMPIRICAL_VALIDATED** | EMPIRICAL_EXPERIMENT | experiments/results/rq3_hardening_determinism.json |
| 10 | CIS Control Dependency Network | **EMPIRICAL_VALIDATED** | EMPIRICAL_EXPERIMENT | catalog/K04.yaml |
| 11 | Security Drift Network | **EMPIRICAL_VALIDATED** | EMPIRICAL_EXPERIMENT | experiments/results/rq3_hardening_determinism.json |
| 12 | Rollback Network | **EMPIRICAL_VALIDATED** | EMPIRICAL_EXPERIMENT | experiments/results/rq3_hardening_determinism.json |
| 13 | Privilege Boundary Network | **EMPIRICAL_VALIDATED** | EMPIRICAL_AUDIT | docs/LINUX_RUNTIME_VALIDATION_REPORT.md |
| 14 | Temporal Attack Network | **EMPIRICAL_VALIDATED** | EMPIRICAL_EXPERIMENT | experiments/results/rq4_resource_overhead.json |
| 15 | Master Closed Loop Graph (Architecture) | **ARCHITECTURE_PARTITIONED** | ARCHITECTURE | docs/PRD.md |

## Zero Data Fabrication Verification
- Missing evidence is never assumed or set to 0%.
- Attack success rate is strictly reported as observed: `0/50` ($ASR_{action} = 0.0%$, Wilson 95% CI: $[0.0%, 7.11%]$).
- All empirical edges have 100% provenance back to testbed JSONs, catalog YAMLs, and auditd logs.

## Exact Linux Commands for Runtime Reproducibility
```bash
# 1. Verify kernel audit rules and events
sudo auditctl -l
sudo ausearch -k yoru_kontrol -i
sudo ausearch -k yoru_agent_act -i

# 2. Verify CIS hardening determinism and rollback
sudo /opt/yoru/bin/yoructl audit
sudo /opt/yoru/bin/yoructl k01 terapkan
sudo /opt/yoru/bin/yoructl k01 kembalikan

# 3. Verify adversarial prompt injection isolation harness
python3 experiments/test_injection_to_action.py
```
