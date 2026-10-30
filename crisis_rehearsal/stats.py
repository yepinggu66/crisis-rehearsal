# -*- coding: utf-8 -*-
"""Recompute every published v0.2 number from the shipped evidence pack.

The arithmetic is not re-implemented here: ``scripts/ci_stats.py`` and
``scripts/sta_stats.py`` are imported (read-only) and their functions are called.
The aggregation loops are ported line-for-line from those scripts' ``main()``
because they are not exposed as functions; ``tests/test_stats.py`` runs both
scripts as subprocesses and asserts that the CLI reproduces their printed values,
so a drift between the two paths fails the test suite instead of shipping.

Statistical unit: the **event** (30), never the run (90). Repeats estimate
run-to-run noise, they are not independent samples.
"""
from __future__ import annotations

import math
import statistics as st
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

from . import scripts_bridge as bridge
from .data import DataError, load_baseline_scores, load_clusters, load_events, load_scores
from .paths import SCORES_JSONL, sha256_file


class StatsUnavailable(RuntimeError):
    """Raised when the statistics cannot be recomputed (missing inputs)."""


#: Numbers published in README.md / data/repeat_v02/*.md. ``crh stats`` prints a
#: comparison table against these; a mismatch is a release blocker.
PUBLISHED = {
    "n_events": 30,
    "n_runs": 90,
    "hit_rate_pct": 82.2,
    "ci_t_low_pct": 78.5,
    "ci_t_high_pct": 85.9,
    "ci_bootstrap_low_pct": 78.7,
    "ci_bootstrap_high_pct": 85.6,
    "within_event_sd": 0.26,
    "identical_events": 5,
    "identical_of": 30,
    "sta": 58,
    "sta_jbar": 0.54,
    "sta_cvbar": 0.08,
    "sta_w": 0.29,
}

STA_PASS_LINE = 60
STA_FUNDING_LINE = 75


def _grade(sta: float) -> str:
    """Same reading as scripts/sta_stats.py grade()."""
    if sta >= STA_FUNDING_LINE:
        return "reproducible"
    if sta >= STA_PASS_LINE:
        return "mostly reproducible"
    return "unstable - read a consensus"


def _pct(score: float) -> float:
    """0..3 graded score -> percent of the maximum."""
    return min(100.0, max(0.0, score / 3.0 * 100.0))


def _pstdev(values: List[float]) -> float:
    return st.pstdev(values) if len(values) > 1 else 0.0


def compute(repo: Path, bootstrap: Optional[int] = 10000,
            seed: Optional[int] = None) -> dict:
    """Recompute the v0.2 statistics for *repo*.

    Returns a JSON-serialisable dict (raw floats; formatting is the caller's job).
    """
    repo = Path(repo)
    ci = bridge.ci_stats(repo)
    sta = bridge.sta_stats(repo)

    scores_path = repo / SCORES_JSONL
    if not scores_path.is_file():
        raise StatsUnavailable(f"missing evidence file: {scores_path}")
    runs = [r for r in ci.load_jsonl(scores_path) if r.get("top3")]
    if not runs:
        raise StatsUnavailable(
            f"no scored runs in {scores_path} (records need a top3 list)")
    n_boot = 10000 if bootstrap is None else int(bootstrap)
    boot_seed = getattr(ci, "DEFAULT_SEED", 20261026) if seed is None else int(seed)

    # --- headline: event-mean graded hit rate, t CI, bootstrap CI ------------
    by_event = defaultdict(list)
    for record in runs:
        by_event[str(record["id"])].append(record)
    events = sorted(by_event, key=int)
    n_events = len(events)
    per_run_counts = [len(by_event[e]) for e in events]

    ev_mean: Dict[str, float] = {}
    ev_sd: Dict[str, float] = {}
    ev_ew: Dict[str, float] = {}
    for eid, records in by_event.items():
        hits = [ci.hit_of(r) for r in records]
        ev_mean[eid] = st.mean(hits)
        ev_sd[eid] = _pstdev(hits)
        warnings = []
        for record in records:
            try:
                warnings.append(float(record.get("early_warning")))
            except (TypeError, ValueError):
                pass
        ev_ew[eid] = st.mean(warnings) if warnings else float("nan")

    means = [ev_mean[e] for e in events]
    grand = st.mean(means)
    between_sd = st.stdev(means) if n_events > 1 else 0.0
    se = between_sd / (n_events ** 0.5)
    half = ci.t975(n_events - 1) * se
    ci_t = (grand - half, grand + half)
    if n_boot > 0:
        boot_lo, boot_hi, boot_method = ci.bootstrap_ci(means, n_boot, boot_seed)
    else:
        boot_lo, boot_hi, boot_method = float("nan"), float("nan"), "disabled"

    within_sd = st.mean([ev_sd[e] for e in events])
    within_sd_median = st.median([ev_sd[e] for e in events])
    unstable = [e for e in events if ev_sd[e] >= 0.5]
    stable = [e for e in events if ev_sd[e] == 0.0]

    k_full = sum(1 for e in events if ev_mean[e] >= 2.999)
    wilson_lo, wilson_hi = ci.wilson(k_full, n_events)
    best_any = sum(1 for e in events if max(ci.hit_of(x) for x in by_event[e]) >= 3)
    n_full_runs = sum(1 for r in runs if ci.hit_of(r) >= 3)

    early_warnings = [ev_ew[e] for e in events if not math.isnan(ev_ew[e])]
    ew_mean = st.mean(early_warnings) if early_warnings else float("nan")
    ew_half = (ci.t975(len(early_warnings) - 1) * st.stdev(early_warnings)
               / (len(early_warnings) ** 0.5)) if len(early_warnings) > 1 else 0.0

    # --- paired replication check against the v0.1 single-run baseline ------
    baseline_rows = load_baseline_scores(repo)
    single = {str(r["id"]): ci.hit_of(r) for r in baseline_rows if r.get("top3")}
    common = [e for e in events if e in single]
    paired = None
    if len(common) > 1:
        diffs = [ev_mean[e] - single[e] for e in common]
        paired = {
            "diff_per_3": st.mean(diffs),
            "half_per_3": ci.t975(len(diffs) - 1) * st.stdev(diffs) / (len(diffs) ** 0.5),
            "n_events": len(common),
        }

    # --- STA stability metric (ported from scripts/sta_stats.py main()) -----
    per_event_sta = _sta_per_event(repo, sta, by_event, events)

    jb = st.mean([per_event_sta[e]["jbar"] for e in events])
    cvb = st.mean([per_event_sta[e]["cv_bar"] for e in events])
    wb = st.mean([per_event_sta[e]["w"] for e in events])
    sta_batch = 100 * (0.40 * jb + 0.30 * (1 - cvb) + 0.30 * wb)

    # --- names from events.csv (canonical), falling back to judge records ----
    try:
        catalogue = load_events(repo)
    except DataError:
        catalogue = {}

    per_event: Dict[str, dict] = {}
    for eid in events:
        records = sorted(by_event[eid], key=lambda r: _run_key(r.get("run")))
        event = catalogue.get(eid)
        per_event[eid] = {
            "id": eid,
            "name": event.title if event else (records[0].get("name") or ""),
            "name_en": event.event_name_en if event else "",
            "n_runs": len(records),
            "scores": [ci.hit_of(r) for r in records],
            "mean": ev_mean[eid],
            "sd": ev_sd[eid],
            "hit_rate_pct": _pct(ev_mean[eid]),
            "early_warning": None if math.isnan(ev_ew[eid]) else ev_ew[eid],
            "path_hits": [r.get("path_hit") for r in records],
            "sta": per_event_sta[eid],
            "runs": [
                {
                    "run": str(r.get("run")),
                    "md5": r.get("md5"),
                    "score": ci.hit_of(r),
                    "early_warning": r.get("early_warning"),
                    "path_hit": r.get("path_hit"),
                }
                for r in records
            ],
        }

    result: dict = {
        "tool": "crh",
        "repo": str(repo),
        "scores_file": SCORES_JSONL.as_posix(),
        "scores_sha256": sha256_file(scores_path),
        "baseline_file": ("data/repeat_v02/scores_v01.jsonl" if baseline_rows else None),
        "clusters_file": ("data/repeat_v02/item_clusters.json"
                          if (repo / "data" / "repeat_v02" / "item_clusters.json").is_file()
                          else None),
        "n_events": n_events,
        "n_runs": len(runs),
        "runs_per_event_min": min(per_run_counts),
        "runs_per_event_max": max(per_run_counts),
        "hit": {
            "mean_score": grand,
            "rate_pct": _pct(grand),
            "ci_t_pct": [_pct(ci_t[0]), _pct(ci_t[1])],
            "df": n_events - 1,
            "ci_bootstrap_pct": [_pct(boot_lo), _pct(boot_hi)],
            "bootstrap_resamples": n_boot,
            "bootstrap_seed": boot_seed,
            "bootstrap_method": boot_method,
        },
        "paired_v01": paired,
        "variance": {
            "between_sd": between_sd,
            "within_sd": within_sd,
            "within_sd_median": within_sd_median,
        },
        "identical": {"n": len(stable), "of": n_events,
                      "pct": len(stable) / n_events * 100.0},
        "unstable": {"ids": [int(e) for e in unstable], "n": len(unstable),
                     "of": n_events, "pct": len(unstable) / n_events * 100.0},
        "perfect": {
            "all_runs": k_full,
            "any_run": best_any,
            "runs": n_full_runs,
            "wilson_pct": [wilson_lo * 100.0, wilson_hi * 100.0],
        },
        "early_warning": {
            "mean": ew_mean,
            "lo": ew_mean - ew_half,
            "hi": ew_mean + ew_half,
        },
        "sta": {
            "batch": sta_batch,
            "jbar": jb,
            "cvbar": cvb,
            "w": wb,
            "item_merge": per_event_sta.get("_method", "n/a"),
            "pass_line": STA_PASS_LINE,
            "funding_line": STA_FUNDING_LINE,
            "verdict": "FAILED" if sta_batch < STA_PASS_LINE else "pass",
            "reading": _grade(sta_batch),
        },
        "per_event": per_event,
    }
    result["published_check"] = compare_published(result)
    result["published_match"] = all(row["match"] for row in result["published_check"])
    return result


def _run_key(value):
    try:
        return (0, int(value))
    except (TypeError, ValueError):
        return (1, str(value))


def _sta_per_event(repo: Path, sta, by_event, events: List[str]) -> Dict[str, dict]:
    """Port of the per-event loop in scripts/sta_stats.py::main().

    Uses the script's own ``norm``/``jaccard``/``kendall_w``/``UF``/``similar``
    helpers so the metric definition lives in exactly one place.
    """
    clusters = load_clusters(repo)
    method = ("LLM semantic merge (cluster_items.py)" if clusters
              else "literal similarity fallback (no item_clusters.json)")
    per: Dict[str, dict] = {}
    for eid in events:
        records = sorted(by_event[eid], key=lambda x: sta.run_order(x.get("run")))
        items = []  # (run_index, raw, normalised, run label, rank)
        for run_index, record in enumerate(records):
            for item in record.get("top3", []):
                items.append((run_index, str(item.get("risk", "")),
                              sta.norm(item.get("risk", "")),
                              str(record.get("run")), item.get("rank")))
        cluster_of = {}
        if eid in clusters:
            mapping = clusters[eid]
            for index, item in enumerate(items):
                cluster_of[index] = mapping.get(f"{item[3]}:{item[4]}", f"x{index}")
        else:
            union = sta.UF()
            for i in range(len(items)):
                for j in range(i + 1, len(items)):
                    if sta.similar(items[i][2], items[j][2]):
                        union.union(i, j)
            for index in range(len(items)):
                cluster_of[index] = union.find(index)

        sets, ranks = [], []
        for run_index in range(len(records)):
            current_set, rank_map = set(), {}
            for index, item in enumerate(items):
                if item[0] != run_index:
                    continue
                cluster = cluster_of[index]
                current_set.add(cluster)
                if cluster not in rank_map:
                    rank_map[cluster] = len(rank_map) + 1
            sets.append(current_set)
            ranks.append(rank_map)

        jaccards = [sta.jaccard(sets[a], sets[b])
                    for a in range(len(sets)) for b in range(a + 1, len(sets))]
        jbar = st.mean(jaccards) if jaccards else 1.0
        n_union = len({c for s in sets for c in s})
        w = sta.kendall_w(ranks, n_union)

        hits = [sta.hit_of(r) for r in records]
        warnings = []
        for record in records:
            try:
                warnings.append(float(record.get("early_warning")))
            except (TypeError, ValueError):
                pass

        def cv(values: List[float]) -> float:
            if len(values) < 2:
                return 0.0
            mean = st.mean(values)
            if mean == 0:
                return 1.0
            return min(1.0, st.pstdev(values) / mean)

        cv_hr = cv(hits)
        cv_ew = cv(warnings) if len(warnings) >= 2 else 0.0
        cv_bar = (cv_hr + cv_ew) / 2
        value = 100 * (0.40 * jbar + 0.30 * (1 - cv_bar) + 0.30 * w)
        per[eid] = {
            "value": value,
            "jbar": jbar,
            "d": 1 - jbar,
            "w": w,
            "cv_hr": cv_hr,
            "cv_bar": cv_bar,
            "hits": hits,
            "reading": _grade(value),
            "disagreement": (1 - jbar) >= 0.4,
            "item_merge": len(clusters) > 0,
        }
    per["_method"] = method
    return per


def _decimals(value) -> int:
    text = str(value)
    return len(text.split(".")[1]) if "." in text else 0


def _match(published, computed: float) -> bool:
    if isinstance(published, int):
        return int(round(computed)) == published
    return round(computed, _decimals(published)) == published


def compare_published(result: dict) -> List[dict]:
    """Compare a compute() result with the numbers published in the README."""
    hit = result["hit"]
    variance = result["variance"]
    values = {
        "n_events": float(result["n_events"]),
        "n_runs": float(result["n_runs"]),
        "hit_rate_pct": hit["rate_pct"],
        "ci_t_low_pct": hit["ci_t_pct"][0],
        "ci_t_high_pct": hit["ci_t_pct"][1],
        "ci_bootstrap_low_pct": hit["ci_bootstrap_pct"][0],
        "ci_bootstrap_high_pct": hit["ci_bootstrap_pct"][1],
        "within_event_sd": variance["within_sd"],
        "identical_events": float(result["identical"]["n"]),
        "identical_of": float(result["identical"]["of"]),
        "sta": result["sta"]["batch"],
        "sta_jbar": result["sta"]["jbar"],
        "sta_cvbar": result["sta"]["cvbar"],
        "sta_w": result["sta"]["w"],
    }
    rows = []
    for key, published in PUBLISHED.items():
        computed = values[key]
        rows.append({
            "metric": key,
            "published": published,
            "computed": computed,
            "match": _match(published, computed),
        })
    return rows


def fmt_pct(value: float, digits: int = 1) -> str:
    return f"{value:.{digits}f}%"


def as_text(result: dict) -> str:
    """The ``crh stats`` console report (ASCII box art, English)."""
    hit = result["hit"]
    variance = result["variance"]
    stability = result["sta"]
    lines: List[str] = []
    add = lines.append

    add(f"Crisis Rehearsal Engine — published statistics (crh {_version()})")
    add("=" * 78)
    add(f"repo            : {result['repo']}")
    add(f"scores          : {result['scores_file']}  sha256 {result['scores_sha256'][:16]}")
    if result["clusters_file"]:
        add(f"item merge      : {result['clusters_file']}")
    add(f"events / runs   : {result['n_events']} events x "
        f"{_runs_per_event(result)} = {result['n_runs']} runs")
    add("statistical unit: EVENT (repeats estimate run-to-run noise, "
        "they are not independent samples)")
    add("")
    add("Headline (the numbers quoted in README.md)")
    add("-" * 78)
    add(f"  Top-3 risk hit rate (event mean) : {fmt_pct(hit['rate_pct'])}"
        f"   [mean {hit['mean_score']:.2f}/3, n={result['n_events']} events]")
    add(f"  95% CI, t-distribution (primary) : "
        f"{fmt_pct(hit['ci_t_pct'][0])} - {fmt_pct(hit['ci_t_pct'][1])}"
        f"   (df={hit['df']})")
    add(f"  95% CI, {hit['bootstrap_resamples']:,}-sample bootstrap : "
        f"{fmt_pct(hit['ci_bootstrap_pct'][0])} - {fmt_pct(hit['ci_bootstrap_pct'][1])}"
        f"   ({hit['bootstrap_method']}, seed {hit['bootstrap_seed']})")
    if result["paired_v01"]:
        paired = result["paired_v01"]
        add(f"  Paired diff vs v0.1 single run   : {paired['diff_per_3']:+.2f}/3"
            f"   (±{paired['half_per_3']:.2f}, n={paired['n_events']} events)")
    add("")
    add("Variance and stability")
    add("-" * 78)
    add(f"  Between-event SD                 : {variance['between_sd']:.2f}/3"
        "   (difficulty spread across events)")
    add(f"  Within-event SD (mean)           : {variance['within_sd']:.2f}/3"
        "   (same event, re-run)")
    add(f"  Within-event SD (median)         : {variance['within_sd_median']:.2f}/3")
    add(f"  Events identical in every run    : {result['identical']['n']}"
        f"/{result['identical']['of']} = {result['identical']['pct']:.0f}%")
    add(f"  Events with within SD >= 0.5     : {result['unstable']['n']}"
        f"/{result['unstable']['of']} = {result['unstable']['pct']:.0f}%"
        f"   (#{', #'.join(str(i) for i in result['unstable']['ids']) or 'none'})")
    add(f"  Events at a perfect 3/3, all runs: {result['perfect']['all_runs']}"
        f"/{result['n_events']} (Wilson {result['perfect']['wilson_pct'][0]:.0f}"
        f"-{result['perfect']['wilson_pct'][1]:.0f}%)")
    add(f"  Events at a perfect 3/3, any run : {result['perfect']['any_run']}"
        f"/{result['n_events']} = {result['perfect']['any_run'] / result['n_events'] * 100:.0f}%")
    add(f"  Runs scoring a perfect 3/3       : {result['perfect']['runs']}"
        f"/{result['n_runs']} = {result['perfect']['runs'] / result['n_runs'] * 100:.0f}%"
        "   (descriptive only, runs are correlated)")
    add(f"  Early-warning quality            : {result['early_warning']['mean']:.0f}/100"
        f"   ({result['early_warning']['lo']:.0f}-{result['early_warning']['hi']:.0f},"
        " event mean ± t)")
    add("")
    add("Stability STA (internal template section 2.5)")
    add("-" * 78)
    add(f"  STA = 100 * [0.40*J-bar + 0.30*(1 - CV-bar) + 0.30*Kendall W]")
    add(f"  STA {stability['batch']:.0f}  ->  {stability['verdict']}"
        f"   (pass line {stability['pass_line']}, funding line {stability['funding_line']})")
    add(f"  J-bar item agreement {stability['jbar']:.2f}   "
        f"CV-bar {stability['cvbar']:.2f}   Kendall W {stability['w']:.2f}")
    add(f"  item merge: {stability['item_merge']}")
    add("")
    add("Published-number check")
    add("-" * 78)
    for row in result["published_check"]:
        mark = "OK  " if row["match"] else "DIFF"
        computed = (f"{row['computed']:.1f}" if abs(row["computed"]) >= 1
                    else f"{row['computed']:.2f}")
        add(f"  [{mark}] {row['metric']:<24} published {row['published']!s:<8}"
            f" computed {computed}")
    add("")
    add("Scoring discipline (do not quote the headline without these)")
    add("-" * 78)
    add(f"  1. {fmt_pct(hit['rate_pct'])} is an EVENT-MEAN GRADED SCORE, not a binary"
        " hit/miss rate.")
    add("     The binary framing on 30 events is roughly ±17pp; do not mix the two.")
    add(f"  2. {result['n_runs']} runs are NOT {result['n_runs']} independent samples;"
        f" the unit is {result['n_events']} events.")
    add("  3. The interval covers sampling and run randomness only. It does NOT include")
    add("     LLM-judge error or the systematic bias of a 2-round simulation.")
    add(f"  4. Only {result['identical']['n']} of {result['n_events']} events score"
        " identically across repeats: commit to a")
    add("     consistent level, never to 'the same conclusion every time'.")
    add("  5. This is a rehearsal/backtest producing DIRECTIONAL EVIDENCE, not a forecast.")
    add("")
    add("Source: data/repeat_v02 (90 judge records, shipped in this repository).")
    add("Recomputed by importing scripts/ci_stats.py + scripts/sta_stats.py — "
        "no API key, no network.")
    return "\n".join(lines)


def as_json(result: dict) -> str:
    import json

    return json.dumps(result, ensure_ascii=False, indent=2, sort_keys=False)


def _runs_per_event(result: dict) -> str:
    low = result["runs_per_event_min"]
    high = result["runs_per_event_max"]
    return f"{low} runs per event" if low == high else f"{low}-{high} runs per event"


def _version() -> str:
    from . import __version__

    return __version__
