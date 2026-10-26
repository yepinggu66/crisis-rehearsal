# v0.2 results summary — 30 events × 3 runs

Snapshot: 2026-10-26. Raw judge output: `data/repeat_v02/scores.jsonl` (90 records).
Failure notes: `data/failures.md`. Everything below is recomputable from this repository
with `scripts/ci_stats.py` and `scripts/sta_stats.py` and no API key.

## What we did

v0.1 scored each event once and reported 83%. That number had no variance behind it, so we
re-ran **every** event three times — 90 full simulations, each 2 rounds, same seed packs,
same judge prompt, same thresholds — and republished the result. This is a replication and
self-falsification exercise, not a new model.

## Headline numbers

| Metric | v0.2 value |
|---|---|
| Events | 30 publicly documented Chinese corporate crises (2018–2026) |
| Runs | 30 × 3 = **90** (all completed, no failed runs) |
| Top-3 risk hit rate (event mean) | **82.2%** (mean 2.47/3) |
| 95% CI, t-distribution (primary) | **78.5%–85.9%** (±3.7pp, df = 29) |
| 95% CI, 10,000-sample bootstrap | 78.7%–85.6% |
| Paired per-event difference vs v0.1 | **−0.02/3 (±0.18)** — v0.1 reproduced |
| Early-warning quality | 78/100 (75–81) |
| Cost / time per run | ~$0.03 (DeepSeek API) / ~4 minutes |

## What the repeats revealed (the uncomfortable part)

| Metric | v0.2 value | Reading |
|---|---|---|
| Between-event SD | 0.30/3 | difficulty spread across events |
| Within-event SD, mean | **0.26/3** (median 0.24) | re-running the same event moves the score almost as much as the choice of event |
| Events identical in all 3 runs | **5/30 = 17%** | only one event in six reproduces exactly |
| Events with within SD ≥ 0.5 | 2/30 = 7% | #21 (1.5–3.0), #23 (1.0–2.5) |
| Events at a perfect 3/3 in every run | 0/30 | nobody is perfect three times in a row |
| Events at 3/3 at least once | 14/30 = 47% | headroom that only a consensus of repeats can exploit |
| Runs that scored a perfect 3/3 | 21/90 = 23% | descriptive only: runs are correlated |
| Stability STA (item agreement, CV, Kendall's W) | **58** | pass line 60, funding line 75 → **we fail our own bar** |

STA components: J̄ item agreement 0.54, CV̄ 0.08, Kendall W 0.29.

## Weakest events

| # | Event | Mean | Three run scores |
|---|---|---|---|
| 23 | Baidu VP Qu Jing short-video remarks | 1.83/3 | 1.0 / 2.0 / 2.5 |
| 6 | Luckin Coffee accounting fraud | 2.00/3 | 1.5 / 2.0 / 2.5 |
| 8 | Brilliance Auto bond default | 2.00/3 | 2.0 / 2.0 / 2.0 |
| 14 | Meituan "choose one of two" antitrust penalty | 2.00/3 | 1.5 / 2.0 / 2.5 |

`data/failures.md` documents what went wrong in each case, in the judge's own words.

## Scoring discipline (do not quote the headline without these)

1. 82.2% is an **event-mean graded score** (0 / 0.5 / 1 … 3 per event), not a binary
   hit/miss rate. The binary framing on 30 events is roughly ±17pp. The two must not be
   mixed.
2. The 90 runs are **not** 90 independent samples. The statistical unit is 30 events;
   repeats exist to estimate run-to-run noise.
3. The interval covers sampling and run randomness only. It does **not** include
   LLM-judge error and does not include systematic bias from a 2-round simulation.
4. Because only 17% of events are fully stable, we commit to "a consistent level across
   repeated runs", never to "the same conclusion every time". High-variance events must be
   run several times and read as a consensus.
5. This is a rehearsal / backtest producing **directional evidence** — not a forecast, not
   a probability, not "we know what happens next".

## Recompute it

```bash
python scripts/ci_stats.py  --out data/repeat_v02   # 82.2%, CI, variance, 17%
python scripts/sta_stats.py --out data/repeat_v02   # STA 58
```

To regenerate the whole grid from scratch (needs MiroFish running plus an LLM key):
`python scripts/repeat_runs.py --runs 3 --rounds 2 --out output_v2`, then
`python scripts/score_repeat.py --out output_v2`.
