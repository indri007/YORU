#!/bin/bash
# ==============================================================================
# yoru_all_in_one.sh - Automated All-In-One Runner for YORU Harness
# ==============================================================================
# Opsi Penggunaan:
#   ./yoru_all_in_one.sh --vm        Setup VM Multipass (yoru-a) & uji runtime Linux
#   ./yoru_all_in_one.sh --skip-vm   Jalankan validasi lokal tanpa VM (alias --local)
#   ./yoru_all_in_one.sh --local     Jalankan validasi lokal (statis, skema, benchmark)
#   ./yoru_all_in_one.sh --benchmark Jalankan benchmark evaluasi Injection-to-Action (RQ1)
#   ./yoru_all_in_one.sh --demo      Nyalakan Web Dashboard Demo (FastAPI)
#   ./yoru_all_in_one.sh --clean-vm  Hapus dan bersihkan VM Multipass yoru-a
#   ./yoru_all_in_one.sh --help      Tampilkan panduan ini
# ==============================================================================

set -uo pipefail

# ANSI Colors
GREEN="\033[1;32m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
BLUE="\033[1;34m"
CYAN="\033[1;36m"
BOLD="\033[1m"
RESET="\033[0m"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VM_NAME="yoru-a"

log_info()  { echo -e "  ${BLUE}[INFO]${RESET} $1"; }
log_ok()    { echo -e "  ${GREEN}[OK]${RESET} $1"; }
log_warn()  { echo -e "  ${YELLOW}[PERINGATAN]${RESET} $1"; }
log_err()   { echo -e "  ${RED}[ERROR]${RESET} $1"; }

show_header() {
    echo
    echo -e "${CYAN}${BOLD}====================================================================${RESET}"
    echo -e "${CYAN}${BOLD}                 YORU HARNESS - ALL-IN-ONE RUNNER                   ${RESET}"
    echo -e "${CYAN}${BOLD}====================================================================${RESET}"
    echo -e "Direktori Kerja : ${BOLD}${ROOT_DIR}${RESET}"
    echo -e "Sistem Host     : ${BOLD}$(uname -s) ($(uname -m))${RESET}"
    echo
}

show_help() {
    show_header
    echo -e "Penggunaan: ${BOLD}./yoru_all_in_one.sh [OPSI]${RESET}"
    echo
    echo "Opsi:"
    echo "  --vm          Setup VM Multipass (Ubuntu 24.04), mount direktori,"
    echo "                dan jalankan instalasi serta pengujian runtime auditd Linux."
    echo "  --local       Jalankan validasi lengkap lokal (statis, skema, benchmark)."
    echo "  --benchmark   Jalankan benchmark RQ1: Injection-to-Action (50 vektor)."
    echo "  --demo        Nyalakan web dashboard demo (port 8000)."
    echo "  --clean-vm    Hapus VM 'yoru-a' dari Multipass (reset total)."
    echo "  --help        Tampilkan panduan ini."
    echo
}

run_local_validation() {
    show_header
    echo -e "${BLUE}${BOLD}>>> Menjalankan Validasi Lokal YORU Harness...${RESET}"
    if [ -x "./run_yoru_validation.sh" ]; then
        ./run_yoru_validation.sh
    else
        bash ./run_yoru_validation.sh
    fi
}

run_benchmark_only() {
    show_header
    echo -e "${BLUE}${BOLD}>>> Menjalankan Benchmark RQ1 (Injection-to-Action)...${RESET}"
    if command -v /usr/bin/python3 >/dev/null 2>&1; then
        /usr/bin/python3 experiments/test_injection_to_action.py
    else
        python3 experiments/test_injection_to_action.py
    fi
}

run_demo_dashboard() {
    show_header
    echo -e "${BLUE}${BOLD}>>> Menyalakan Web Dashboard Demo YORU...${RESET}"
    if [ -f "./demo.sh" ]; then
        bash ./demo.sh "$@"
    else
        log_err "demo.sh tidak ditemukan!"
        exit 1
    fi
}

clean_vm() {
    show_header
    echo -e "${YELLOW}${BOLD}>>> Menghapus VM '${VM_NAME}' dari Multipass...${RESET}"
    if ! command -v multipass >/dev/null 2>&1; then
        log_err "Multipass tidak terpasang di sistem ini."
        exit 1
    fi
    multipass stop "$VM_NAME" 2>/dev/null || true
    multipass delete "$VM_NAME" 2>/dev/null || true
    multipass purge 2>/dev/null || true
    log_ok "VM '${VM_NAME}' berhasil dihapus dan dibersihkan."
}

run_vm_pipeline() {
    show_header
    echo -e "${CYAN}${BOLD}>>> Menjalankan Pipeline VM Linux (Ubuntu 24.04 via Multipass)${RESET}"
    echo

    # 1. Cek ketersediaan perintah multipass
    if ! command -v multipass >/dev/null 2>&1; then
        log_err "Perintah 'multipass' tidak ditemukan di host ini."
        echo -e "     Silakan pasang Multipass terlebih dahulu: ${BOLD}brew install --cask multipass${RESET}"
        exit 1
    fi
    log_ok "Multipass terdeteksi di: $(command -v multipass)"

    # 2. Periksa apakah VM yoru-a sudah ada
    log_info "Memeriksa status instance '${VM_NAME}'..."
    VM_STATUS=$(multipass info "$VM_NAME" 2>&1 || true)

    if echo "$VM_STATUS" | grep -q "does not exist"; then
        log_warn "Instance '${VM_NAME}' belum ada. Memulai pembuatan VM baru..."
        echo -e "     Spesifikasi: Ubuntu 24.04 LTS (2 vCPU, 4GB RAM)"
        echo -e "     Proses ini mungkin memakan waktu beberapa menit saat pertama kali mengunduh image..."
        if multipass launch 24.04 --name "$VM_NAME" --cpus 2 --memory 4G; then
            log_ok "VM '${VM_NAME}' berhasil diluncurkan!"
        else
            log_err "Gagal meluncurkan VM '${VM_NAME}' via Multipass."
            echo -e "     Tip: Pastikan daemon Multipass sudah aktif di macOS."
            echo -e "     Jalankan manual: ${BOLD}multipass launch 24.04 --name yoru-a --cpus 2 --memory 4G${RESET}"
            exit 1
        fi
    elif echo "$VM_STATUS" | grep -qi "Stopped"; then
        log_info "Menyalakan kembali VM '${VM_NAME}' yang sedang berhenti..."
        multipass start "$VM_NAME"
        log_ok "VM '${VM_NAME}' aktif."
    else
        log_ok "Instance '${VM_NAME}' sudah aktif."
    fi

    # Verifikasi kembali keberadaan VM sebelum mount dan exec
    if ! multipass info "$VM_NAME" >/dev/null 2>&1; then
        log_err "Instance '${VM_NAME}' tidak dapat diakses. Batalkan pipeline."
        exit 1
    fi

    # 3. Mount direktori repo ke VM
    log_info "Melakukan sinkronisasi / mounting direktori kerja ke VM..."
    multipass mount "$ROOT_DIR" "${VM_NAME}:/home/ubuntu/yoru" 2>/dev/null || {
        log_info "Mount sudah terpasang atau diperbarui."
    }

    # 4. Instalasi & Setup YORU jika belum terpasang
    log_info "Memeriksa instalasi YORU di dalam VM..."
    multipass exec "$VM_NAME" -- bash -lc '
        if [ ! -f /opt/yoru/bin/yoructl ]; then
            echo "--> Memasang komponen YORU di VM..."
            cd /home/ubuntu/yoru && sudo ./install.sh
        else
            echo "--> Komponen /opt/yoru/bin/yoructl sudah terpasang di VM."
        fi
    '

    # 5. Jalankan validasi runtime kernel lengkap di dalam VM
    echo
    echo -e "${CYAN}${BOLD}====================================================================${RESET}"
    echo -e "${CYAN}${BOLD}     MENJALANKAN VALIDASI RUNNEL KERNEL DI DALAM VM UBUNTU 24.04    ${RESET}"
    echo -e "${CYAN}${BOLD}====================================================================${RESET}"
    multipass exec "$VM_NAME" -- bash -lc 'cd /home/ubuntu/yoru && sudo ./run_yoru_validation.sh'

    echo
    echo -e "${GREEN}${BOLD}Pipeline VM Selesai.${RESET}"
    echo -e "Akses shell interaktif VM sewaktu-waktu:"
    echo -e "  ${BOLD}multipass shell ${VM_NAME}${RESET}"
}

# ------------------------------------------------------------------------------
# Dispatcher Argumen CLI
# ------------------------------------------------------------------------------
CMD="${1:---interactive}"

case "$CMD" in
    --vm)
        run_vm_pipeline
        ;;
    --skip-vm|--no-vm|--local)
        run_local_validation
        ;;
    --benchmark)
        run_benchmark_only
        ;;
    --demo)
        shift
        run_demo_dashboard "$@"
        ;;
    --clean-vm)
        clean_vm
        ;;
    --help|-h)
        show_help
        ;;
    *)
        # Default: Jika dijalankan tanpa opsi atau interaktif
        show_header
        echo -e "${BOLD}Pilih mode eksekusi YORU Harness:${RESET}"
        echo -e "  ${CYAN}[1]${RESET} Setup & Validasi Lengkap di VM Linux Ubuntu 24.04 (Multipass) [${BOLD}--vm${RESET}]"
        echo -e "  ${CYAN}[2]${RESET} Jalankan Validasi Lokal Statis & Keamanan [${BOLD}--local${RESET}]"
        echo -e "  ${CYAN}[3]${RESET} Jalankan Benchmark Evaluasi Injeksi RQ1 [${BOLD}--benchmark${RESET}]"
        echo -e "  ${CYAN}[4]${RESET} Jalankan Dashboard Web Demo [${BOLD}--demo${RESET}]"
        echo -e "  ${CYAN}[5]${RESET} Keluar"
        echo
        read -r -p "Masukkan pilihan [1-5]: " PILIHAN </dev/tty 2>/dev/null || PILIHAN="2"
        case "$PILIHAN" in
            1) run_vm_pipeline ;;
            2) run_local_validation ;;
            3) run_benchmark_only ;;
            4) run_demo_dashboard ;;
            *) echo "Keluar." ;;
        esac
        ;;
esac
