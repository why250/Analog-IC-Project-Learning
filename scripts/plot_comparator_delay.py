"""Plot the small archived comparator excerpt using matplotlib.

Usage: python plot_comparator_delay.py METRICS_JSON EXCERPT_CSV OUTPUT_PNG
"""

import argparse
import csv
import json
from pathlib import Path


def plot(metrics_path, excerpt_path, output_path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    summary = json.loads(metrics_path.read_text(encoding="utf-8"))
    with excerpt_path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    groups = {point["vin_expression"]: [row for row in rows if row["input"] == point["vin_expression"]]
              for point in summary["points"]}
    if any(not group for group in groups.values()):
        raise ValueError("Excerpt does not cover every measured point")
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False,
                         "axes.spines.right": False})
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True, constrained_layout=True)
    first = groups["1m"]
    time = [float(row["offset_ps"]) for row in first]
    axes[0].plot(time, [float(row["core_clk_V"]) for row in first], color="#7b8492", label="Core clock")
    for key, linestyle in (("1m", "-"), ("100u", "--")):
        group = groups[key]
        t = [float(row["offset_ps"]) for row in group]
        for node, color in (("x", "#2166ac"), ("y", "#d95f02")):
            axes[0].plot(t, [float(row[f"{node}_V"]) for row in group], linestyle=linestyle,
                         color=color, label=f"{node}: +{key}")
    axes[0].set_ylabel("Clock / internal nodes (V)")
    axes[0].legend(ncol=3, fontsize=9, loc="lower left")
    for point, color in zip(summary["points"], ("#2166ac", "#67a9cf", "#d95f02", "#fdb863")):
        key = point["vin_expression"]
        group = groups[key]
        t = [float(row["offset_ps"]) for row in group]
        delay = point["mean_raw_delay_ps"]
        axes[1].plot(t, [float(row["sb_minus_rb_V"]) for row in group], color=color,
                     label=f"{key}: {delay:.1f} ps")
        axes[2].plot(t, [float(row["out_minus_outb_V"]) for row in group], color=color,
                     linestyle="--" if "100u" in key else "-", label=key)
    for threshold in (-1.08, 1.08):
        axes[1].axhline(threshold, color="#737373", linestyle=":", linewidth=1)
    axes[1].set_ylabel("Raw sb - rb (V)")
    axes[1].legend(ncol=2, loc="center left")
    axes[2].set_ylabel("Final out - outb (V)")
    axes[2].legend(ncol=4, loc="center left")
    axes[2].set_xlabel("Time from dynamic core clock 0.6 V rising crossing (ps)")
    for axis in axes:
        axis.axvline(0, color="#737373", linestyle=":", linewidth=1)
        axis.grid(alpha=0.18)
        axis.set_ylim(-1.35, 1.45)
    axes[2].set_xlim(-60, 470)
    fig.suptitle("Fresh nominal comparator transient: reset, evaluate, retained output\n"
                 "tt | VDD 1.2 V | VCM 0.6 V | clock 1.2 GHz | maxstep 2 ps | no added output load",
                 fontsize=12)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("metrics_json", type=Path)
    parser.add_argument("excerpt_csv", type=Path)
    parser.add_argument("output_png", type=Path)
    args = parser.parse_args()
    try:
        plot(args.metrics_json, args.excerpt_csv, args.output_png)
    except (OSError, ValueError, KeyError, ImportError) as error:
        parser.exit(2, f"Plot failed: {error}\n")
