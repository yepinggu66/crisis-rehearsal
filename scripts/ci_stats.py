#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v0.2 repeat statistics: event-mean Top-3 hit rate, 95% CI (t + bootstrap), variance.

The statistical unit is the **event** (30 events), not the run (90 runs). Repeated
runs are used only to estimate run-to-run noise, so the confidence interval is built
on the per-event mean with df = n_events - 1. Treating the 90 runs as 90 independent
samples would badly overstate precision.

Input (default: data/repeat_v02/scores.jsonl) -- one JSON object per run:

    {"id": "21", "run": "1", "name": "...", "md5": "...",
     "top3": [{"rank": 1, "risk": "...", "hit": "yes|partial|no", "why": "..."}],
     "path_hit": "yes|partial|no", "early_warning": 88, "comment": "..."}

Scoring: hit = yes -> 1, partial -> 0.5, no -> 0; a single run scores 0..3.
Event-mean hit rate = mean over events of (per-event mean score) / 3.

Optional baseline (default: <out>/scores_v01.jsonl) -- the v0.1 single-run scores,
used for the paired per-event replication check (v0.2 event mean - v0.1 single run).

Output: the table below on stdout, plus <out>/ci_summary.md (deterministic: no
timestamps, so re-running produces byte-identical output).

Usage:
    python scripts/ci_stats.py                              # shipped v0.2 data
    python scripts/ci_stats.py --out output_v2              # fresh re-run
    python scripts/ci_stats.py --out output_v2 --bootstrap 10000

numpy is used for the bootstrap when installed (default 10,000 resamples, fixed
seed); otherwise a pure-Python fallback runs and the output says so.
"""
import argparse
import hashlib
import json
import math
import os
import statistics as st
from collections import defaultdict
from pathlib import Path

ROOT = Path(os.environ.get("CR_ROOT") or Path(__file__).resolve().parents[1]).expanduser().resolve()
DEFAULT_OUT = ROOT / "data" / "repeat_v02"
DEFAULT_SEED = 20261026

# Two-sided 97.5% quantiles of Student's t (small table + linear interpolation).
T975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306,
        9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131,
        16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086, 25: 2.060, 29: 2.045,
        30: 2.042, 40: 2.021, 60: 2.000, 120: 1.980}


def t975(df):
    """t-distribution 97.5% quantile."""
    if df <= 0:
        return float("inf")
    keys = sorted(T975)
    if df <= keys[0]:
        return T975[keys[0]]
    if df >= keys[-1]:
        return T975[keys[-1]]
    for a, b in zip(keys, keys[1:]):
        if a <= df <= b:
            return T975[a] + (T975[b] - T975[a]) * (df - a) / (b - a)
    return 1.96


def wilson(k, n, z=1.96):
    """Wilson score interval for a binomial proportion."""
    if n == 0:
        return 0.0, 0.0
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def hit_of(run):
    """Graded score of one run: yes=1, partial=0.5, no=0 -> 0..3."""
    return sum({"yes": 1.0, "partial": 0.5}.get(str(t.get("hit", "")).lower(), 0.0)
               for t in (run.get("top3") or []))


def load_jsonl(path):
    rows = []
    if path and Path(path).is_file():
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return rows


def _percentile(sorted_vals, q):
    """Linear-interpolation percentile, matching numpy.percentile defaults."""
    if not sorted_vals:
        return float("nan")
    k = (len(sorted_vals) - 1) * q / 100.0
    lo, hi = math.floor(k), math.ceil(k)
    if lo == hi:
        return float(sorted_vals[int(k)])
    return sorted_vals[lo] * (hi - k) + sorted_vals[hi] * (k - lo)


def bootstrap_ci(vals, n_boot=10000, seed=DEFAULT_SEED):
    """Percentile bootstrap of the event-mean score. Returns (lo, hi, method)."""
    if len(vals) < 2:
        return float("nan"), float("nan"), "n/a"
    try:
        import numpy as np  # optional: much faster, and what the published CI used
    except ImportError:
        n = len(vals)
        rng = __import__("random").Random(seed)
        means = []
        for _ in range(n_boot):
            total = 0.0
            for _ in range(n):
                total += vals[rng.randrange(n)]
            means.append(total / n)
        means.sort()
        return _percentile(means, 2.5), _percentile(means, 97.5), "stdlib fallback"
    rng = np.random.default_rng(seed)
    arr = np.asarray(vals, dtype=float)
    draws = arr[rng.integers(0, len(arr), size=(n_boot, len(arr)))].mean(axis=1)
    return (float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5)),
            "numpy")


def pct(x):
    return min(100.0, max(0.0, x / 3.0 * 100.0))


def rel(path):
    """Path as shown to the reader: repo-relative when possible."""
    try:
        return Path(path).resolve().relative_to(ROOT).as_posix()
    except (ValueError, OSError):
        return Path(path).as_posix()


def sha256_file(path):
    try:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16]
    except OSError:
        return "n/a"


def find_baseline(args, out_dir):
    """Explicit --baseline first, then <out>/scores_v01.jsonl, then the shipped one."""
    candidates = []
    if args.baseline:
        candidates.append(Path(args.baseline))
    candidates.append(out_dir / "scores_v01.jsonl")
    candidates.append(DEFAULT_OUT / "scores_v01.jsonl")
    for cand in candidates:
        if cand.is_file():
            return cand.resolve()
    return None


def main():
    ap = argparse.ArgumentParser(
        description="Event-mean Top-3 hit rate, 95% CI (t + bootstrap) and variance "
                    "for the v0.2 repeated backtest.")
    ap.add_argument("--out", default=None,
                    help="directory holding scores.jsonl (default: <repo>/data/repeat_v02)")
    ap.add_argument("--scores", default=None,
                    help="explicit scores.jsonl (overrides --out/scores.jsonl)")
    ap.add_argument("--baseline", default=None,
                    help="v0.1 single-run scores.jsonl for the paired replication check "
                         "(default: <out>/scores_v01.jsonl)")
    ap.add_argument("--bootstrap", type=int, default=10000,
                    help="bootstrap resamples (default: %(default)s; 0 disables)")
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED,
                    help="bootstrap RNG seed (default: %(default)s)")
    ap.add_argument("--no-md", action="store_true", help="do not write <out>/ci_summary.md")
    args = ap.parse_args()

    out_dir = Path(args.out).expanduser() if args.out else DEFAULT_OUT
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    scores_path = Path(args.scores).expanduser() if args.scores else out_dir / "scores.jsonl"
    if not scores_path.is_absolute():
        scores_path = (Path.cwd() / scores_path).resolve()
    if not scores_path.is_file():
        raise SystemExit(f"scores file not found: {scores_path}\n"
                         "run scripts/score_repeat.py first, or point --out/--scores at "
                         "the shipped data/repeat_v02 directory.")

    runs = [r for r in load_jsonl(scores_path) if r.get("top3")]
    if not runs:
        raise SystemExit(f"no scored runs in {scores_path} (need records with a top3 list)")

    by_event = defaultdict(list)
    for r in runs:
        by_event[str(r["id"])].append(r)
    events = sorted(by_event, key=int)
    n_ev = len(events)
    per_run_counts = [len(v) for v in by_event.values()]

    ev_mean, ev_sd, ev_ew = {}, {}, {}
    for eid, rs in by_event.items():
        hits = [hit_of(x) for x in rs]
        ev_mean[eid] = st.mean(hits)
        ev_sd[eid] = st.pstdev(hits) if len(hits) > 1 else 0.0
        ews = []
        for x in rs:
            try:
                ews.append(float(x.get("early_warning")))
            except (TypeError, ValueError):
                pass
        ev_ew[eid] = st.mean(ews) if ews else float("nan")

    means = [ev_mean[e] for e in events]
    n = len(means)
    grand = st.mean(means)
    between_sd = st.stdev(means) if n > 1 else 0.0
    se = between_sd / (n ** 0.5)
    half = t975(n - 1) * se
    ci_t = (grand - half, grand + half)
    ci_boot = bootstrap_ci(means, args.bootstrap, args.seed) if args.bootstrap > 0 \
        else (float("nan"), float("nan"), "disabled")
    within_sd = st.mean([ev_sd[e] for e in events])
    within_sd_med = st.median([ev_sd[e] for e in events])
    unstable = [e for e in events if ev_sd[e] >= 0.5]
    stable = [e for e in events if ev_sd[e] == 0.0]

    k_full = sum(1 for e in events if ev_mean[e] >= 2.999)
    w_lo, w_hi = wilson(k_full, n)
    best_any = sum(1 for e in events if max(hit_of(x) for x in by_event[e]) >= 3)
    n_full_runs = sum(1 for r in runs if hit_of(r) >= 3)

    ews = [ev_ew[e] for e in events if not math.isnan(ev_ew[e])]
    ew_mean = st.mean(ews) if ews else float("nan")
    ew_half = (t975(len(ews) - 1) * st.stdev(ews) / (len(ews) ** 0.5)) if len(ews) > 1 else 0.0

    # Paired comparison against the v0.1 single-run baseline, event by event.
    baseline_path = find_baseline(args, out_dir)
    single = {}
    if baseline_path:
        for r in load_jsonl(baseline_path):
            if r.get("top3"):
                single[str(r["id"])] = hit_of(r)
    common = [e for e in events if e in single]
    diff_mean = diff_half = float("nan")
    if len(common) > 1:
        paired = [ev_mean[e] - single[e] for e in common]
        diff_mean = st.mean(paired)
        diff_half = t975(len(paired) - 1) * st.stdev(paired) / (len(paired) ** 0.5)

    head = [
        "# v0.2 repeat statistics (generated by scripts/ci_stats.py)",
        "",
        f"- Events: **{n_ev}**; runs: **{len(runs)}** "
        + (f"({min(per_run_counts)} runs per event)"
           if min(per_run_counts) == max(per_run_counts)
           else f"({min(per_run_counts)}-{max(per_run_counts)} runs per event)"),
        f"- Scores input: `{rel(scores_path)}` (sha256 {sha256_file(scores_path)})",
        f"- v0.1 baseline: `{rel(baseline_path)}`" if baseline_path
        else "- v0.1 baseline: not found (paired comparison skipped)",
        "- Statistical unit: event. Repeats estimate run-to-run noise; they are NOT "
        "independent samples.",
        "- Scoring: hit = yes 1 / partial 0.5 / no 0, per run 0-3; hit rate = "
        "event-mean score / 3.",
        "",
        "## Headline (the numbers quoted in README.md)",
        "",
        "| Metric | Value | 95% CI / spread | Note |",
        "|---|---|---|---|",
        f"| **Top-3 risk hit rate** (event mean) | **{grand / 3 * 100:.1f}%** "
        f"| {pct(ci_t[0]):.1f}-{pct(ci_t[1]):.1f}% (t, df={n - 1}) "
        f"| mean {grand:.2f}/3, n={n} events |",
        f"| Same, percentile bootstrap | {grand / 3 * 100:.1f}% "
        f"| {pct(ci_boot[0]):.1f}-{pct(ci_boot[1]):.1f}% "
        f"| {args.bootstrap} resamples, seed {args.seed}, {ci_boot[2]} |",
        f"| Paired diff vs v0.1 single run | {diff_mean:+.2f}/3 "
        f"| ±{diff_half:.2f} | {len(common)} events, paired |",
        "",
        "## Variance and stability",
        "",
        "| Metric | Value | Meaning |",
        "|---|---|---|",
        f"| Between-event SD | {between_sd:.2f}/3 | spread of difficulty across events |",
        f"| Within-event SD (mean) | {within_sd:.2f}/3 | same event, re-run: run-to-run noise |",
        f"| Within-event SD (median) | {within_sd_med:.2f}/3 | |",
        f"| Events identical in every run | {len(stable)}/{n} = {len(stable) / n * 100:.0f}% "
        f"| same score all {min(per_run_counts)} runs |",
        f"| Events with within SD >= 0.5 | {len(unstable)}/{n} = {len(unstable) / n * 100:.0f}% "
        f"| {', '.join('#' + e for e in unstable) or 'none'} |",
        f"| Events at a perfect 3/3 in every run | {k_full}/{n} = {k_full / n * 100:.0f}% "
        f"| Wilson {w_lo * 100:.0f}-{w_hi * 100:.0f}% |",
        f"| Events at a perfect 3/3 at least once | {best_any}/{n} = "
        f"{best_any / n * 100:.0f}% | headroom from reading a consensus of repeats |",
        f"| Runs scoring a perfect 3/3 | {n_full_runs}/{len(runs)} = "
        f"{n_full_runs / len(runs) * 100:.0f}% | descriptive only (runs are correlated) |",
        f"| Early-warning quality | {ew_mean:.0f}/100 | {ew_mean - ew_half:.0f}-"
        f"{ew_mean + ew_half:.0f}, event mean ± t |",
        "",
        "## Scoring discipline (do not quote the headline without these)",
        "",
        f"1. {grand / 3 * 100:.1f}% is an **event-mean graded score**, not a binary "
        "hit/miss rate. The binary framing on 30 events is roughly ±17pp; do not mix the two.",
        f"2. {len(runs)} runs are **not** {len(runs)} independent samples; the unit is "
        f"{n} events.",
        "3. The interval covers sampling and run randomness only. It does **not** include "
        "LLM-judge error or systematic bias from a 2-round simulation.",
        f"4. Only {len(stable)} of {n} events score identically across repeats: commit to a "
        "consistent level, never to 'the same conclusion every time'.",
        "5. This is a rehearsal/backtest producing directional evidence, not a forecast.",
        "",
        f"> Reproduce: `python scripts/ci_stats.py --out {rel(out_dir)}`",
    ]
    md = "\n".join(head) + "\n"

    print(md)
    if not args.no_md:
        out_dir.mkdir(parents=True, exist_ok=True)
        md_path = out_dir / "ci_summary.md"
        md_path.write_text(md, encoding="utf-8")
        print(f"[written] {rel(md_path)}")


if __name__ == "__main__":
    main()
