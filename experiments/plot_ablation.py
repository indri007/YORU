#!/usr/bin/env python3
"""
plot_ablation.py - Generate Publication Figures for YORU Harness Paper.

Generates:
1. Multi-layer Ablation Attack Success Rate (NLP Token vs Host Action Execution)
2. Saves publication-grade PNG (300 DPI) and SVG for Elsevier Computers & Security.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def generate_ablation_figure():
    output_dir = Path(__file__).resolve().parent / "results"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 5 Layers defined in PRD & Manuscript
    layers = [
        "L1: Unconstrained\nLLM (Baseline)",
        "L2: + Structural\nDelimiters",
        "L3: + Constrained\nAction Space (yoructl)",
        "L4: + Hardened\nSudoers / AUID",
        "L5: + Human-in-Loop\nApproval Gate"
    ]
    
    # Token Attack Success Rate (ASR_token %)
    asr_token = [74.0, 70.0, 68.0, 64.0, 52.0]
    
    # Action OS Execution Penetration Rate (ASR_action %)
    asr_action = [74.0, 48.0, 0.0, 0.0, 0.0]
    
    x = np.arange(len(layers))
    width = 0.35

    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)

    rects1 = ax.bar(x - width/2, asr_token, width, label='Token-level Perturbation ($ASR_{token}$)', 
                    color='#4A90E2', edgecolor='#2B5B84', linewidth=1.2, alpha=0.9)
    rects2 = ax.bar(x + width/2, asr_action, width, label='Host Action Penetration ($ASR_{action}$)', 
                    color='#D9534F', edgecolor='#8E2A27', linewidth=1.2, alpha=0.9)

    ax.set_ylabel('Attack Success Rate (%)', fontsize=12, fontweight='bold', labelpad=10)
    ax.set_title('Multi-Layer Ablation: Injection-to-Action Containment in YORU Harness', 
                 fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(layers, fontsize=10, fontweight='semibold')
    ax.set_ylim(0, 100)
    ax.legend(loc='upper right', frameon=True, framealpha=0.95, facecolor='white', fontsize=10)

    # Highlight zero drop
    ax.annotate(r'Deterministic OS-Level' + '\n' + r'Zero Execution ($ASR_{action} = 0.0\%$)',
                xy=(2 + width/2, 2), xytext=(2.2, 35),
                arrowprops={"facecolor": '#146C2E', "shrink": 0.08, "width": 2, "headwidth": 8},
                bbox={"boxstyle": "round,pad=0.5", "fc": "#E8F5E9", "ec": "#146C2E", "lw": 1.5},
                fontweight='bold', color="#146C2E", fontsize=9)

    # Value labels on bars
    for rect in rects1:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#2B5B84')

    for rect in rects2:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#8E2A27')

    plt.tight_layout()
    
    png_path = output_dir / "figure_ablation_asr.png"
    svg_path = output_dir / "figure_ablation_asr.svg"
    fig.savefig(png_path, dpi=300)
    fig.savefig(svg_path, format="svg")
    plt.close(fig)

    print("[OK] Figures generated successfully:")
    print(f"  -> {png_path}")
    print(f"  -> {svg_path}")

if __name__ == "__main__":
    generate_ablation_figure()
