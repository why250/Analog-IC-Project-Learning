"""Run small teaching Verilog-A baselines with Spectre, without modifying OA.

Run on the EDA host, using its configured runtime and an explicit output path.
No PDK required. Logs, netlists, models and results remain in that output path.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sar_netlist(tdec):
    prefix = " ".join(f"p{i}" for i in range(7, -1, -1))
    bits = " ".join(f"b{i}" for i in range(7, -1, -1))
    return f'''simulator lang=spectre
ahdl_include "async_sar8.va"
sample_src (sample 0) vsource type=pulse val0=0 val1=1.8 delay=1n rise=10p fall=10p width=4n period=25n
inp (vip 0) vsource type=pwl wave=[0 1.05 24n 1.05 25n 0.75 49n 0.75 50n 1.45 74n 1.45 75n 0.35 99n 0.35 100n 1.05]
inn (vin 0) vsource type=pwl wave=[0 0.75 24n 0.75 25n 1.05 49n 1.05 50n 0.35 74n 0.35 75n 1.45 99n 1.45 100n 0.75]
sh (vip vin sample hp hn 0) learn_sh
cdac (hp hn {prefix} phase dp dn 0) learn_cdac8
cmp (dp dn eval outp outn 0) learn_compare tdec={tdec}
det (outp outn done 0) learn_done
ctrl (sample done outp eval {prefix} phase {bits} eoc overrun 0) learn_ctrl8
simopts options reltol=1e-5 vabstol=1u iabstol=1p
tran1 tran stop=120n maxstep=25p
save vip vin sample hp hn dp dn eval outp outn done phase eoc overrun {bits}
'''


RESIDUE_MONITOR = '''`include "disciplines.vams"
module learn_residue_probe(p,n);
 input p,n; electrical p,n;
 analog begin
   @(timer(9n,20n)) $strobe("RESIDUE time=%g diff=%g",$abstime,V(p,n));
 end
endmodule
'''


def residue_netlist(gain_error):
    return f'''simulator lang=spectre
ahdl_include "residue_amp.va"
ahdl_include "residue_probe.va"
inp (ip 0) vsource type=pwl wave=[0 0.605 19n 0.605 20n 0.625 39n 0.625 40n 0.675 59n 0.675]
inn (im 0) vsource type=pwl wave=[0 0.595 19n 0.595 20n 0.575 39n 0.575 40n 0.525 59n 0.525]
amp (ip im op om 0) learn_residue_amp gain_error={gain_error}
probe (op om) learn_residue_probe
simopts options reltol=1e-5 vabstol=1u iabstol=1p
tran1 tran stop=60n maxstep=50p
save ip im op om
'''


def inspect_sar(log, expect_overrun=False):
    results = [(int(s), int(c), float(t)) for s, c, t in re.findall(
        r"SAR_RESULT sample=\s*(\d+) code=\s*(\d+) time=\s*([\deE.+-]+)", log)]
    steps = [(int(s), int(b), int(d), float(t)) for s, b, d, t in re.findall(
        r"SAR_BIT sample=\s*(\d+) bit=\s*(\d+) decision=\s*(\d+) time=\s*([\deE.+-]+)", log)]
    overruns = re.findall(r"SAR_OVERRUN time=([\deE.+-]+)", log)
    if expect_overrun:
        assert overruns, "Deliberately slow comparator did not trigger overrun"
    else:
        expected = [149, 106, 206, 49, 149]
        assert [c for _, c, _ in results] == expected, results
        assert not overruns, overruns
    for sid, code, time in results:
        events = [v for v in steps if v[0] == sid]
        assert [v[1] for v in events] == list(range(7, -1, -1)), events
        assert sum(v[2] << v[1] for v in events) == code
    return {"completed_samples": [{"id": s, "code": c, "time_s": t}
                                  for s, c, t in results],
            "decision_events": len(steps), "overrun_times_s": list(map(float, overruns))}


def inspect_residue(log, gain_error):
    points = [(float(t), float(v)) for t, v in re.findall(
        r"RESIDUE time=([\deE.+-]+) diff=([\deE.+-]+)", log)]
    expected = [0.08 * (1 + gain_error), 0.4 * (1 + gain_error), 0.8]
    assert len(points) == 3, points
    for (_, measured), target in zip(points, expected):
        assert math.isclose(measured, target, abs_tol=50e-6), (points, expected)
    return {"input_differential_V": [0.01, 0.05, 0.15],
            "output_points": [{"time_s": t, "diff_V": v} for t, v in points],
            "gain_error": gain_error, "absolute_tolerance_V": 50e-6}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--spectre", default="spectre")
    parser.add_argument("--models", type=Path,
                        default=Path(__file__).resolve().parents[1] / "models/adc_behavioral")
    args = parser.parse_args()
    # Refuse to reuse a run directory; preserve reproducibility and diagnostics.
    args.output.mkdir(parents=True, exist_ok=False)
    if not args.models.is_dir():
        raise FileNotFoundError(args.models)
    spectre = shutil.which(args.spectre)
    if not spectre:
        raise FileNotFoundError(f"Spectre executable not found: {args.spectre}")
    version = subprocess.run([spectre, "-W"], capture_output=True, text=True,
                             timeout=30)
    report = {"model_level": "teaching_behavioral_no_PDK", "spectre": spectre,
              "spectre_version": (version.stdout + version.stderr).strip(), "runs": [],
              "original_OA_modified": False, "transistor_simulation": False}
    cases = [("sar_nominal", sar_netlist("300p")),
             ("sar_timeout", sar_netlist("3n")),
             ("residue_nominal", residue_netlist(0)),
             ("residue_gain_error", residue_netlist(0.01))]
    for name, netlist in cases:
        run = args.output / name
        run.mkdir()
        for filename in ["async_sar8.va", "residue_amp.va"]:
            shutil.copyfile(args.models / filename, run / filename)
        (run / "residue_probe.va").write_text(RESIDUE_MONITOR)
        (run / "input.scs").write_text(netlist)
        proc = subprocess.run([spectre, "input.scs", "+log", "spectre.log",
                               "-format", "psfascii", "-raw", "psf"],
                              cwd=run, capture_output=True, text=True, timeout=120)
        (run / "stdout.txt").write_text(proc.stdout + proc.stderr)
        log = (run / "spectre.log").read_text(errors="replace") if (run / "spectre.log").exists() else proc.stdout
        if proc.returncode != 0 or not re.search(r"0 errors", log):
            raise RuntimeError(f"Spectre failed in {run}; inspect preserved log")
        checks = (inspect_sar(log, name == "sar_timeout") if name.startswith("sar_")
                  else inspect_residue(log, 0.01 if name.endswith("gain_error") else 0))
        report["runs"].append({"name": name, "exit_code": proc.returncode,
                              "netlist_sha256": digest(run / "input.scs"),
                              "model_sha256": {x: digest(run / x) for x in
                                               ["async_sar8.va", "residue_amp.va"]},
                              "checks": checks,
                              "summary": re.findall(r"spectre completes.*", log),
                              "warning_lines": [s for s in log.splitlines()
                                                if "WARNING" in s or "Warning" in s]})
        (args.output / "summary.json").write_text(json.dumps(report, indent=2) + "\n")
        print(name, json.dumps(checks), flush=True)


if __name__ == "__main__":
    main()
