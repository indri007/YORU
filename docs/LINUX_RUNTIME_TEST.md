# Linux Runtime Test Plan untuk YORU (VM `yoru-a`)

Dokumen ini berisi langkah-langkah pengujian yang **HARUS** dijalankan secara langsung di server Linux atau VM `yoru-a`. 

1. **OS/version**
   ```bash
   cat /etc/os-release
   # Harapkan: Ubuntu 24.04 LTS
   ```

2. **auditd status**
   ```bash
   systemctl is-active auditd
   systemctl is-enabled auditd
   # Harapkan: active, enabled
   ```

3. **auditctl availability**
   ```bash
   which auditctl
   # Harapkan: /usr/sbin/auditctl (atau path valid)
   ```

4. **augenrules validation**
   ```bash
   sudo augenrules --check
   # Pastikan tidak ada konflik. zz-yoru-k08.rules harus dimuat terakhir dan menimpa audit.rules (-D)
   ```

5. **K08 rule loading**
   ```bash
   sudo auditctl -l | grep -c '^-w'
   # Harapkan: >= 12
   ```

6. **exact rule validation**
   ```bash
   sudo auditctl -l
   # Validasi secara manual keberadaan path: /etc/passwd, /etc/shadow, /etc/sudoers, ufw, dan kontrol perlindungan Yoru.
   ```

7. **auid validation**
   ```bash
   touch /etc/sysctl.d/99-yoru-k10.conf
   sudo ausearch -k yoru_kontrol -i --start recent | tail -20
   # Harapkan: Log berisi `auid=` dari pengguna login asli (misal yoru), bukan `uid=root`.
   ```

8. **yoru-watch.service**
   ```bash
   systemctl status yoru-watch.service
   # Pastikan tidak ada error permission terkait ketiadaan /home jika `ProtectHome=yes` dihindari.
   ```

9. **yoru-watch.timer**
   ```bash
   systemctl status yoru-watch.timer
   # Pastikan timer aktif dan jadwal RandomizedDelaySec terlihat.
   ```

10. **journal logs**
    ```bash
    journalctl -b -t systemd-journald | grep "max "
    # Harapkan: pagu log 500M sesuai K09.
    ```

11. **drift detection**
    ```bash
    # Lakukan perubahan pada port SSH, lalu tunggu/jalankan yoru-watch
    # Harapkan: mendeteksi port berubah dan memunculkan auid pengubah.
    ```

12. **restore test**
    ```bash
    # Uji restorasi Yoru via yoructl atau Hermes untuk kontrol yang dideteksi drift
    ```

13. **Hermes notification test**
    ```bash
    # Verifikasi notifikasi terkirim via Telegram / webhook dari hasil drift detection.
    ```

14. **check-all.sh final result**
    ```bash
    sudo bash check-all.sh
    # Harapkan: Semua cek LULUS tanpa error syntax.
    ```
