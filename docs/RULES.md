# Detection Rules

YORU organizes its core security auditing through a catalog of rules (K01 to K10).

## Implemented Rules
All active rules are defined in the `catalog/` directory as YAML definitions.

- **K01-K07, K09-K10:** (See corresponding `catalog/K*.yaml` for exact paths and syscalls monitored).
- **K08: Auditd Path Monitoring**
  - **Source:** `catalog/K08.yaml`
  - **Severity:** High
  - **Audit Key:** `yoru_kontrol`
  - **What is monitored:** Critical system files:
    - `/etc/passwd`
    - `/etc/shadow`
    - `/etc/group`
    - `/etc/sudoers`
    - `/etc/ssh/sshd_config`
    - `/etc/ufw/`
  - **Example Trigger:** A user runs `sudo visudo`. The audit daemon logs a `SYSCALL` with `key=yoru_kontrol`.
  
### Known False Positives
Automated system updates (e.g., `apt-get upgrade` modifying `/etc/passwd` or `/etc/shadow`).

### Tuning
Exclude package manager AUIDs if desired, though logging them provides a complete trail.

## Planned Rules
- **K11+**: Planned for future releases (TBD).

## Adding New Rules
1. Define the path or syscall in an `auditd` format.
2. Ensure the key uses the convention `yoru_<rule_name>`.
3. Add it to the YAML catalog in the `catalog/` directory.
