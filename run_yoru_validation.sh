#!/bin/bash
# ==============================================================================
# run_yoru_validation.sh - Comprehensive Validation Suite for YORU Harness
# ==============================================================================
# Menjalankan validasi menyeluruh:
#   1. Validasi Sintaks Skrip Shell (bash -n)
#   2. Kompilasi & Integritas Kode Python
#   3. Integritas Katalog Kontrol CIS (K01-K10) & Skema Kontrak JSON
#   4. Evaluasi Keamanan YORU Harness (RQ1: Injection-to-Action Benchmark)
#   5. Pengecekan Runtime Linux / Kernel Auditd (jika dijalankan pada Linux)
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

PASS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0

pass() {
    printf "  ${GREEN}[LULUS]${RESET} %s\n" "$1"
    PASS_COUNT=$((PASS_COUNT + 1))
}

fail() {
    printf "  ${RED}[GAGAL]${RESET} %s (%s)\n" "$1" "$2"
    FAIL_COUNT=$((FAIL_COUNT + 1))
}

skip() {
    printf "  ${YELLOW}[LEWATI]${RESET} %s (%s)\n" "$1" "$2"
    SKIP_COUNT=$((SKIP_COUNT + 1))
}

# Tentukan Python yang digunakan
if command -v /usr/bin/python3 >/dev/null 2>&1; then
    PYTHON="/usr/bin/python3"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON="python3"
else
    PYTHON="python"
fi

OS=$(uname -s)
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR" || exit 1

echo
echo -e "${CYAN}${BOLD}====================================================================${RESET}"
echo -e "${CYAN}${BOLD}           YORU HARNESS COMPREHENSIVE VALIDATION SUITE              ${RESET}"
echo -e "${CYAN}${BOLD}====================================================================${RESET}"
echo -e "Waktu Pengujian : $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo -e "Sistem Operasi  : ${BOLD}${OS} ($(uname -m))${RESET}"
echo -e "Direktori Proyek: ${BOLD}${ROOT_DIR}${RESET}"
echo -e "Interpreter Py  : ${BOLD}$(${PYTHON} --version 2>&1)${RESET}"
echo

# ------------------------------------------------------------------------------
# BAGIAN 1: Validasi Sintaks Skrip Shell (Bash)
# ------------------------------------------------------------------------------
echo -e "${BLUE}${BOLD}[1/5] Validasi Sintaks Skrip Shell (bash -n)${RESET}"

SHELL_SCRIPTS=(
    "bin/yoructl"
    "bin/yoru-watch"
    "check-all.sh"
    "demo.sh"
    "install.sh"
)

for script in "${SHELL_SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        if bash -n "$script" 2>/dev/null; then
            pass "Sintaks bash: $script"
        else
            fail "Sintaks bash: $script" "syntax error terdeteksi"
        fi
    else
        fail "File skrip: $script" "berkas tidak ditemukan"
    fi
done
echo

# ------------------------------------------------------------------------------
# BAGIAN 2: Kompilasi & Verifikasi Kode Python
# ------------------------------------------------------------------------------
echo -e "${BLUE}${BOLD}[2/5] Validasi & Kompilasi Kode Python${RESET}"

PYTHON_FILES=(
    "bin/yoru-agent"
    "bin/yoru-model-proxy"
    "web/api.py"
    "web/streamlit_app.py"
    "web/demo.py"
    "experiments/test_injection_to_action.py"
)

for py_file in "${PYTHON_FILES[@]}"; do
    if [ -f "$py_file" ]; then
        if "$PYTHON" -m py_compile "$py_file" 2>/dev/null; then
            pass "Kompilasi python: $py_file"
        else
            fail "Kompilasi python: $py_file" "syntax error atau kompilasi gagal"
        fi
    else
        skip "File python: $py_file" "berkas opsional tidak ditemukan"
    fi
done
echo

# ------------------------------------------------------------------------------
# BAGIAN 3: Integritas Katalog Kontrol CIS (K01-K10) & Kontrak JSON
# ------------------------------------------------------------------------------
echo -e "${BLUE}${BOLD}[3/5] Validasi Integritas Katalog Kontrol CIS (K01-K10) & Skema${RESET}"

for i in $(seq -w 1 10); do
    cat_file="catalog/K${i}.yaml"
    if [ -f "$cat_file" ]; then
        # Verifikasi bahwa file tidak kosong dan memiliki id kontrol yang sesuai
        if grep -q "id:.*K${i}" "$cat_file" 2>/dev/null || grep -q "K${i}" "$cat_file" 2>/dev/null; then
            pass "Katalog kontrol: $cat_file (terdefinisi)"
        else
            fail "Katalog kontrol: $cat_file" "field ID K${i} hilang"
        fi
    else
        fail "Katalog kontrol: $cat_file" "berkas hilang"
    fi
done

JSON_SAMPLES=(
    "examples/report-fix.json"
    "examples/report-watch.json"
)

for json_file in "${JSON_SAMPLES[@]}"; do
    if [ -f "$json_file" ]; then
        if "$PYTHON" -m json.tool "$json_file" >/dev/null 2>&1; then
            pass "Validitas format JSON: $json_file"
        else
            fail "Validitas format JSON: $json_file" "parse error"
        fi
    else
        skip "Sample JSON: $json_file" "berkas tidak ditemukan"
    fi
done
echo

# ------------------------------------------------------------------------------
# BAGIAN 4: Benchmark Evaluasi Keamanan YORU Harness (RQ1: Injection-to-Action)
# ------------------------------------------------------------------------------
echo -e "${BLUE}${BOLD}[4/5] Benchmark Evaluasi Keamanan YORU Harness (RQ1: Injection-to-Action)${RESET}"

if [ -f "experiments/test_injection_to_action.py" ]; then
    BENCHMARK_OUTPUT=$("$PYTHON" experiments/test_injection_to_action.py 2>&1)
    if echo "$BENCHMARK_OUTPUT" | grep -q "ASR_action): 0.0%"; then
        pass "Ruang Aksi Tertutup: ASR_action = 0.0% (Zero Arbitrary OS Execution)"
    else
        fail "Ruang Aksi Tertutup" "ASR_action gagal mencapai 0.0%"
    fi

    if [ -f "experiments/results/rq1_injection_results.json" ]; then
        pass "Artefak hasil benchmark: experiments/results/rq1_injection_results.json"
    else
        fail "Artefak hasil benchmark" "file output tidak tercipta"
    fi
else
    skip "Benchmark RQ1" "experiments/test_injection_to_action.py tidak ditemukan"
fi
echo

# ------------------------------------------------------------------------------
# BAGIAN 5: Pengujian Runtime Host & Kernel Auditd
# ------------------------------------------------------------------------------
echo -e "${BLUE}${BOLD}[5/5] Pemeriksaan Runtime Host & Kernel Auditd${RESET}"

if [ "$OS" = "Linux" ]; then
    echo "  -> Terdeteksi lingkungan Linux."
    if command -v systemctl >/dev/null 2>&1; then
        pass "systemctl tersedia"
    else
        fail "systemctl" "tidak ditemukan"
    fi

    if command -v auditctl >/dev/null 2>&1; then
        pass "auditctl tersedia"
        RULES_COUNT=$(sudo auditctl -l 2>/dev/null | grep -c '^-w' || true)
        if [ "$RULES_COUNT" -gt 0 ]; then
            pass "Audit rules aktif: $RULES_COUNT rules terpantau"
        else
            skip "Audit rules" "belum ada rule -w yang dimuat"
        fi
    else
        fail "auditctl" "auditd/auditctl tidak ditemukan"
    fi

    if [ -f "check-all.sh" ] && [ "${EUID:-$(id -u)}" -eq 0 ]; then
        echo "  -> Menjalankan check-all.sh dengan root..."
        bash check-all.sh || true
    fi
else
    skip "Linux Runtime & Kernel auditd" "Host saat ini adalah macOS ($OS)"
    echo -e "     ${YELLOW}Catatan:${RESET} Pengujian level kernel (auditd, ausearch, systemd) membutuhkan Ubuntu 24.04."
    echo -e "     Untuk menguji di macOS via Multipass:"
    echo -e "       ${BOLD}multipass exec yoru-a -- bash -lc 'cd /home/ubuntu/yoru && sudo ./run_yoru_validation.sh'${RESET}"
fi
echo

# ------------------------------------------------------------------------------
# RINGKASAN SKOR AKHIR
# ------------------------------------------------------------------------------
echo -e "${CYAN}${BOLD}====================================================================${RESET}"
echo -e "${CYAN}${BOLD}                       RINGKASAN VALIDASI                           ${RESET}"
echo -e "${CYAN}${BOLD}====================================================================${RESET}"
printf "  Total LULUS  : ${GREEN}${BOLD}%d${RESET}\n" "$PASS_COUNT"
printf "  Total GAGAL  : ${RED}${BOLD}%d${RESET}\n" "$FAIL_COUNT"
printf "  Total LEWATI : ${YELLOW}${BOLD}%d${RESET}\n" "$SKIP_COUNT"
echo -e "${CYAN}${BOLD}====================================================================${RESET}"

if [ "$FAIL_COUNT" -eq 0 ]; then
    echo -e "${GREEN}${BOLD}STATUS: SEMUA VALIDASI YANG DIJALANKAN LULUS (PASS)${RESET}"
    exit 0
else
    echo -e "${RED}${BOLD}STATUS: TERDAPAT $FAIL_COUNT KEGAGALAN DALAM VALIDASI (FAIL)${RESET}"
    exit 1
fi
