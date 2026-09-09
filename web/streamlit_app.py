import streamlit as st
import sqlite3
import json
import pandas as pd
from pathlib import Path
import time
import requests

# Layout config
st.set_page_config(
    page_title="Hermes by Yoru",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown("""
<style>
    .metric-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 24px;
        text-align: center;
        border: none;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
        color: #1d1b20;
    }
    .score-high { color: #146c2e; font-size: 56px; font-weight: 800; letter-spacing: -1px; }
    .score-med { color: #b3261e; font-size: 56px; font-weight: 800; letter-spacing: -1px; }
    .score-low { color: #b3261e; font-size: 56px; font-weight: 800; letter-spacing: -1px; }
    
    .drift-alert {
        background-color: #fce8e8;
        border-left: 6px solid #b3261e;
        padding: 18px;
        border-radius: 12px;
        margin-bottom: 16px;
        color: #1d1b20;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .control-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 18px;
        border-radius: 16px;
        margin-bottom: 12px;
        color: #1d1b20;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .control-card:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

DB_PATH = Path(__file__).resolve().parent / "yoru.db"
API_URL = "http://127.0.0.1:8000/api/keputusan"

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        st.error(f"Gagal koneksi database: {e}")
        return None

def fetch_latest_report():
    conn = get_db_connection()
    if not conn: return None
    try:
        cur = conn.execute("SELECT isi FROM laporan ORDER BY diterima DESC LIMIT 1")
        row = cur.fetchone()
        if row:
            return json.loads(row["isi"])
    except Exception as e:
        st.error(f"Error reading report: {e}")
    finally:
        conn.close()
    return None

def send_decision(server, kontrol, nilai):
    try:
        # Instead of going through HTTP API for demo, we can just insert to DB directly to avoid port issues
        # But for best practice, let's use the DB directly since this is local demo
        conn = get_db_connection()
        if conn:
            conn.execute("""INSERT INTO keputusan (server, kontrol, nilai, catatan, dibuat, diambil)
                             VALUES (?,?,?,?,?,0)
                             ON CONFLICT(server, kontrol) DO UPDATE SET
                               nilai=excluded.nilai, catatan=excluded.catatan,
                               dibuat=excluded.dibuat, diambil=0""",
                          (server, kontrol, nilai, "", time.time()))
            conn.commit()
            conn.close()
            st.toast(f"Keputusan untuk {kontrol} disimpan: {nilai}!", icon="✅")
    except Exception as e:
        st.error(f"Gagal menyimpan: {e}")

def init_mock_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        # Check if table exists and has data
        try:
            count = conn.execute("SELECT COUNT(*) FROM laporan").fetchone()[0]
            if count > 0:
                conn.close()
                return
        except sqlite3.OperationalError:
            pass # Table doesn't exist

        # Create table and insert mock data
        conn.execute("""CREATE TABLE IF NOT EXISTS laporan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            server TEXT NOT NULL,
            waktu TEXT NOT NULL,
            siklus TEXT NOT NULL,
            skor INTEGER NOT NULL,
            isi TEXT NOT NULL,
            diterima REAL NOT NULL)""")
        
        conn.execute("""CREATE TABLE IF NOT EXISTS keputusan (
            server TEXT NOT NULL,
            kontrol TEXT NOT NULL,
            nilai TEXT NOT NULL,
            catatan TEXT,
            dibuat REAL NOT NULL,
            diambil INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (server, kontrol))""")
            
        repo_dir = Path(__file__).resolve().parent.parent
        for berkas in ["report-fix.json", "report-watch.json"]:
            file_path = repo_dir / "examples" / berkas
            if file_path.exists():
                d = json.loads(file_path.read_text(encoding="utf-8"))
                conn.execute(
                    "INSERT INTO laporan (server, waktu, siklus, skor, isi, diterima) VALUES (?,?,?,?,?,?)",
                    (str((d.get("server") or {}).get("nama") or "contoh"),
                     str(d.get("waktu")), str(d.get("siklus")),
                     int((d.get("ringkasan") or {}).get("skor") or 0),
                     json.dumps(d, ensure_ascii=False), time.time()),
                )
        conn.commit()
        conn.close()
    except Exception as e:
        print("Mock DB Init Error:", e)

init_mock_db()
report = fetch_latest_report()

if not report:
    st.warning("Belum ada laporan yang masuk. Jalankan agent terlebih dahulu.")
    st.stop()

server_info = report.get("server", {})
server_name = server_info.get("nama", "tanpa-nama")
summary = report.get("ringkasan", {})
score = summary.get("skor", 0)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/artificial-intelligence.png", width=60)
    st.title("Hermes")
    st.caption("AI Agent Penjaga Server")
    st.divider()
    st.write(f"**Server:** {server_name}")
    st.write(f"**OS:** {server_info.get('os', '-')}")
    st.write(f"**IP:** {server_info.get('ip_utama', '-')}")
    st.write(f"**Siklus:** {report.get('siklus', '-')}")
    
    st.divider()
    st.markdown("### Status Ringkasan")
    col1, col2, col3 = st.columns(3)
    col1.metric("Aman", summary.get("lulus", 0))
    col2.metric("Bahaya", summary.get("gagal", 0))
    col3.metric("Lewat", summary.get("dilewati", 0))

# Main UI
st.title("🛡️ Dashboard Keamanan Server")

# Score and Metrics
score_class = "score-high" if score >= 80 else "score-med" if score >= 50 else "score-low"
st.markdown(f"""
<div class="metric-card">
    <h3>Skor Keamanan</h3>
    <div class="{score_class}">{score}/100</div>
    <p>Diperiksa terakhir: {report.get('waktu', '-').replace('T', ' ')}</p>
</div>
<br>
""", unsafe_allow_html=True)

# Tabs
tab_action, tab_controls, tab_chat = st.tabs(["⚠️ Action Center", "📋 Semua Kontrol", "💬 Chat dengan Hermes"])

with tab_action:
    st.header("Tindakan Diperlukan")
    
    drifts = report.get("drift", [])
    if drifts:
        st.subheader("🚨 Ada yang berubah di server kamu")
        for drift in drifts:
            with st.container():
                st.markdown(f"""
                <div class="drift-alert">
                    <h4>{drift.get('nama')} ({drift.get('id')})</h4>
                    <p><s>{drift.get('berubah_dari')}</s> ➡️ <b>{drift.get('berubah_jadi')}</b></p>
                    <p><i>Diubah oleh <b>{drift.get('siapa', 'Unknown')}</b> pada {drift.get('kapan_diubah', '-')} lewat <code>{drift.get('perintah', '-')}</code></i></p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Itu memang saya (Izinkan)", key=f"sah_{drift['id']}", type="primary"):
                        send_decision(server_name, drift['id'], 'sah')
                with col2:
                    if st.button("Kembalikan seperti semula", key=f"rev_{drift['id']}"):
                        send_decision(server_name, drift['id'], 'kembalikan')
    else:
        st.success("Tidak ada perubahan tak terduga (drift) terdeteksi.")
        
    butuh_keputusan = set(report.get("butuh_keputusan", []))
    kontrols = report.get("kontrol", [])
    pending_controls = [k for k in kontrols if k['id'] in butuh_keputusan and k['id'] not in [d['id'] for d in drifts]]
    
    if pending_controls:
        st.subheader("Menunggu Persetujuan Anda")
        for k in pending_controls:
            with st.expander(f"{k['status']} - {k['nama']} ({k['id']})", expanded=True):
                st.write(f"**Target:** {k['nilai_terbaca']} ➡️ {k['nilai_target']}")
                st.write(f"**Kenapa:** {k.get('kenapa', '-')}")
                
                terhalang = k.get("prasyarat_gagal", [])
                if terhalang:
                    st.error(f"Belum bisa dijalankan: {' / '.join(terhalang)}")
                else:
                    st.warning(f"Jika disetujui: {k.get('yang_rusak_kalau_diterapkan', '-')}")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("Setuju, amankan", key=f"setuju_{k['id']}", type="primary"):
                            send_decision(server_name, k['id'], 'setuju')
                    with c2:
                        if st.button("Nanti dulu", key=f"tolak_{k['id']}"):
                            send_decision(server_name, k['id'], 'tolak')


with tab_controls:
    st.header("Semua Aturan Keamanan")
    for k in kontrols:
        status_color = "green" if k['status'] == "LULUS" else "red" if k['status'] == "GAGAL" else "gray"
        st.markdown(f"""
        <div class="control-card">
            <span style="background-color: {status_color}; padding: 3px 8px; border-radius: 5px; font-size: 12px; font-weight: bold;">{k['status']}</span>
            <b>{k['nama']} ({k['id']})</b>
            <br><small style="color: gray;">Target: {k['nilai_target']} | Terbaca: {k['nilai_terbaca']}</small>
        </div>
        """, unsafe_allow_html=True)

with tab_chat:
    st.header("Chat dengan Hermes")
    st.info("Hermes adalah AI assistant yang memonitor server Anda. Tanyakan apa saja tentang keamanan server ini.")
    
    # Simple Mock Chat for Hackathon Demo
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": f"Halo Tuan. Saya Hermes. Server {server_name} saat ini memiliki skor keamanan {score}/100. Ada yang bisa saya bantu?"}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Tanya Hermes tentang K06 atau port 3306..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            if "port" in prompt.lower() or "3306" in prompt.lower() or "k06" in prompt.lower():
                response = "Saya mendeteksi port 3306 (biasanya untuk database MySQL/MariaDB) diubah konfigurasinya dari `127.0.0.1` (lokal) menjadi `0.0.0.0` (publik) oleh user `budi`. Ini sangat berisiko karena siapapun di internet bisa mencoba meretas database Anda. Saya sarankan Anda membuka tab **Action Center** dan menekan tombol 'Kembalikan seperti semula'."
            else:
                response = "Sebagai agen AI DevSecOps, saya terus memantau `auditd` dan `syslog` Anda. Saat ini saya fokus memprioritaskan penyelesaian masalah port yang terbuka. Silakan cek Action Center."
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
