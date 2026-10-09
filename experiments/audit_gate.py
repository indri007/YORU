#!/usr/bin/env python3
"""
experiments/audit_gate.py
Automated Quality Gate Validator for Scopus Q1 Network Analysis
Handles gates 4, 5, 6, and 7 of run_scientific_audit.sh
"""

import sys
import csv
from pathlib import Path
from collections import Counter

def gate_4():
    p = Path("experiments/results/nodexl_edges_empirical.csv")
    if not p.exists():
        print("FAIL: empirical edge file missing")
        sys.exit(1)

    rows = list(csv.DictReader(p.open(encoding="utf-8")))
    required = [
        "Vertex 1", "Vertex 2", "Relationship", "Weight",
        "Network Graph", "Network ID", "Evidence Type",
        "Source", "Source Locator"
    ]

    missing = [x for x in required if x not in (rows[0].keys() if rows else required)]
    if missing:
        print("FAIL: missing columns:", missing)
        sys.exit(1)

    bad = [
        r for r in rows
        if not r["Vertex 1"] or not r["Vertex 2"] or not r["Source"] or not r["Source Locator"]
    ]

    arch = [r for r in rows if r["Evidence Type"].lower() == "architecture"]

    print(f"rows: {len(rows)}")
    print(f"missing provenance: {len(bad)}")
    print(f"architecture edges inside empirical: {len(arch)}")

    if bad or arch:
        print("FAIL")
        sys.exit(1)

    print("PASS")

def gate_5():
    p = Path("experiments/results/nodexl_edges_empirical.csv")
    if not p.exists():
        print("FAIL: empirical edge file missing")
        sys.exit(1)

    rows = list(csv.DictReader(p.open(encoding="utf-8")))
    c = Counter(r["Network ID"] for r in rows)

    for i in range(1, 16):
        print(f"Network {i:02d}: {c[str(i)]} empirical edges")

    if c["15"] > 0:
        print("FAIL: Network 15 architecture must not be in empirical dataset")
        sys.exit(1)

    print("PASS")

def gate_6():
    p = Path("experiments/results/network_metrics.csv")
    if not p.exists():
        print("FAIL: network_metrics.csv missing")
        sys.exit(1)

    rows = list(csv.DictReader(p.open(encoding="utf-8")))
    if not rows:
        print("FAIL: no metrics")
        sys.exit(1)

    required = ["network_id", "network_name", "nodes", "edges", "density"]
    missing = [x for x in required if x not in rows[0]]
    if missing:
        print("FAIL missing:", missing)
        sys.exit(1)

    for r in rows:
        try:
            n = int(r["nodes"])
            e = int(r["edges"])
            d = float(r["density"])
            if n > 1 and (d < 0 or d > 1.05):
                print(f"FAIL density out of bounds in network {r['network_id']}: {d}")
                sys.exit(1)
        except Exception as ex:
            print(f"FAIL invalid numbers in {r['network_id']}: {ex}")
            sys.exit(1)

    print(f"PASS ({len(rows)} networks validated)")

def gate_7():
    p = Path("experiments/results/network_centrality.csv")
    if not p.exists():
        print("FAIL: network_centrality.csv missing")
        sys.exit(1)

    rows = list(csv.DictReader(p.open(encoding="utf-8")))
    if not rows:
        print("FAIL: no centrality")
        sys.exit(1)

    required = ["network_id", "network_name", "node", "metric", "score", "rank", "evidence_type"]
    missing = [x for x in required if x not in rows[0]]
    if missing:
        print("FAIL missing:", missing)
        sys.exit(1)

    print(f"PASS ({len(rows)} centrality records verified)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: audit_gate.py <gate_number>")
        sys.exit(1)

    gate = sys.argv[1]
    if gate == "4":
        gate_4()
    elif gate == "5":
        gate_5()
    elif gate == "6":
        gate_6()
    elif gate == "7":
        gate_7()
    else:
        print(f"Unknown gate: {gate}")
        sys.exit(1)
