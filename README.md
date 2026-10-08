<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/banner-dark.svg">
  <img alt="YORU Banner" src="./assets/banner-light.svg">
</picture>

# YORU: Linux Security Auditing & Forensics

> OS-enforced security harness for Linux AI agents: Closed-loop kernel accountability, constrained CIS action space, and end-to-end injection-to-action defense.

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](#license)
[![Platform](https://img.shields.io/badge/Platform-Ubuntu%2024.04-orange.svg)](#quick-start)
[![Static Validation](https://img.shields.io/badge/Static%20Validation-PASS-brightgreen.svg)](#-validation-status)
[![Runtime Validation](https://img.shields.io/badge/Runtime%20Validation-Pending-yellow.svg)](#-validation-status)


## 🚨 The Incident
It’s 3 AM. Your server's critical configuration was altered. You check the logs, but the actor appears as `root`. Was it an automated script? An attacker? A junior developer who `sudo su`'d into root? You have no idea because the original identity is masked. The forensic trail is gone.

## 💡 Why YORU Exists (The Problem)
* **Forensics Lost After `sudo`:** Standard logging masks the original actor's identity once they switch to root.
* **Alert Fatigue & Noise:** Too many logs make it impossible to separate critical changes from regular system noise.
* **Lack of Context & Agent Vulnerability:** Traditional audit logs are cryptic, while giving an LLM direct shell access creates dangerous indirect prompt injection vectors.
* **Resource Constraints:** Small teams lack a dedicated Security Operations Center (SOC) to monitor endpoints 24/7.

## 🛠️ The Solution (YORU Harness)
| The Problem | The YORU Answer |
| --- | --- |
| Forensic trail lost after `sudo` | **Closed-Loop Kernel Accountability:** Extracts the Audit User ID (`auid`) at the kernel layer, tracking both attacker and agent interventions separately. |
| Prompt injection via untrusted logs | **Constrained Action Space:** The AI cannot run shell commands; it can only invoke 40 discrete CIS primitives via `yoructl` with human approval for risky actions. |
| Cryptic Logs & Alert Noise | **Targeted K01–K10 CIS Catalog & Resilient AI Proxy:** Hardened path monitoring with automated fail-safe fallback. |
| No Dedicated SOC | **Automated Systemd Watcher:** Lightweight guard (< 50MB RAM, < 1% CPU) suited for budget VPS deployments. |

## 🌟 Key Features
* **Constrained Action Space:** 40 discrete CIS Ubuntu 24.04 primitives (`yoructl <K01..K10> <periksa|terapkan|kembalikan|verifikasi>`).
* **Closed-Loop Kernel Forensics:** `auditd` rules monitoring both critical config drift and agent execution via dedicated AUID.
* **Injection-to-Action Defense:** Eliminates arbitrary shell execution, isolating untrusted log inputs.
* **Systemd Managed:** `yoru-watch.service` & `yoru-watch.timer` for scheduled inspection.
* **Web Dashboard:** `yoru-web.service` powered by FastAPI.
* **Resilient AI Proxy:** `yoru-model-proxy` with primary and fallback model routing.

## ⚙️ How It Works

```mermaid
flowchart LR
    A[Linux Kernel auditd] -->|Log Event| B(Untrusted Input Sanitizer)
    B -->|Structured Context| C{LLM Deliberation Engine}
    C -->|Choose Discrete Action| D[Action Gatekeeper / Approval]
    D -->|sudo yoructl Kxx verb| E[yoructl Dispatcher]
    E -->|Closed-Loop Audit Hook auid=1001| A
```

## 🚀 Quick Start
### Prerequisites
- Ubuntu 24.04
- `auditd`, `audispd-plugins`, `python3`

### Installation
```bash
git clone https://github.com/indri007/YORU.git
cd YORU
sudo ./install.sh
```

*(Try on macOS via Multipass)*
```bash
multipass launch 24.04 --name yoru-a --cpus 2 --memory 4G
multipass mount ./ yoru-a:/home/ubuntu/yoru
multipass exec yoru-a -- bash -lc 'cd /home/ubuntu/yoru && sudo ./install.sh'
```

## 📊 Validation Status
| Item | Status | Evidence |
| --- | --- | --- |
| Static Validation (Shell, Python, Git) | **PASS** | `docs/LINUX_RUNTIME_TEST.md` |
| Linux auditd | *PENDING* (Needs Ubuntu 24.04) | TBD |
| K08 Runtime | *PENDING* | TBD |
| AUID Forensic | *PENDING* | TBD |
| yoru-watch.service | *PENDING* | TBD |
| yoru-web.service | *PARTIAL PASS* (macOS app-level) | TBD |
| yoru-model-proxy | *PARTIAL PASS* (Error handling) | TBD |

## 📂 Project Structure
- `bin/`: Executables (`yoru-agent`, `yoructl`, `yoru-model-proxy`).
- `catalog/`: Control YAML definitions (K01-K10).
- `systemd/`: Daemons (`yoru-watch.service`, `yoru-web.service`).
- `web/`: Dashboard application.
- `docs/`: Extensive documentation.

## 📖 Documentation
- [PRD (Product Requirements)](docs/PRD.md)
- [ERD (Entity-Relationship)](docs/ERD.md)
- [Schema](docs/SCHEMA.md)
- [Detection Rules](docs/RULES.md)
- [UI/UX Guide](docs/UI-UX.md)
- [Usage Guide](docs/USAGE.md)

## 🇮🇩 Ringkasan Bahasa Indonesia
YORU Harness adalah lapisan pengendali (*governance harness*) keamanan Linux berbasis kernel untuk agen otonom LLM pada Ubuntu 24.04. YORU menggabungkan tiga pilar inovasi:
1. **Closed-Loop Kernel Accountability:** Kernel Linux (`auditd`) merekam aksi penyerang sekaligus tindakan remediasi agen AI secara independen dengan AUID terisolasi.
2. **Evaluasi Injection-to-Action End-to-End:** Menguji ketahanan prompt injection pada log tak tepercaya langsung hingga level eksekusi OS, bukan sekadar respons token bahasa.
3. **Ruang Aksi Tertutup (*Constrained Action Space*):** Menghilangkan shell interpreter bebas dan membatasi aksi agen hanya pada 40 primitif CIS Benchmark (`yoructl K01..K10`), dirancang hemat daya (< 50MB RAM, < 1% CPU) untuk VPS UMKM.

## License
MIT License. See [LICENSE](LICENSE) for details.
