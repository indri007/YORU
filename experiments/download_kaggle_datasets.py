#!/usr/bin/env python3
"""
download_kaggle_datasets.py - Pengunduh Otomatis Dataset Keamanan IoT/IIoT dari Kaggle

Dataset yang diunduh:
1. azalhowaide/iot-dataset-for-intrusion-detection-systems-ids
2. mohamedamineferrag/edgeiiotset-cyber-security-dataset-of-iot-iiot
"""

import subprocess
import sys
from pathlib import Path

DEST_DIR = Path(__file__).resolve().parent / "datasets"
DEST_DIR.mkdir(parents=True, exist_ok=True)

DATASETS = [
    {
        "id": "azalhowaide/iot-dataset-for-intrusion-detection-systems-ids",
        "name": "IoT-Dataset-IDS-Alhowaide"
    },
    {
        "id": "mohamedamineferrag/edgeiiotset-cyber-security-dataset-of-iot-iiot",
        "name": "Edge-IIoTset-Ferrag"
    }
]

def check_kaggle_installed():
    import importlib.util
    if importlib.util.find_spec("kagglehub") is not None:
        return "kagglehub"

    try:
        res = subprocess.run(["kaggle", "--version"], capture_output=True, text=True, check=False)
        if res.returncode == 0:
            return "kaggle_cli"
    except FileNotFoundError:
        pass

    return None

def download_via_kagglehub(ds_id, target_subfolder):
    import shutil

    import kagglehub
    print(f"[*] Mengunduh {ds_id} via kagglehub...")
    download_path = kagglehub.dataset_download(ds_id)
    print(f"[+] Berhasil diunduh ke cache: {download_path}")
    
    target_path = DEST_DIR / target_subfolder
    if not target_path.exists():
        shutil.copytree(download_path, target_path)
        print(f"[+] Tersalin ke: {target_path}")
    else:
        print(f"[i] Folder tujuan sudah ada: {target_path}")

def download_via_cli(ds_id, target_subfolder):
    target_path = DEST_DIR / target_subfolder
    target_path.mkdir(parents=True, exist_ok=True)
    print(f"[*] Mengunduh {ds_id} via Kaggle CLI...")
    cmd = ["kaggle", "datasets", "download", "-d", ds_id, "-p", str(target_path), "--unzip"]
    subprocess.run(cmd, check=True)
    print(f"[+] Selesai diunduh dan diekstrak ke: {target_path}")

def main():
    print("=" * 70)
    print("PENGUNDUH DATASET IDS IoT/IIoT UNTUK EVALUASI YORU HARNESS")
    print("=" * 70)

    tool = check_kaggle_installed()

    if not tool:
        print("\n[!] Library 'kagglehub' atau 'kaggle' CLI belum terpasang.")
        print("    Silakan pasang kagglehub terlebih dahulu:")
        print("        pip install kagglehub")
        print("    Atau pasang Kaggle CLI:")
        print("        pip install kaggle")
        print("\n    Jika menggunakan Kaggle CLI, pastikan API token Anda ada di:")
        print("        ~/.kaggle/kaggle.json")
        sys.exit(1)

    for ds in DATASETS:
        ds_id = ds["id"]
        subfolder = ds["name"]
        print(f"\n--> Memproses: {ds_id}")
        try:
            if tool == "kagglehub":
                download_via_kagglehub(ds_id, subfolder)
            else:
                download_via_cli(ds_id, subfolder)
        except (OSError, RuntimeError) as e:
            print(f"[ERROR] Gagal mengunduh {ds_id}: {e}")
            print("Tip: Pastikan Anda sudah login ke Kaggle atau memiliki token API aktif.")

if __name__ == "__main__":
    main()
