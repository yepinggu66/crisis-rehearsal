#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v0.2 stability metric STA: are repeated runs of the same event the same thing?

Definition (internal evaluation template section 2.5):

    J-bar : item-level agreement. Top-3 risk items of every pair of runs are compared
            with Jaccard once items have been merged by meaning (similarity >= 0.85;
            cluster_items.py produces the LLM merge, a literal-similarity fallback is
            built in).
    CV-bar: metric-level coefficient of variation of HR@3 and early_warning across
            runs (sd/mean; mean=0 -> 1; capped at 1).
    W     : rank agreement (Kendall's W) across runs over the union of items.

    STA = 100 * [0.40 * J-bar + 0.30 * (1 - CV-bar) + 0.30 * W]
    Disagreement D = 1 - J-bar; events with D >= 0.4 must be reported as a split
    (consensus + disagreement) instead of a single number.

Input (default): data/repeat_v02/scores.jsonl and data/repeat_v02/item_clusters.json.
Output: the tables below on stdout, plus <out>/sta_summary.md (deterministic).

Usage:
    python scripts/sta_stats.py                    # shipped v0.2 data
    python scripts/sta_stats.py --out output_v2    # fresh re-run
    python scripts/sta_stats.py --threshold 0.85   # item merge threshold
"""
import argparse
import json
import os
import re
import statistics as st
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(os.environ.get("CR_ROOT") or Path(__file__).resolve().parents[1]).expanduser().resolve()
DEFAULT_OUT = ROOT / "data" / "repeat_v02"
DEFAULT_THRESHOLD = 0.85


def norm(s):
    s = str(s or "").lower()
    return re.sub(r"[\s，。、；：！？,.;:!?\"'（）()\[\]【】《》<>·…—\-—_/\\|]+", "", s)


def bigrams(s):
    return {s[i:i + 2] for i in range(max(0, len(s) - 1))}


def similar(a, b):
    """Literal-similarity fallback used only when no cluster file is available."""
    if not a or not b:
        return False
    if a == b:
        return True
    if (a in b or b in a) and min(len(a), len(b)) / max(len(a), len(b)) >= 0.75:
        return True
    ba, bb = bigrams(a), bigrams(b)
    if ba and bb and len(ba & bb) / len(ba | bb) >= 0.35:
        return True
    return SequenceMatcher(None, a, b).ratio() >= 0.7


class UF:
    """Union-find for the literal-similarity fallback."""

    def __init__(self):
        self.p = {}

    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra


def jaccard(a, b):
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def kendall_w(rankings, n_items):
    """rankings: list of {item: rank}; items missing from a run get (n+1)/2."""
    m = len(rankings)
    if m < 2 or n_items < 2:
        return 0.0
    items = sorted({i for r in rankings for i in r})
    n = n_items
    r_sum = {}
    for it in items:
        r_sum[it] = sum(r.get(it, (n + 1) / 2) for r in rankings)
    mean_r = sum(r_sum.values()) / len(r_sum)
    s = sum((v - mean_r) ** 2 for v in r_sum.values())
    denom = m * m * (n ** 3 - n)
    if denom == 0:
        return 0.0
    return max(0.0, min(1.0, 12 * s / denom))


def hit_of(run):
    return sum({"yes": 1.0, "partial": 0.5}.get(str(t.get("hit", "")).lower(), 0.0)
               for t in (run.get("top3") or []))


def load_jsonl(path):
    rows = []
    if Path(path).is_file():
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return rows


def run_order(run):
    try:
        return (0, int(run))
    except (TypeError, ValueError):
        return (1, str(run))


def rel(path):
    try:
        return Path(path).resolve().relative_to(ROOT).as_posix()
    except (ValueError, OSError):
        return Path(path).as_posix()


def main():
    ap = argparse.ArgumentParser(
        description="Stability metric STA (item agreement J-bar, CV-bar, Kendall's W) "
                    "for repeated runs of the same event.")
    ap.add_argument("--out", default=None,
                    help="directory holding scores.jsonl and item_clusters.json "
                         "(default: <repo>/data/repeat_v02)")
    ap.add_argument("--scores", default=None, help="explicit scores.jsonl")
    ap.add_argument("--clusters", default=None,
                    help="explicit item_clusters.json (default: <out>/item_clusters.json)")
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                    help="item merge similarity threshold, documentation only; the "
                         "shipped clusters come from cluster_items.py (default: %(default)s)")
    ap.add_argument("--no-md", action="store_true", help="do not write <out>/sta_summary.md")
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

    rows = [r for r in load_jsonl(scores_path) if r.get("top3")]
    by_ev = defaultdict(list)
    for r in rows:
        by_ev[str(r["id"])].append(r)
    events = sorted([e for e, v in by_ev.items() if len(v) >= 2], key=int)
    if not events:
        raise SystemExit("STA needs at least two runs per event; score more repeats first")

    clusters_path = Path(args.clusters).expanduser() if args.clusters \
        else out_dir / "item_clusters.json"
    if not clusters_path.is_absolute():
        clusters_path = (Path.cwd() / clusters_path).resolve()
    clusters = {}
    if clusters_path.is_file():
        clusters = json.loads(clusters_path.read_text(encoding="utf-8"))
    method = ("LLM semantic merge (cluster_items.py)" if clusters
              else "literal similarity fallback (no item_clusters.json)")

    per = {}
    for eid in events:
        runs = sorted(by_ev[eid], key=lambda x: run_order(x.get("run")))
        items = []  # (run_index, raw, normalised, run label, rank)
        for ri, r in enumerate(runs):
            for t in r.get("top3", []):
                items.append((ri, str(t.get("risk", "")), norm(t.get("risk", "")),
                              str(r.get("run")), t.get("rank")))
        cid = {}
        if eid in clusters:
            mapping = clusters[eid]
            for i, it in enumerate(items):
                cid[i] = mapping.get(f"{it[3]}:{it[4]}", f"x{i}")
        else:
            uf = UF()
            for i in range(len(items)):
                for j in range(i + 1, len(items)):
                    if similar(items[i][2], items[j][2]):
                        uf.union(i, j)
            for i in range(len(items)):
                cid[i] = uf.find(i)
        sets, ranks = [], []
        for ri in range(len(runs)):
            s, rk = set(), {}
            for idx, it in enumerate(items):
                if it[0] != ri:
                    continue
                c = cid[idx]
                s.add(c)
                if c not in rk:
                    rk[c] = len(rk) + 1
            sets.append(s)
            ranks.append(rk)
        js = [jaccard(sets[a], sets[b]) for a in range(len(sets))
              for b in range(a + 1, len(sets))]
        jbar = st.mean(js) if js else 1.0
        n_union = len({c for s in sets for c in s})
        w = kendall_w(ranks, n_union)

        hs = [hit_of(r) for r in runs]
        ews = []
        for r in runs:
            try:
                ews.append(float(r.get("early_warning")))
            except (TypeError, ValueError):
                pass

        def cv(vals):
            if len(vals) < 2:
                return 0.0
            mu = st.mean(vals)
            if mu == 0:
                return 1.0
            return min(1.0, st.pstdev(vals) / mu)

        cv_hr = cv(hs)
        cv_ew = cv(ews) if len(ews) >= 2 else 0.0
        cv_bar = (cv_hr + cv_ew) / 2
        sta = 100 * (0.40 * jbar + 0.30 * (1 - cv_bar) + 0.30 * w)
        per[eid] = dict(n=len(runs), jbar=jbar, d=1 - jbar, w=w, cv_hr=cv_hr, cv_ew=cv_ew,
                        cv_bar=cv_bar, sta=sta, hits=hs,
                        name=runs[0].get("name", ""), n_items=n_union)

    jb = st.mean([per[e]["jbar"] for e in events])
    cvb = st.mean([per[e]["cv_bar"] for e in events])
    wb = st.mean([per[e]["w"] for e in events])
    sta_batch = 100 * (0.40 * jb + 0.30 * (1 - cvb) + 0.30 * wb)
    dispute = [e for e in events if per[e]["d"] >= 0.4]

    def grade(sta):
        return "reproducible" if sta >= 75 else ("mostly reproducible" if sta >= 60
                                                 else "**unstable - read a consensus**")

    lines = [
        "# v0.2 stability report - STA (generated by scripts/sta_stats.py)",
        "",
        f"- Scores input: `{rel(scores_path)}`",
        f"- Item merge: {method}"
        + (f" (`{rel(clusters_path)}`)" if clusters else ""),
        f"- Events: {len(events)}; runs: {sum(per[e]['n'] for e in events)}",
        "- Formula: STA = 100 * [0.40*J-bar + 0.30*(1 - CV-bar) + 0.30*Kendall W], "
        "pass line 60, funding line 75 (internal template section 2.5).",
        "",
        "## Batch STA",
        "",
        "| Metric | Value | Pass line | Funding line | Verdict |",
        "|---|---|---|---|---|",
        f"| **STA** | **{sta_batch:.0f}** | >=60 | >=75 | "
        f"{'pass' if sta_batch >= 60 else '**FAILED - below pass line**'} |",
        f"| J-bar item agreement | {jb:.2f} | >=0.45 | >=0.65 | "
        f"{'pass' if jb >= 0.45 else 'below'} |",
        f"| CV-bar coefficient of variation | {cvb:.2f} | <=0.40 | <=0.25 | "
        f"{'pass' if cvb <= 0.40 else 'above'} |",
        f"| W rank agreement | {wb:.2f} | - | - | - |",
        "",
        "## Per event",
        "",
        "| # | Event | N | J-bar | D | W | CV(HR@3) | STA | Reading |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for e in sorted(events, key=int):
        p = per[e]
        name = str(p["name"])[:20].replace("|", "/")
        lines.append(f"| {e} | {name} | {p['n']} | {p['jbar']:.2f} | {p['d']:.2f} | "
                     f"{p['w']:.2f} | {p['cv_hr']:.2f} | {p['sta']:.0f} | {grade(p['sta'])} |")

    lines += ["", "## Disagreement list (D >= 0.4 -> report consensus + split, never one run)",
              ""]
    if dispute:
        for e in dispute:
            p = per[e]
            drift = ("scores stable, items/order drift" if max(p["hits"]) == min(p["hits"])
                     else "scores drift across runs")
            lines.append(f"- **#{e} {str(p['name'])[:20]}**: D = {p['d']:.2f}, "
                         f"run scores {p['hits']} -> {drift}")
    else:
        lines.append("- none")

    lines += [
        "",
        "## How to read it",
        "",
        "1. High STA = repeated runs of the same event produce the same kind of thing; "
        "the score can be quoted per event.",
        "2. Low STA = run the event several times and deliver the consensus, or upgrade "
        "the model and re-run.",
        "3. We commit to 'a consistent level across repeated runs', never to 'the same "
        "conclusion every time'.",
        "",
        f"> Reproduce: `python scripts/sta_stats.py --out {rel(out_dir)}`",
    ]
    md = "\n".join(lines) + "\n"

    print(md)
    if not args.no_md:
        out_dir.mkdir(parents=True, exist_ok=True)
        md_path = out_dir / "sta_summary.md"
        md_path.write_text(md, encoding="utf-8")
        print(f"[written] {rel(md_path)}")


if __name__ == "__main__":
    main()
