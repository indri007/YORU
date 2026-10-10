#!/usr/bin/env bash
# ==============================================================================
# YORU 24/7 Google Cloud Deployment Script
# Mengotomatiskan pemasangan YORU Telegram Bot & Hermes AI di Google Cloud (Ubuntu)
# ==============================================================================
set -euo pipefail

echo "=================================================="
echo "    YORU 24/7 GOOGLE CLOUD VM DEPLOYMENT SETUP    "
echo "=================================================="

# 1. Update paket & dependensi dasar
echo "[1/5] Memperbarui sistem dan dependensi Python..."
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv git curl

# 2. Direktori kerja
INSTALL_DIR="/opt/yoru"
echo "[2/5] Menyiapkan direktori aplikasi di ${INSTALL_DIR}..."
sudo mkdir -p "${INSTALL_DIR}"
sudo chown -R "$USER:$USER" "${INSTALL_DIR}"

if [ ! -d "${INSTALL_DIR}/.git" ]; then
    git clone https://github.com/indri007/YORU.git "${INSTALL_DIR}"
else
    cd "${INSTALL_DIR}" && git pull origin main
fi

cd "${INSTALL_DIR}"

# 3. Kredensial Environment (Input Interaktif jika belum ada .env)
echo "[3/5] Memeriksa file environment .env..."
if [ ! -f "${INSTALL_DIR}/.env" ]; then
    echo "Masukkan kredensial Telegram & AI (atau tekan enter untuk menggunakan nilai env):"
    read -rp "Telegram Bot Token : " IN_TG_TOKEN
    read -rp "Telegram Chat ID   : " IN_TG_CHAT
    read -rp "OpenAI / AI Key    : " IN_AI_KEY

    cat << EOF > "${INSTALL_DIR}/.env"
TELEGRAM_TOKEN="${IN_TG_TOKEN:-}"
TELEGRAM_CHAT_ID="${IN_TG_CHAT:-}"
OPENAI_API_KEY="${IN_AI_KEY:-}"
EOF
    chmod 600 "${INSTALL_DIR}/.env"
fi

if [ ! -f "${INSTALL_DIR}/.yoru.conf.secret" ]; then
    source "${INSTALL_DIR}/.env"
    cat << EOF > "${INSTALL_DIR}/.yoru.conf.secret"
NAMA_SERVER="GCP-Production-24h"
TELEGRAM_TOKEN="${TELEGRAM_TOKEN}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID}"
ZONA_WAKTU="Asia/Jakarta"
EOF
    chmod 600 "${INSTALL_DIR}/.yoru.conf.secret"
fi

chmod +x "${INSTALL_DIR}/bin/yoru-terminal.py"

# 4. Buat systemd service agar jalan 24 jam nonstop
echo "[4/5] Memasang daemon service Systemd (yoru-bot.service)..."
sudo tee /etc/systemd/system/yoru-bot.service > /dev/null << EOF
[Unit]
Description=YORU Telegram & Hermes 24/7 Security Daemon
After=network.target

[Service]
Type=simple
User=${USER}
WorkingDirectory=${INSTALL_DIR}
EnvironmentFile=${INSTALL_DIR}/.env
ExecStart=/usr/bin/python3 ${INSTALL_DIR}/bin/yoru-terminal.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# 5. Aktifkan & Jalankan
echo "[5/5] Mengaktifkan dan menyalakan layanan 24 jam..."
sudo systemctl daemon-reload
sudo systemctl enable yoru-bot.service
sudo systemctl restart yoru-bot.service

echo "=================================================="
echo "✅ BERHASIL! Layanan YORU 24/7 aktif di Google Cloud."
echo "Status service:"
sudo systemctl status yoru-bot.service --no-pager || true
echo "=================================================="
echo "Silakan periksa chat Telegram @Mrs007_bot di HP Anda!"
