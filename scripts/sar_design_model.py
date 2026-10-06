"""Reproducible SAR design examples: budgets, weighted search and FFT.

Offline teaching calculations only. No PDK, OA, Spectre or silicon results.
The capacitor mismatch model assumes independent unit errors and ideal grouping;
it excludes gradients, parasitics and routing correlation.
"""
from dataclasses import dataclass
from pathlib import Path
import argparse
import hashlib
import json
import math
import numpy as np

K_B = 1.380649e-23


@dataclass(frozen=True)
class Spec:
    bits: int = 10
    fs_Hz: float = 20e6
    differential_span_V: float = 2.0
    enob_target: float = 9.0
    temperature_K: float = 300.0
    sampling_noise_rms_V: float = 0.6e-3
    comparator_noise_rms_V: float = 0.4e-3
    reference_noise_rms_V: float = 0.3e-3
    other_noise_rms_V: float = 0.2e-3
    provisional_unit_C_F: float = 10e-15
    acquisition_s: float = 10e-9
    analog_error_lsb: float = 0.25
    output_guard_s: float = 6e-9
    dac_time_s: float = 2.2e-9
    comparator_time_s: float = 0.3e-9
    reset_time_s: float = 0.3e-9
    logic_time_s: float = 0.2e-9


def budget(spec):
    if not all(math.isfinite(value) for value in spec.__dict__.values()):
        raise ValueError("Budget inputs must be finite")
    if spec.bits < 2 or spec.fs_Hz <= 0 or spec.differential_span_V <= 0:
        raise ValueError("Invalid resolution, sample rate or span")
    if spec.sampling_noise_rms_V <= 0 or spec.temperature_K <= 0:
        raise ValueError("Noise allocation and absolute temperature must be positive")
    levels = 1 << spec.bits
    lsb = spec.differential_span_V / levels
    signal_rms = spec.differential_span_V / (2 * math.sqrt(2))
    snr_goal = 6.02 * spec.enob_target + 1.76
    total_allow = signal_rms / (10 ** (snr_goal / 20))
    quant_rms = lsb / math.sqrt(12)
    if total_allow <= quant_rms:
        raise ValueError("No positive nonquantization noise margin under this approximation")
    analog_allow = math.sqrt(total_allow ** 2 - quant_rms ** 2)
    allocations = [spec.sampling_noise_rms_V, spec.comparator_noise_rms_V,
                   spec.reference_noise_rms_V, spec.other_noise_rms_V]
    if any(value < 0 for value in allocations):
        raise ValueError("Noise allocations must be nonnegative")
    if spec.provisional_unit_C_F <= 0 or spec.acquisition_s <= 0 or spec.dac_time_s <= 0:
        raise ValueError("Capacitance and acquisition/DAC windows must be positive")
    if not 0 < spec.analog_error_lsb < (levels / 2):
        raise ValueError("Settling allowance must be positive and below the DAC step")
    if any(value < 0 for value in (spec.output_guard_s, spec.comparator_time_s,
                                   spec.reset_time_s, spec.logic_time_s)):
        raise ValueError("Timing allocations must be nonnegative")
    assigned_rms = math.sqrt(quant_rms ** 2 + sum(x ** 2 for x in allocations))
    # Independent, equally sized sampled capacitors on both differential sides.
    c_noise = 2 * K_B * spec.temperature_K / spec.sampling_noise_rms_V ** 2
    c_array = levels * spec.provisional_unit_C_F
    error = spec.analog_error_lsb * lsb
    # Conservative differential full-span step, single exponential assumption.
    tau = spec.acquisition_s / math.log(spec.differential_span_V / error)
    dac_tau = spec.dac_time_s / math.log((spec.differential_span_V / 2) / error)
    per_bit = spec.dac_time_s + spec.comparator_time_s + spec.reset_time_s + spec.logic_time_s
    period = 1 / spec.fs_Hz
    time_used = spec.acquisition_s + spec.bits * per_bit + spec.output_guard_s
    return {"LSB_V": lsb, "fullscale_sine_rms_V": signal_rms,
            "ideal_quantization_rms_V": quant_rms, "SNDR_target_dB": snr_goal,
            "total_error_rms_allowance_V": total_allow,
            "nonquantization_rms_allowance_V": analog_allow,
            "allocated_uncorrelated_total_rms_V": assigned_rms,
            "allocated_noise_only_SNR_dB": 20 * math.log10(signal_rms / assigned_rms),
            "C_per_side_kTC_only_F": c_noise, "provisional_C_per_side_F": c_array,
            "sampling_noise_at_provisional_C_V": math.sqrt(2 * K_B * spec.temperature_K / c_array),
            "acquisition_error_V": error, "maximum_single_pole_tau_s": tau,
            "maximum_Rtotal_at_provisional_C_ohm": tau / c_array,
            "maximum_DAC_single_pole_tau_s": dac_tau,
            "period_s": period, "conservative_per_bit_s": per_bit,
            "time_used_s": time_used, "remaining_margin_s": period - time_used,
            "assumptions": "uncorrelated RMS; fullscale sine; differential 2kT/C; single-pole full-span step; conservative non-overlap timing"}


def weights(bits, span, unit_sigma, seed):
    if not 2 <= bits <= 12 or span <= 0 or not 0 <= unit_sigma <= 0.1:
        raise ValueError("Supported teaching range: 2..12 bits, positive span, unit sigma 0..10%")
    rng = np.random.default_rng(seed)
    units = 2.0 ** np.arange(bits - 1, -1, -1)
    groups = units * (1 + rng.normal(size=bits) * unit_sigma / np.sqrt(units))
    dummy = 1 + rng.normal() * unit_sigma
    if np.any(groups <= 0) or dummy <= 0:
        raise ValueError("Nonpositive capacitor in teaching mismatch draw")
    return span * groups / (groups.sum() + dummy)


def convert(x, bit_weights, rng=None, cmp_sigma=0.0, vos=0.0,
            dac_time=2.2e-9, tau=0.0):
    if cmp_sigma < 0 or tau < 0 or dac_time <= 0:
        raise ValueError("Invalid comparator noise or settling condition")
    if cmp_sigma and rng is None:
        raise ValueError("Comparator noise requires an explicit random generator")
    code = 0
    prefix_voltage = 0.0
    settled_voltage = 0.0
    trace = []
    for index, w in enumerate(bit_weights):
        target = prefix_voltage + w
        settled_voltage = (target if tau == 0 else target +
                           (settled_voltage - target) * math.exp(-dac_time / tau))
        noise = rng.normal(0, cmp_sigma) if cmp_sigma and rng is not None else 0.0
        keep = x - settled_voltage >= vos + noise
        if keep:
            prefix_voltage = target
            code |= 1 << (len(bit_weights) - index - 1)
        trace.append({"bit": len(bit_weights) - index - 1, "trial_V": float(target),
                      "settled_trial_V": float(settled_voltage), "keep": bool(keep),
                      "code_prefix": code})
    return code, trace


def transition_metrics(bit_weights, span):
    levels = 1 << len(bit_weights)
    transitions = []
    for code in range(1, levels):
        low, high = 0.0, span
        for _ in range(28):
            mid = (low + high) / 2
            observed, _ = convert(mid, bit_weights)
            if observed >= code:
                high = mid
            else:
                low = mid
        transitions.append((low + high) / 2)
    transitions = np.asarray(transitions)
    # Endpoint fit from first/last transition; exclude outer saturated bins.
    lsb_fit = (transitions[-1] - transitions[0]) / (levels - 2)
    inl = (transitions - (transitions[0] + np.arange(levels - 1) * lsb_fit)) / lsb_fit
    widths = np.diff(transitions)
    dnl = widths / lsb_fit - 1
    tolerance = span / (2 ** 26)
    return {"fit": "first-to-last transition endpoint; outer bins excluded",
            "fitted_LSB_V": float(lsb_fit), "max_abs_INL_LSB": float(np.abs(inl).max()),
            "min_DNL_LSB": float(dnl.min()), "max_DNL_LSB": float(dnl.max()),
            "zero_width_inner_bins_at_numeric_resolution": int((widths <= tolerance).sum()),
            "transition_search_tolerance_V": tolerance}


def fft_metrics(codes, span, bits, tone_bin):
    codes = np.asarray(codes, dtype=float)
    n = len(codes)
    if n < 32 or n % 2 or not 0 < tone_bin < n // 2 or math.gcd(tone_bin, n) != 1:
        raise ValueError("Need a coherent coprime tone bin below Nyquist")
    y = (codes + 0.5) * span / (1 << bits)
    y -= y.mean()
    spectrum = np.fft.rfft(y) / n
    power = np.abs(spectrum) ** 2
    power[1:-1] *= 2  # Even-length record, one-sided power; Nyquist not doubled.
    signal = power[tone_bin]
    distortion_bins = set()
    for harmonic in range(2, 6):
        b = (harmonic * tone_bin) % n
        b = min(b, n - b)
        if b not in (0, tone_bin):
            distortion_bins.add(b)
    residual = power[1:].sum() - signal
    harmonic_power = sum(power[b] for b in distortion_bins)
    noise = max(residual - harmonic_power, np.finfo(float).tiny)
    sndr = 10 * math.log10(signal / max(residual, np.finfo(float).tiny))
    return {"record_length": n, "tone_bin": tone_bin, "window": "rectangular coherent",
            "harmonic_orders_removed_from_SNR": [2, 3, 4, 5],
            "SNR_dB": 10 * math.log10(signal / noise), "SNDR_dB": sndr,
            "THD_dBc_orders_2_to_5": 10 * math.log10(max(harmonic_power, np.finfo(float).tiny) / signal),
            "ENOB_from_measured_amplitude": (sndr - 1.76) / 6.02}


def plot_examples(spec, result, directory):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    c = np.logspace(-14, -10, 400)
    noise = np.sqrt(2 * K_B * spec.temperature_K / c)
    fig, ax = plt.subplots(figsize=(8, 4.5), layout="constrained")
    ax.loglog(c * 1e12, noise * 1e6, label="Independent differential 2kT/C")
    ax.axhline(spec.sampling_noise_rms_V * 1e6, color="#d07a26", ls="--", label="Teaching noise allocation")
    ax.axvline(result['budget']['provisional_C_per_side_F'] * 1e12,
               color="#5b8b52", ls=":", label="Provisional array; unit C not PDK-derived")
    ax.set(xlabel="Sampling C per side (pF)", ylabel="Differential RMS noise (uV)",
           title="Noise lower bound does not establish CDAC matching or linearity")
    ax.legend(fontsize=8);ax.grid(alpha=.2, which="both")
    fig.savefig(directory / "noise-capacitance.png", dpi=170);plt.close(fig)
    tau = np.logspace(-11, -8, 400)
    error_lsb = spec.differential_span_V * np.exp(-spec.acquisition_s / tau) / result['budget']['LSB_V']
    fig, ax = plt.subplots(figsize=(8, 4.5), layout="constrained")
    ax.semilogx(tau * 1e9, error_lsb)
    ax.axhline(spec.analog_error_lsb, color="#d07a26", ls="--", label="0.25 LSB teaching allowance")
    ax.set(xlabel="Single-pole tau (ns)", ylabel="Residual error (LSB)", ylim=(0, 2),
           title="10 ns acquisition, full-span step; no slew or multipole effects")
    ax.legend(fontsize=8);ax.grid(alpha=.2)
    fig.savefig(directory / "acquisition-settling.png", dpi=170);plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--seed", default=42, type=int)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    spec = Spec()
    ideal = weights(spec.bits, spec.differential_span_V, 0, args.seed)
    mismatched = weights(spec.bits, spec.differential_span_V, 0.01, args.seed)
    n, tone_bin = 2048, 901
    fin = tone_bin * spec.fs_Hz / n
    result = {"date": "2026-10-05", "evidence_level": "offline_python_teaching_model",
              "new_EDA_simulation": False, "PDK_used": False,
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "seed": args.seed, "spec": spec.__dict__, "budget": budget(spec),
              "static_ideal": transition_metrics(ideal, spec.differential_span_V),
              "static_mismatch": transition_metrics(mismatched, spec.differential_span_V),
              "mismatch_unit_sigma_relative": 0.01,
              "mismatch_weights_V": mismatched.tolist(), "dynamic_cases": []}
    cases = [("ideal", ideal, 0, 0, 0, 0),
             ("unit_mismatch_1pct_one_seed", mismatched, 0, 0, 0, 0),
             ("sampling_and_comparator_noise", ideal, 0.6e-3, 0.4e-3, 0, 0),
             ("jitter_50ps", ideal, 0, 0, 50e-12, 0),
             ("DAC_tau_1ns", ideal, 0, 0, 0, 1e-9)]
    for name, w, sample_sigma, cmp_sigma, jitter_sigma, tau in cases:
        rng = np.random.default_rng(args.seed)
        time = np.arange(n) / spec.fs_Hz + rng.normal(0, jitter_sigma, n)
        x = spec.differential_span_V / 2 + 0.49 * spec.differential_span_V * np.sin(2 * np.pi * fin * time)
        x += rng.normal(0, sample_sigma, n)
        codes = [convert(v, w, rng, cmp_sigma, dac_time=spec.dac_time_s, tau=tau)[0] for v in x]
        metrics = fft_metrics(codes, spec.differential_span_V, spec.bits, tone_bin)
        metrics.update({"name": name, "fin_Hz": fin, "input_sine_peak_V": 0.49 * spec.differential_span_V,
                        "sampling_noise_rms_V": sample_sigma, "comparator_per_decision_noise_rms_V": cmp_sigma,
                        "jitter_rms_s": jitter_sigma, "DAC_tau_s": tau})
        result["dynamic_cases"].append(metrics)
    value = 0.63 * spec.differential_span_V
    golden = min((1 << spec.bits) - 1, max(0, math.floor(value / spec.differential_span_V * (1 << spec.bits))))
    code, trace = convert(value, ideal)
    assert code == golden
    result["example_search"] = {"unipolar_input_V": value, "code": code,
                                "independent_floor_code": golden, "trace": trace}
    (args.output / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
    plot_examples(spec, result, args.output)
    print(json.dumps({"budget": result["budget"], "static": result["static_mismatch"],
                      "dynamic": [{"case": x["name"], "SNDR_dB": x["SNDR_dB"]} for x in result["dynamic_cases"]]}, indent=2))


if __name__ == "__main__":
    main()
