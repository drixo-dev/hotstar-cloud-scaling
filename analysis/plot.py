#!/usr/bin/env python3
"""
Results Plotting and Evidence Generator for IT457 Hotstar PoC.
Merges Locust load test history and ASG instance history to produce the required plots.

Required Output Deliverable:
- Response Time vs. Instance Count (F2)
- Latency and Instance Count over Time (F1)

Usage:
    python analysis/plot.py [--locust results/raw/locust_stats_history.csv] [--instances results/raw/instances.csv] [--out results/figures]
"""

import argparse
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Generate IT457 Cloud Scaling plots.")
    parser.add_argument("--locust", default="results/raw/locust_stats_history.csv", help="Path to Locust stats history CSV")
    parser.add_argument("--instances", default="results/raw/instances.csv", help="Path to ASG instances CSV")
    parser.add_argument("--out", default="results/figures", help="Directory to save figures")
    args = parser.parse_args()

    locust_path = Path(args.locust)
    instances_path = Path(args.instances)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not locust_path.exists():
        print(f"[!] Error: Locust history file '{locust_path}' not found.")
        print("    Run your Locust load test first with: locust -f loadtest/locustfile.py --csv results/raw/locust ...")
        sys.exit(1)

    if not instances_path.exists():
        print(f"[!] Error: Instances file '{instances_path}' not found.")
        print("    Run the ASG poller during the test with: python loadtest/poller.py")
        sys.exit(1)

    print(f"[*] Reading Locust stats from: {locust_path}")
    df_locust = pd.read_csv(locust_path)

    # Filter for aggregated stats
    if "Name" in df_locust.columns:
        df_locust = df_locust[df_locust["Name"] == "Aggregated"].copy()

    if df_locust.empty:
        print("[!] Error: No 'Aggregated' rows found in Locust history CSV.")
        sys.exit(1)

    # Check timestamp and percentile columns
    # Locust headers typically contain 'Timestamp' and '95%' (or '95% ms')
    ts_col = "Timestamp" if "Timestamp" in df_locust.columns else "timestamp"
    p95_candidates = [c for c in df_locust.columns if "95" in c]
    p50_candidates = [c for c in df_locust.columns if "50" in c]

    if not p95_candidates:
        print(f"[!] Error: Could not locate 95th percentile column in {df_locust.columns.tolist()}")
        sys.exit(1)

    p95_col = p95_candidates[0]
    p50_col = p50_candidates[0] if p50_candidates else p95_col

    df_locust["t"] = df_locust[ts_col].astype(int)
    # If timestamps are in milliseconds, convert to seconds
    if df_locust["t"].iloc[0] > 10_000_000_000:
        df_locust["t"] = (df_locust["t"] / 1000).astype(int)

    df_locust["p95"] = pd.to_numeric(df_locust[p95_col], errors="coerce")
    df_locust["p50"] = pd.to_numeric(df_locust[p50_col], errors="coerce")
    df_locust = df_locust.dropna(subset=["p95"]).sort_values("t")

    print(f"[*] Reading instance history from: {instances_path}")
    df_inst = pd.read_csv(instances_path)
    inst_ts_col = "timestamp" if "timestamp" in df_inst.columns else df_inst.columns[0]
    df_inst["t_inst"] = df_inst[inst_ts_col].astype(int)
    if df_inst["t_inst"].iloc[0] > 10_000_000_000:
        df_inst["t_inst"] = (df_inst["t_inst"] / 1000).astype(int)
    df_inst = df_inst.sort_values("t_inst")

    # Merge as-of backwards
    merged = pd.merge_asof(
        df_locust,
        df_inst,
        left_on="t",
        right_on="t_inst",
        direction="backward"
    )

    if "in_service" not in merged.columns and "in_service_instances" in merged.columns:
        merged["in_service"] = merged["in_service_instances"]
    elif "in_service" not in merged.columns:
        # Fallback to 1 if no instances column
        merged["in_service"] = 1

    merged["in_service"] = merged["in_service"].fillna(1).astype(int)
    merged["elapsed_seconds"] = merged["t"] - merged["t"].min()

    # -------------------------------------------------------------
    # Plot 1: Combined 2-Panel Figure (Lab Manual Part 9)
    # -------------------------------------------------------------
    fig, axes = plt.subplots(2, 1, figsize=(10, 9))
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    # Panel 1: Response time and Instance Count over time
    ax1 = axes[0]
    color_p95 = "tab:blue"
    ax1.set_xlabel("Elapsed Time (seconds)", fontsize=11, fontweight="bold")
    ax1.set_ylabel("p95 Response Time (ms)", color=color_p95, fontsize=11, fontweight="bold")
    line1 = ax1.plot(merged["elapsed_seconds"], merged["p95"], color=color_p95, linewidth=2, label="p95 Latency (ms)")
    ax1.tick_params(axis="y", labelcolor=color_p95)
    ax1.set_title("Hotstar Cloud Scaling: Response Time & Instance Count Over Time", fontsize=13, fontweight="bold")

    ax1_twin = ax1.twinx()
    color_inst = "tab:red"
    ax1_twin.set_ylabel("In-Service Instances", color=color_inst, fontsize=11, fontweight="bold")
    line2 = ax1_twin.step(merged["elapsed_seconds"], merged["in_service"], where="post", color=color_inst, linewidth=2.5, linestyle="--", label="In-Service Instances")
    ax1_twin.tick_params(axis="y", labelcolor=color_inst)
    ax1_twin.set_ylim(0, max(4, merged["in_service"].max() + 1))

    # Add unified legend
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="upper right", frameon=True)

    # Panel 2: Response time against Instance Count (Course Core Deliverable)
    ax2 = axes[1]
    grouped = merged.groupby("in_service")["p95"].agg(["median", "mean", "count"]).reset_index()

    ax2.plot(grouped["in_service"], grouped["median"], marker="o", markersize=8, linewidth=2.5, color="#107C41", label="Median p95 Latency")
    ax2.set_xlabel("In-Service Instance Count", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Median p95 Response Time (ms)", fontsize=11, fontweight="bold")
    ax2.set_title("Course Mandatory Deliverable: Response Time vs. Instance Count", fontsize=13, fontweight="bold")
    ax2.set_xticks(grouped["in_service"].tolist())
    ax2.grid(True, linestyle="--", alpha=0.7)
    for _, row in grouped.iterrows():
        ax2.annotate(
            f"{row['median']:.1f} ms\n(n={int(row['count'])})",
            (row["in_service"], row["median"]),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            fontsize=10,
            fontweight="bold"
        )
    ax2.legend(loc="upper right", frameon=True)

    plt.tight_layout()
    combined_fig_path = out_dir / "response_vs_instances.png"
    plt.savefig(combined_fig_path, dpi=200)
    plt.close()
    print(f"[+] Saved Combined Deliverable Plot to: {combined_fig_path}")

    # -------------------------------------------------------------
    # Plot 2: Dedicated Mandatory Deliverable Chart (F2)
    # -------------------------------------------------------------
    plt.figure(figsize=(8, 5.5))
    plt.plot(grouped["in_service"], grouped["median"], marker="s", markersize=10, linewidth=2.5, color="#00798C", label="Median p95 Response Time")
    plt.title("IT457 Proof of Concept: Response Time vs. In-Service Instances", fontsize=12, fontweight="bold")
    plt.xlabel("In-Service EC2 Instances (ASG Capacity)", fontsize=11, fontweight="bold")
    plt.ylabel("Median p95 Response Time (ms)", fontsize=11, fontweight="bold")
    plt.xticks(grouped["in_service"].tolist())
    plt.grid(True, linestyle="--", alpha=0.6)
    for _, row in grouped.iterrows():
        plt.annotate(
            f"{row['median']:.1f} ms",
            (row["in_service"], row["median"]),
            textcoords="offset points",
            xytext=(0, 12),
            ha="center",
            fontsize=10,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.3)
        )
    plt.tight_layout()
    f2_path = out_dir / "F2_response_time_vs_instance_count.png"
    plt.savefig(f2_path, dpi=200)
    plt.close()
    print(f"[+] Saved F2 Rubric Plot to: {f2_path}")

    # Print summary metrics for submission report
    print("\n" + "=" * 60)
    print("           IT457 POc EXPERIMENT SUMMARY TABLE")
    print("=" * 60)
    print(f"Total Test Duration      : {merged['elapsed_seconds'].max()} seconds")
    print(f"Max In-Service Instances : {merged['in_service'].max()}")
    print(f"Initial p95 Latency (1x) : {grouped[grouped['in_service'] == 1]['median'].values[0] if (grouped['in_service'] == 1).any() else 'N/A'} ms")
    if (grouped["in_service"] > 1).any():
        scaled_p95 = grouped[grouped["in_service"] > 1]["median"].values[0]
        print(f"Scaled p95 Latency (>1x) : {scaled_p95} ms")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
