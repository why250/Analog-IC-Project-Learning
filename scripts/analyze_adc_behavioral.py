"""Verify actual PSF ASCII output buses and export small teaching traces.

This parser handles scalar DOUBLE traces from these explicit teaching netlists.
It is not a general PSF parser. Complete PSF data stay on the EDA host.
"""
from pathlib import Path
import argparse
import bisect
import csv
import hashlib
import json
import math
import re


def read_psf(path):
    waves = {}
    active = False
    for line in path.read_text().splitlines():
        if line == "VALUE":
            active = True
            continue
        if not active:
            continue
        match = re.fullmatch(r'"([^"]+)"\s+([\deE.+-]+)', line)
        if match:
            name, value = match.groups()
            waves.setdefault(name, []).append(float(value))
    times = waves.get("time", [])
    if len(times) < 2 or any(b <= a for a, b in zip(times, times[1:])):
        raise ValueError("Missing or nonmonotonic PSF time axis")
    if any(len(v) != len(times) for v in waves.values()):
        raise ValueError("Unsupported nonrectangular PSF trace")
    if not all(math.isfinite(x) for values in waves.values() for x in values):
        raise ValueError("Nonfinite PSF values")
    return waves


def at(waves, name, time):
    times = waves["time"]
    if not times[0] <= time <= times[-1]:
        raise ValueError("Requested time outside waveform")
    i = bisect.bisect_right(times, time) - 1
    if i == len(times) - 1:
        return waves[name][i]
    f = (time - times[i]) / (times[i + 1] - times[i])
    return waves[name][i] + f * (waves[name][i + 1] - waves[name][i])


def edges(waves, name, threshold=0.9, rising=True):
    result = []
    for i in range(1, len(waves["time"])):
        a, b = waves[name][i - 1:i + 1]
        crossed = a < threshold <= b if rising else a > threshold >= b
        if crossed:
            ta, tb = waves["time"][i - 1:i + 1]
            result.append(ta + (threshold - a) * (tb - ta) / (b - a))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    path = args.run / "sar_nominal/psf/tran1.tran.tran"
    w = read_psf(path)
    falling = edges(w, "sample", rising=False)
    complete = edges(w, "eoc")
    compare = edges(w, "eval")
    checks = []
    assert len(complete) == len(falling) == 5
    for start, end in zip(falling, complete):
        observe = end + 100e-12
        code = sum((at(w, f"b{i}", observe) > 0.9) << i for i in range(8))
        x = at(w, "vip", start) - at(w, "vin", start)
        expected = min(255, max(0, math.floor((x + 1.8) / 3.6 * 256)))
        count = sum(start < t < end for t in compare)
        assert code == expected and count == 8, (code, expected, count)
        assert at(w, "overrun", observe) < 0.9
        checks.append({"sample_fall_s": start, "eoc_rise_s": end,
                       "conversion_window_s": end - start,
                       "input_differential_V": x, "decoded_bus_code": code,
                       "expected_floor_code": expected, "evaluate_edges": count})
    report = {"new_waveform_analysis": True, "model_level": "teaching_behavioral_no_PDK",
              "waveform_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
              "bus_sample_after_eoc_s": 100e-12, "logic_threshold_V": 0.9,
              "samples": checks}
    (args.run / "waveform-checks.json").write_text(json.dumps(report, indent=2) + "\n")
    with (args.run / "sar-trace.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time_s", "residue_diff_V", "eval_V", "done_V", "phase", "eoc_V"])
        for k, t in enumerate(w["time"]):
            if 4.5e-9 <= t <= 13e-9:
                writer.writerow([t, w["dp"][k]-w["dn"][k], w["eval"][k],
                                 w["done"][k], w["phase"][k], w["eoc"][k]])
    header = path.read_text().split("TYPE", 1)[0]
    print(header.split('"version"', 1)[1].splitlines()[0].strip())
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    main()
