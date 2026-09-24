# Usage Guide

## Daily Operations
Check the health of your watch timer:
```bash
systemctl status yoru-watch.timer
```

View the latest translated AI alerts from the proxy:
```bash
journalctl -u yoru-web.service -n 50
```

## Investigating an Incident (AUID)
If you notice an anomaly, query the audit daemon:
```bash
sudo ausearch -k yoru_kontrol -i
```
Look at the `auid` field. The `auid` is designed to point to the specific user account that logged in.

## Troubleshooting
- **Model Proxy Fails:** Ensure `GEMINI_API_KEY` is exported or exists in `/etc/yoru/web.env`.
- **Timer Doesn't Fire:** Ensure the timer was enabled with `sudo systemctl enable --now yoru-watch.timer`.
- **macOS Multipass Launch Fails:** If you encounter `qemu-img Process crashed` on Apple Silicon, this is a known compatibility issue. Try an alternative like UTM (Ubuntu Server 24.04 ARM64 ISO) or use a standard VPS Ubuntu 24.04. Avoid Docker or Codespaces as they are not representative for `auditd` and full `systemd` functionality.
