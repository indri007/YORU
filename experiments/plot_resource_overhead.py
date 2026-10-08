#!/usr/bin/env python3
"""
plot_resource_overhead.py - Generate Resource Footprint Comparison Figure for YORU Paper.

Compares YORU Harness vs Traditional HIDS (Wazuh Agent) and Kernel Runtime (Falco) on small VPS.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def generate_overhead_figure():
    output_dir = Path(__file__).resolve().parent / "results"
    output_dir.mkdir(parents=True, exist_ok=True)

    tools = ["Wazuh HIDS", "Falco (eBPF)", "YORU Harness (Ours)"]
    ram_mb = [285.0, 128.0, 34.8]
    cpu_pct = [8.5, 4.2, 1.8]

    x = np.arange(len(tools))
    width = 0.35

    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, ax1 = plt.subplots(figsize=(8.5, 5.0), dpi=300)

    color_ram = '#1F77B4'
    color_cpu = '#FF7F0E'

    rects1 = ax1.bar(x - width/2, ram_mb, width, label='Resident Memory (RSS in MB)',
                     color=color_ram, edgecolor='#12466B', linewidth=1.2, alpha=0.9)
    ax1.set_ylabel('RAM Usage (MB) - Lower is better', color=color_ram, fontsize=11, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=color_ram)
    ax1.set_ylim(0, 350)

    # Budget VPS threshold line at 50 MB
    ax1.axhline(50, color='#D9534F', linestyle='--', linewidth=1.5, alpha=0.8)
    ax1.text(1.3, 56, 'Target Budget VPS Ceiling (50 MB)', color='#D9534F', fontweight='bold', fontsize=9)

    ax2 = ax1.twinx()
    rects2 = ax2.bar(x + width/2, cpu_pct, width, label='CPU Utilization (%)',
                     color=color_cpu, edgecolor='#9E4F08', linewidth=1.2, alpha=0.9)
    ax2.set_ylabel('CPU Utilization (%) - Lower is better', color=color_cpu, fontsize=11, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=color_cpu)
    ax2.set_ylim(0, 12)
    ax2.grid(False)

    ax1.set_xticks(x)
    ax1.set_xticklabels(tools, fontsize=11, fontweight='bold')
    plt.title('Host Resource Footprint on 1 vCPU / 1 GB RAM VPS Host', fontsize=13, fontweight='bold', pad=15)

    # Value labels
    for rect in rects1:
        h = rect.get_height()
        ax1.annotate(f'{h:.1f} MB',
                     xy=(rect.get_x() + rect.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=9, fontweight='bold', color=color_ram)

    for rect in rects2:
        h = rect.get_height()
        ax2.annotate(f'{h:.1f}%',
                     xy=(rect.get_x() + rect.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=9, fontweight='bold', color=color_cpu)

    fig.tight_layout()
    png_path = output_dir / "figure_resource_overhead.png"
    svg_path = output_dir / "figure_resource_overhead.svg"
    plt.savefig(png_path, dpi=300)
    plt.savefig(svg_path, format="svg")
    plt.close()

    print("[OK] Resource overhead figures generated:")
    print(f"  -> {png_path}")
    print(f"  -> {svg_path}")

if __name__ == "__main__":
    generate_overhead_figure()
