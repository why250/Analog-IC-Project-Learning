"""Measure fresh comparator OCEAN exports; keep data on the EDA host.

Usage: python measure_comparator_delay.py RUN_DIRECTORY
RUN_DIRECTORY must contain points.json and point_*/{signal}.txt exports.
This script does not run EDA tools or infer results from old ADE histories.
"""

import argparse
import bisect
import csv
import hashlib
import json
import math
from pathlib import Path
from statistics import mean


def read_wave(path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) != 2:
            continue
        try:
            row = tuple(map(float, parts))
        except ValueError:
            continue
        if not all(math.isfinite(value) for value in row):
            raise ValueError(f"Nonfinite waveform: {path}")
        rows.append(row)
    if len(rows) < 2 or any(b[0] <= a[0] for a, b in zip(rows, rows[1:])):
        raise ValueError(f"Missing or nonmonotonic waveform: {path}")
    return [r[0] for r in rows], [r[1] for r in rows]


def at(wave, time):
    times, values = wave
    if time < times[0] or time > times[-1]:
        raise ValueError("Requested time outside waveform")
    index = bisect.bisect_right(times, time) - 1
    if index == len(times) - 1:
        return values[-1]
    fraction = (time - times[index]) / (times[index + 1] - times[index])
    return values[index] + fraction * (values[index + 1] - values[index])


def difference(first, second):
    times, values = first
    return times, [v - at(second, t) for t, v in zip(times, values)]


def crossings(wave, level, rising=True):
    times, values = wave
    result = []
    for i in range(1, len(times)):
        a, b = values[i - 1], values[i]
        crossed = a < level <= b if rising else a > level >= b
        if crossed:
            result.append(times[i - 1] + (level - a) * (times[i] - times[i - 1]) / (b - a))
    return result


def analyze(root):
    points = json.loads((root / "points.json").read_text(encoding="utf-8"))
    results = []
    plot_rows = []
    for point in points:
        archive = root / point["archive_directory"]
        signals = ("clk", "core_clk", "x", "y", "sb", "rb", "out", "outb", "inp", "inn")
        waves = {name: read_wave(archive / f"{name}.txt") for name in signals}
        raw = difference(waves["sb"], waves["rb"])
        final = difference(waves["out"], waves["outb"])
        input_diff = difference(waves["inp"], waves["inn"])
        # Schematic polarity: externally positive Din+-Din- gives sb>rb
        # in the swapped dynamic core, and final out>outb after the NAND SR latch.
        sign = 1 if at(input_diff, 5e-9) > 0 else -1
        expected_raw = raw[0], [sign * value for value in raw[1]]
        rises = crossings(waves["core_clk"], 0.6)
        top_rises = crossings(waves["clk"], 0.6)
        falls = crossings(waves["core_clk"], 0.6, rising=False)
        decisions = crossings(expected_raw, 1.08)
        cycles = []
        for edge in rises[3:8]:
            fall = next((t for t in falls if t > edge), None)
            if fall is None:
                continue
            decision = next((t for t in decisions if edge < t < fall), None)
            # Check the decision stays beyond the threshold until evaluate ends.
            retained = decision is not None and all(
                v >= 1.08 - 1e-6
                for t, v in zip(*expected_raw) if decision + 2e-12 <= t <= fall - 2e-12
            )
            cycles.append({
                "core_rise_s": edge,
                "top_clock_to_core_clock_ps": (edge - max(t for t in top_rises if t <= edge)) * 1e12,
                "evaluate_width_ps": (fall - edge) * 1e12,
                "decision_delay_ps": None if decision is None else (decision - edge) * 1e12,
                "raw_decision_retained": retained,
                "raw_diff_at_end_V": at(raw, fall - 10e-12),
                "final_diff_at_end_V": at(final, fall - 10e-12),
                "raw_reset_diff_V": at(raw, edge - 20e-12),
                "reset_sb_V": at(waves["sb"], edge - 20e-12),
                "reset_rb_V": at(waves["rb"], edge - 20e-12),
            })
        if len(cycles) != 5:
            raise ValueError("Insufficient steady cycles for the fixed measurement window")
        delays = [item["decision_delay_ps"] for item in cycles if item["decision_delay_ps"] is not None]
        errors = []
        if len(delays) != len(cycles):
            errors.append("one or more evaluate windows did not resolve to the expected threshold")
        if any(not item["raw_decision_retained"] for item in cycles):
            errors.append("one or more raw decisions failed retention")
        if any(sign * item["final_diff_at_end_V"] < 1.08 for item in cycles):
            errors.append("final output failed expected polarity or amplitude")
        if any(abs(item["raw_reset_diff_V"]) > 1e-3 for item in cycles):
            errors.append("reset differential did not return within 1 mV")
        item = dict(point)
        item.update({
            "input_differential_V": at(input_diff, 5e-9),
            "input_common_mode_V": (at(waves["inp"], 5e-9) + at(waves["inn"], 5e-9)) / 2,
            "measurement": "core clock rising 0.6 V to expected signed (sb-rb) reaching 1.08 V; 5 cycles after 3 startup cycles",
            "cycles": cycles,
            "mean_raw_delay_ps": mean(delays) if delays else None,
            "delay_range_ps": [min(delays), max(delays)] if delays else None,
            "measurement_errors": errors,
            "waveform_sha256": {name: hashlib.sha256((archive / f"{name}.txt").read_bytes()).hexdigest() for name in signals},
        })
        results.append(item)
        edge = cycles[0]["core_rise_s"]
        # A small uniformly resampled excerpt is for plotting only; measurements
        # above use original adaptive-step exports and linear crossing interpolation.
        for offset_ps in range(-60, 471, 2):
            time = edge + offset_ps * 1e-12
            plot_rows.append([point["vin_expression"], offset_ps, at(waves["core_clk"], time),
                              at(waves["x"], time), at(waves["y"], time), at(raw, time), at(final, time)])
    summary = {"date": "2026-10-04", "VDD_V": 1.2, "model_section": "tt", "fclk_Hz": 1.2e9,
               "maxstep_s": 2e-12, "stop_s": 10e-9, "random_noise": False,
               "output_load": "unchanged comparator_noise_TB_new; intrinsic buffers/SR latch, no added load",
               "source_files_sha256": json.loads((root / "source-manifest.json").read_text(encoding="utf-8")),
               "source_files_unchanged": json.loads((root / "originals-unchanged.json").read_text(encoding="utf-8")),
               "points": results}
    if not all(summary["source_files_unchanged"].values()):
        raise ValueError("Original source hash verification failed")
    (root / "measurement.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    with (root / "cycle-excerpt.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["input", "offset_ps", "core_clk_V", "x_V", "y_V", "sb_minus_rb_V", "out_minus_outb_V"])
        writer.writerows(plot_rows)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_directory", type=Path)
    args = parser.parse_args()
    try:
        summary = analyze(args.run_directory)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(2, f"Measurement failed: {error}\n")
    for point in summary["points"]:
        print(point["vin_expression"], point["mean_raw_delay_ps"], point["measurement_errors"])
