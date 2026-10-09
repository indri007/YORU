#!/usr/bin/env bash
# ==============================================================================
# YORU FINAL SCIENTIFIC + SECURITY AUDIT SCRIPT
# Automated 12-Step Quality Gate for Scopus Q1 Network Analysis
# ==============================================================================

set -o pipefail
FAIL=0

echo "============================================================"
echo "        YORU FINAL SCIENTIFIC + SECURITY AUDIT"
echo "============================================================"

echo ""
echo "[1/12] Repository status"
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
git status --short

echo ""
echo "[2/12] Credential leak scan"
# Scan all tracked project files, excluding .git and images
LEAK_COUNT=$(grep -RInE --exclude-dir=.git --exclude-dir=node_modules --exclude='*.png' --exclude='*.svg' \
'(ghp_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|Authorization:[[:space:]]*Bearer|api[_-]?key[[:space:]]*=[[:space:]]*["'"'"'][^"'"'"']+|password[[:space:]]*=[[:space:]]*["'"'"'][^"'"'"']+)' . 2>/dev/null | wc -l || true)

if [ "$LEAK_COUNT" -gt 0 ]; then
  echo "FAIL: possible credential/secret found ($LEAK_COUNT instances)"
  FAIL=1
else
  echo "PASS: no obvious credential pattern"
fi

echo ""
echo "[3/12] Required empirical NodeXL artifacts"
for f in \
experiments/results/nodexl_edges_empirical.csv \
experiments/results/nodexl_vertices_empirical.csv \
experiments/results/nodexl_provenance.csv \
experiments/results/nodexl_manifest.json \
experiments/results/nodexl_gap_report.md \
experiments/results/network_metrics.csv \
experiments/results/network_centrality.csv \
experiments/results/figure_selection.md \
experiments/results/Q1_NETWORK_ANALYSIS_AUDIT.md; do
  if [ -f "$f" ]; then
    echo "PASS $f"
  else
    echo "FAIL $f"
    FAIL=1
  fi
done

echo ""
echo "[4/12] Empirical edge integrity"
if /usr/bin/python3 experiments/audit_gate.py 4; then
  :
else
  FAIL=1
fi

echo ""
echo "[5/12] Network coverage"
if /usr/bin/python3 experiments/audit_gate.py 5; then
  :
else
  FAIL=1
fi

echo ""
echo "[6/12] Metrics sanity"
if /usr/bin/python3 experiments/audit_gate.py 6; then
  :
else
  FAIL=1
fi

echo ""
echo "[7/12] Centrality sanity"
if /usr/bin/python3 experiments/audit_gate.py 7; then
  :
else
  FAIL=1
fi

echo ""
echo "[8/12] Statistical claim scan"
LEGACY_COUNT=$(grep -RInE \
'ASR_action[[:space:]]*=[[:space:]]*0\.0%|100% (accuracy|rollback|reversibility)|86% (loss|masked)' \
experiments/results docs README.md 2>/dev/null | wc -l || true)

if [ "$LEGACY_COUNT" -gt 0 ]; then
  echo "WARNING: inspect hard-coded percentage claims ($LEGACY_COUNT instances)"
else
  echo "PASS: no obvious hard-coded legacy claims"
fi

echo ""
echo "[9/12] Architecture/empirical separation"
ARCH_MIX_COUNT=$(grep -RInE \
'Network 15.*empirical|Closed-Loop.*empirical|architecture.*empirical' \
experiments/results 2>/dev/null | wc -l || true)

if [ "$ARCH_MIX_COUNT" -gt 0 ]; then
  echo "FAIL: possible architecture/empirical mixing ($ARCH_MIX_COUNT instances)"
  FAIL=1
else
  echo "PASS"
fi

echo ""
echo "[10/12] Figure provenance"
if [ -d assets/network_figures ]; then
  find assets/network_figures -type f | sort
else
  echo "WARNING: no network figure directory"
fi

echo ""
echo "[11/12] Git diff safety"
git diff --check
git diff --stat

echo ""
echo "[12/12] FINAL SCIENTIFIC GATE"
if [ "$FAIL" -eq 0 ]; then
  echo "============================================================"
  echo "PASS — YORU NODEXL AUDIT GATE"
  echo "============================================================"
  echo "No blocking structural/security issue detected."
  echo "Review scientific claims manually before commit."
else
  echo "============================================================"
  echo "FAIL — DO NOT COMMIT/PUSH"
  echo "============================================================"
  echo "Fix every FAIL above, rerun this audit, then review manually."
fi

exit "$FAIL"
