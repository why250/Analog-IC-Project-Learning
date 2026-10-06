"""Plot a small exported trace from the new teaching SAR simulation."""
from pathlib import Path
import argparse
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    with args.csv.open() as f:
        rows = [{k: float(v) for k, v in row.items()} for row in csv.DictReader(f)]
    if not rows:
        raise ValueError("Empty exported trace")
    t = [r["time_s"] * 1e9 for r in rows]
    fig, axes = plt.subplots(3, 1, figsize=(10, 7), sharex=True, layout="constrained")
    axes[0].plot(t, [r["residue_diff_V"] for r in rows], color="#2463a5")
    axes[0].axhline(0, lw=0.7, color="gray")
    axes[0].set_ylabel("Residual (V)")
    axes[0].set_title("Teaching SAR8: 8 decisions, 7 CDAC updates; input = +0.3 V")
    for name, label, color in [("eval_V", "evaluate", "#2463a5"),
                               ("done_V", "done", "#e07828")]:
        axes[1].plot(t, [r[name] for r in rows], label=label, color=color)
    axes[1].set_ylabel("Logic (V)")
    axes[1].legend(loc="upper right", ncols=2)
    axes[2].plot(t, [r["phase"] for r in rows], label="decision count", color="#2463a5")
    axes[2].plot(t, [r["eoc_V"] for r in rows], label="EOC (V)", color="#e07828")
    axes[2].set_ylabel("Count / EOC")
    axes[2].set_xlabel("Time (ns)")
    axes[2].legend(loc="upper left", ncols=2)
    for ax in axes:
        ax.grid(alpha=0.2)
    fig.text(0.99, 0.005, "Fresh Spectre behavioral run; no PDK or transistor validation",
             ha="right", fontsize=9, color="#555555")
    fig.savefig(args.output, dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()
