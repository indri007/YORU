#!/usr/bin/env python3
"""
YORU Telegram Terminal & Hermes AI Bridge
Menjalankan perintah terminal & tanya-jawab Hermes AI melalui bot Telegram.
HANYA memproses permintaan dari TELEGRAM_CHAT_ID yang terdaftar.
"""
import asyncio
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

# Jalur konfigurasi
CONFIG_PATHS = [
    Path(__file__).parent.parent / ".yoru.conf.secret",
    Path(__file__).parent.parent / ".env",
    Path("/etc/yoru/yoru.conf")
]

HERMES_BIN = "/Users/jevin/.local/bin/hermes"

def load_config():
    conf = {}
    for p in CONFIG_PATHS:
        if p.exists():
            for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    conf[k.strip()] = v.strip().strip("\"'")
    return conf

config = load_config()
TOKEN = os.environ.get("TELEGRAM_TOKEN", config.get("TELEGRAM_TOKEN", "")).strip()
ALLOWED_CHAT = str(os.environ.get("TELEGRAM_CHAT_ID", config.get("TELEGRAM_CHAT_ID", ""))).strip()

if not TOKEN or not ALLOWED_CHAT:
    print("[ERROR] TELEGRAM_TOKEN atau TELEGRAM_CHAT_ID tidak ditemukan.")
    sys.exit(1)

TELEGRAM_API = "https://api.telegram.org"
BLOCKLIST_INTERACTIVE = {"nano", "vi", "vim", "top", "htop", "less", "more", "man", "watch"}

def send_message(chat_id: str, text: str, parse_mode: str = "Markdown"):
    # Telegram max message length is 4096
    if len(text) > 4000:
        text = text[:3900] + "\n\n... [Output dipotong karena melebihi batas Telegram]"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{TELEGRAM_API}/bot{TOKEN}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        # Fallback without Markdown if parsing error occurs
        try:
            payload2 = json.dumps({"chat_id": chat_id, "text": text}).encode("utf-8")
            req2 = urllib.request.Request(
                f"{TELEGRAM_API}/bot{TOKEN}/sendMessage",
                data=payload2,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req2, timeout=15) as resp2:
                return json.loads(resp2.read().decode())
        except Exception:
            print(f"[ERROR] Gagal kirim pesan: {e}")
            return None

async def execute_shell_command(cmd: str) -> str:
    parts = cmd.strip().split()
    if not parts:
        return "Perintah kosong."
    
    base_cmd = parts[0].lower()
    if base_cmd in BLOCKLIST_INTERACTIVE:
        return f"⚠️ Perintah interaktif `{base_cmd}` tidak didukung karena membutuhkan layar terminal interaktif."

    try:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30.0)
        except asyncio.TimeoutError:
            try:
                proc.kill()
            except ProcessLookupError:
                pass
            return "⏱️ *Waktu habis:* Perintah melebihi batas waktu 30 detik dan telah dihentikan."

        out = stdout.decode("utf-8", errors="replace").strip()
        err = stderr.decode("utf-8", errors="replace").strip()
        code = proc.returncode

        result = []
        if out:
            result.append(out)
        if err:
            result.append(f"[STDERR]\n{err}")
        if not out and not err:
            result.append(f"[Selesai dengan kode status: {code}]")

        return "\n".join(result)
    except Exception as ex:
        return f"❌ Terjadi kesalahan eksekusi: {ex}"

async def query_hermes_ai(prompt: str) -> str:
    if not os.path.exists(HERMES_BIN):
        return "Hermes CLI binary tidak ditemukan di sistem."
    try:
        proc = await asyncio.create_subprocess_exec(
            HERMES_BIN,
            "-z",
            prompt,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=60.0)
        except asyncio.TimeoutError:
            try:
                proc.kill()
            except ProcessLookupError:
                pass
            return "⏱️ *Waktu habis:* Hermes membutuhkan waktu lebih dari 60 detik untuk merespons."

        out = stdout.decode("utf-8", errors="replace").strip()
        err = stderr.decode("utf-8", errors="replace").strip()
        if out:
            return out
        if err:
            return f"Hermes mengembalikan error:\n`{err}`"
        return "Hermes tidak mengembalikan teks jawaban."
    except Exception as ex:
        return f"❌ Gagal menghubungi Hermes Agent: {ex}"

async def handle_update(update: dict):
    msg = update.get("message")
    if not msg:
        return
    chat_id = str(msg.get("chat", {}).get("id", ""))
    text = (msg.get("text") or "").strip()

    # STRICT SECURITY GATE
    if chat_id != ALLOWED_CHAT:
        print(f"[REJECTED] Akses ditolak dari ID: {chat_id}")
        return

    if not text:
        return

    print(f"[INPUT] Dari {chat_id}: {text}")

    if text in ("/start", "/help", "/bantuan"):
        help_text = (
            "🛡️ *[YORU Guardian & Hermes AI]*\n\n"
            "Bot ini memiliki dua mode pintar yang aktif bersamaan:\n\n"
            "1️⃣ *Mode Terminal (Eksekusi OS)*:\n"
            "• `/cmd <perintah>` atau `$ <perintah>`\n"
            "  _Contoh:_ `/cmd uptime`, `/cmd df -h`, `$ git status`\n\n"
            "2️⃣ *Mode Hermes AI (Tanya Jawab)*:\n"
            "• Kirimkan pertanyaan atau kalimat apa saja langsung tanpa awalan!\n"
            "  _Contoh:_ `Halo Hermes, jelaskan apa itu hardening SSH`\n\n"
            "3️⃣ *Perintah Cepat*:\n"
            "• `/status` : Ringkasan kesehatan sistem & disk\n"
            "• `/model` : Info model Hermes aktif\n"
            "• `/ping` : Uji responsivitas bot"
        )
        send_message(chat_id, help_text)
        return

    if text in ("/ping", "ping"):
        send_message(chat_id, "🏓 Pong! Terminal & Hermes AI aktif melayani Anda.")
        return

    if text in ("/model", "model"):
        send_message(chat_id, "🧠 *Model AI Aktif:* Hermes Agent v0.18.0 (Nous Research) ditenagai model penalaran *o3-mini*.")
        return

    if text in ("/status", "status"):
        res = await execute_shell_command("uptime && echo '---' && uname -a && echo '---' && df -h /")
        send_message(chat_id, f"📊 *System Status:*\n```bash\n{res}\n```")
        return

    cmd = None
    if text.startswith("/cmd "):
        cmd = text[5:].strip()
    elif text.startswith("/sh "):
        cmd = text[4:].strip()
    elif text.startswith("$ "):
        cmd = text[2:].strip()

    if cmd:
        send_message(chat_id, f"⏳ *Menjalankan perintah:* `{cmd}` ...")
        output = await execute_shell_command(cmd)
        reply = f"🖥️ *Hasil:* `{cmd}`\n```bash\n{output}\n```"
        send_message(chat_id, reply)
    else:
        # Teks biasa -> Hermes AI
        send_message(chat_id, "🧠 *Hermes sedang menalar pertanyaan Anda...*")
        ai_reply = await query_hermes_ai(text)
        send_message(chat_id, f"🤖 *Hermes AI:*\n\n{ai_reply}")

async def main():
    print(f"[*] YORU Telegram Terminal & Hermes AI Bridge berjalan...")
    print(f"[*] Bot Token terpasang. Chat ID Whitelist: {ALLOWED_CHAT}")
    offset = None
    
    send_message(ALLOWED_CHAT, "⚡ *[Hermes AI & YORU Terminal Terhubung]*\n"
                               "Halo Bu Sari! Hermes Agent (Nous Research) resmi terhubung ke bot ini.\n"
                               "Anda bisa langsung kirim pertanyaan apa saja untuk dijawab AI, "
                               "atau gunakan `/cmd <perintah>` untuk menjalankan terminal!")

    while True:
        try:
            url = f"{TELEGRAM_API}/bot{TOKEN}/getUpdates"
            params = {"timeout": 25, "allowed_updates": ["message"]}
            if offset:
                params["offset"] = offset
            
            data = urllib.parse.urlencode(params).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
            
            resp_data = await asyncio.to_thread(lambda: urllib.request.urlopen(req, timeout=30).read())
            res = json.loads(resp_data.decode("utf-8"))
            
            if res.get("ok"):
                for upd in res.get("result", []):
                    offset = upd["update_id"] + 1
                    await handle_update(upd)
        except Exception as e:
            await asyncio.sleep(2)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Dihentikan.")
