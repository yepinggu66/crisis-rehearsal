# Crisis Rehearsal Engine — rehearse the crisis before it happens

> ▶ **Watch the 2:42 demo:** https://youtu.be/pj7PKonS2Ns
> 🧵 **Launch thread on X:** https://x.com/PingguYe/status/2115103453110468641

**TL;DR** — We take a real reputation crisis, rewind to 72 hours before it broke, and give a swarm-simulation engine (MiroFish) only the public information available at that moment. 7–12 persona agents — journalists, retail investors, regulators, short sellers, competitors — react for 2 rounds on a simulated social feed, and an 8k-character rehearsal report comes out. An LLM judge then scores the report's top-3 risks against what actually happened.

In v0.2 we re-ran all 30 events **three times each — 90 runs, identical scoring rubric**.

**Top-3 risk hit rate: 82.2%** (95% CI 78.5–85.9; n=30 events × 3 runs).

The uncomfortable part is published too: **only 17% of events scored identically across all three runs**, and our internal stability score is **STA 58** — under our own pass line of 60.

Event library, T-72h seeds, local graph adapter, scoring protocol and failure file are open (AGPL-3.0). **We sell rehearsal reports and workshops, not software.**

**Check the numbers yourself in two commands, no API key required:**

```bash
git clone https://github.com/yepinggu66/crisis-rehearsal && cd crisis-rehearsal
python scripts/ci_stats.py     # -> 82.2%, 95% CI 78.5-85.9%, within-event SD 0.26, 5/30 identical
python scripts/sta_stats.py    # -> stability STA 58 (our pass line is 60, so: failed)
```

Those two scripts read the shipped evidence pack in `data/repeat_v02/` (90 judge records) and are standard-library only.

---

## Why

A reputation crisis is irreversible once it starts: the first 24 hours get written into public memory, and most companies only buy **monitoring** — after the fact. The budget that already exists sits on the response side. We sell the rehearsal that happens *before* the crisis.

## What we built

1. **Pre-crisis information pack** — only what was publicly available 72 hours before the event. No hindsight.
2. **Local knowledge graph** — MiroFish's Zep Cloud dependency replaced with a local JSON graph adapter (1 file, ~400 lines). The pipeline runs with zero cloud graph service.
3. **Swarm simulation** — 7–12 persona agents per event on a simulated Twitter/Reddit, 2 rounds, driven by DeepSeek or any OpenAI-compatible model.
4. **Native report generation** — MiroFish's ReportAgent produces an ~8k-character structured rehearsal report per event.
5. **Scoring** — an LLM judge compares the report's top-3 risks with the real outcome (the event library carries ground truth), and returns top-3 hits plus an early-warning quality score.

## Backtest results (v0.2, 30 events × 3 runs)

| Metric | v0.2 value |
|---|---|
| Events | 30 publicly documented Chinese corporate crises (2018–2026) |
| Runs | 30 events × 3 runs = **90** (all completed, no failures) |
| **Top-3 risk hit rate** (event mean) | **82.2%** (mean 2.47/3) |
| 95% CI, t-distribution (primary) | **78.5% – 85.9%** (±3.7pp) |
| 95% CI, 10,000-sample bootstrap | 78.7% – 85.6% |
| Paired per-event diff vs v0.1 | **−0.02/3 (±0.18)** — v0.1 reproduced |
| Between-event SD (difficulty spread) | 0.30/3 |
| Within-event SD (same event, re-run) | **0.26/3** (median 0.24) |
| Events identical across all 3 runs | **5/30 = 17%** |
| Events with SD ≥ 0.5 | 2/30 = 7% (#21, #23) |
| Events at a perfect 3/3 in all three runs | 0/30 |
| Events at a perfect 3/3 at least once | 14/30 = 47% |
| Runs scoring a perfect 3/3 | 21/90 = 23% |
| Early-warning quality | 78/100 (range 75–81) |
| **Stability STA** (internal template §2.5) | **58** — pass line 60, funding line 75 → **failed** |
| Cost / time per event | ~$0.03 (DeepSeek API) / ~4 minutes |

Full table, per-event scores and the stability breakdown: `data/repeat_v02/v02_summary.md`.
The judge's raw records for all 90 runs: `data/repeat_v02/scores.jsonl`.
The cases we lost: `data/failures.md`.

## What changed in v0.2 (we re-ran everything 3×)

- **Every event re-run three times.** 30 events × 3 runs = 90 full simulations, 2 rounds each, same seeds, same judge prompt, same thresholds. v0.1 was one run per event.
- **Variance and interval estimation added.** Event-mean hit rate with a t-distribution CI (primary) and a 10,000-sample bootstrap CI, reported side by side. Between-event and within-event SD are now separate numbers instead of one blended claim.
- **Replication check, published.** The per-event paired difference against v0.1 is −0.02/3 (±0.18). The old single-run result reproduced. That is the least interesting sentence in this README and the one we most wanted to be able to write.
- **Our own stability score is disclosed, including the failure.** STA 58 against a pass line of 60: J̄ item agreement 0.54, CV 0.08, Kendall W 0.29. We publish it because a metric you only show when it passes is marketing.
- **Honest wording upgraded.** v0.1 said "83%". The defensible statement is "Top-3 risk hit rate 82.2%, event-mean graded score, n=30 events × 3 runs" — a graded 0–3 score averaged across events, not a binary hit/miss rate, and not a probability about the future.
- **New scripts.** `repeat_runs.py`, `score_repeat.py`, `cluster_items.py`, `ci_stats.py`, `sta_stats.py` alongside `backtest_runner.py` and `score.py`. The v0.2 statistics scripts use the standard library only.

### Seed hygiene (v0.2.2)

Every file in data/seeds/ is restricted to what was publicly available in the 72 hours **before** T0.
As of v0.2.2 the packs were swept for artifacts that violated that rule:

- removed 91 待核 placeholders (unfilled authoring slots);
- moved the outcome-derived 可预测性 rating out of the seeds — it lives only in data/events.csv (predictability column);
- truncated 首发平台 chains at the point where they started describing post-T0 outcomes (e.g. a disclosure date, an app takedown, a regulator penalty).

If you spot a remaining post-T0 clause, open an issue. The seeds are meant to be auditable, not to look complete.

## Reproducibility & stability

This is the section most benchmark write-ups skip, so here is ours.

**How stable are the results?**
- Only **5 of 30 events (17%)** produced identical scores on all three runs. Run the same event twice and you can get a meaningfully different report.
- Within-event SD is **0.26/3** (median 0.24), against a between-event SD of 0.30/3. Roughly speaking, the randomness from re-running is nearly as large as the differences between easy and hard events.
- Two events are outright unstable (SD ≥ 0.5/3, 7%): the canteen food-safety visual case (#21) and the executive self-video case (#23), scoring 1.5–3.0 and 1.0–2.5 across their three runs.
- We would rather report this than hide it: **a single-run score on a single event is noise.** Our delivery rule is 3–5 repeated runs per event and read the consensus, not the best draw.

**Two kinds of stability, measured separately.** A score can be stable while the reasoning under it moves. Event #8 scored exactly 2.0/3 in all three runs, yet its top-3 items and their order drifted (disagreement D = 0.60), which is why we compute STA (item agreement, CV, Kendall's W), not just SD.

**Scoring discipline (please hold us to it)**
1. 82.2% is an **event-mean graded score** (0/0.5/1 … 3 per event), not a binary hit/miss rate. The binary framing on 30 events is roughly ±17pp. Do not mix the two.
2. 90 runs are **not** 90 independent samples. The statistical unit is 30 events; repeats exist to estimate run-to-run noise.
3. The interval covers sampling and run randomness only. It does **not** include LLM-judge error, and it does not include systematic bias from a 2-round simulation.
4. Because only 17% of events are fully stable, we commit to "a consistent level across repeated runs", never to "the same conclusion every time". High-variance events must be run multiple times and read as a consensus.
5. This is a rehearsal / backtest producing **directional evidence** — not a forecast, not a probability, not "we know what happens next".

**What we do not ship.** The judge's scores for all 90 runs are in this repo, but the 90 generated reports (~8.4k characters / ~23 KB each) are not. You can recompute every published statistic; you cannot independently re-judge the reports from this repo alone. Four full samples are shipped — `docs/reports/{1,28}.md` and `data/reports/{6,25}.md`. The judge prompt is fixed, Chinese and unchanged since v0.1 (`scripts/score_repeat.py`), so the two batches stay comparable.

## Honest limitations

- **The judge is an LLM.** Same model family, fixed prompt, fixed thresholds — reproducible, but **not human-calibrated**: no human spot-check has been run yet (planned for v0.2.2; status and template in `data/judge_calibration.md`). It is not part of the 82.2% figure, and the 95% CI excludes judge error by construction.
- **The judge grades risk type, not consequence severity.** A rehearsal that names the right risk at the wrong scale can still score 2.5/3. We think this is a bigger limitation than the 17% stability number, and it is visible in `data/failures.md` (#6, #8).
- **The dominant error is a false escalation.** In the five worst events, 5 of the 6 zero-scoring Top-3 slots were "legal pressure / blame the supplier" branches that never happened. It is a systematic false-positive mode, documented honestly rather than smoothed over.
- **30 events is small.** Binary framing gives roughly ±17pp at 95%. The corpus is Chinese-market, 2018–2026. Generalization is unproven.
- **There is no control condition in this release.** No human-analyst baseline, no ablation, no dumb baseline. The 82.2% describes the pipeline against a fixed rubric; it is not a claim that the pipeline beats an analyst.
- **2 rounds of simulation is a simplification** of real opinion dynamics. It is enough to produce escalation paths and the right questions; it is not a model of society.
- **Agent interviews came back empty in the v0.1 grid.** Every v0.1 report carries the engine's own caveat — "agent interview interface returned no valid records (0/19 interviews)". The top-3 ranking therefore rests on the knowledge-graph relations and propagation paths, **not** on first-person testimony from the simulated agents. `data/reports/6.md` is a verbatim example: the caveat appears in all four chapters. The interview step has not been re-run on v0.2 output.
- **Negative samples are included.** Events where the engine should not have claimed an edge are in the corpus and they count against the score.
- **Failures are in the repo** (`data/failures.md`), with post-mortem notes. We do not hide misses.

## Reproduce it

Two levels. The first needs nothing but Python; the second needs a running MiroFish and an LLM key.

### A. Verify the published numbers (no API key, no simulation)

The v0.2 evidence pack is shipped: 90 judge records, the v0.1 baseline, the item merge.

```bash
python scripts/ci_stats.py  --out data/repeat_v02   # 82.2%, CI 78.5-85.9, variance, 17%
python scripts/sta_stats.py --out data/repeat_v02   # stability STA 58
```

With no flags both scripts default to `data/repeat_v02`. They print the sha256 prefix of the
scores file they read, so a silent edit to the data shows up in the output. Each script has a
full flag set under `--help`.

### B. Regenerate the whole grid (MiroFish + LLM key)

```bash
# 0) MiroFish (upstream, AGPL-3.0) + local graph adapter, no Zep Cloud
git clone https://github.com/666ghj/MiroFish && cd MiroFish
git checkout 7657031ac01184afe2cb220f5ee3545573b5e843   # the commit our patches are pinned to
git apply ../patches/000*.patch                        # 5 verified patches, see docs/patches.md
npm run setup:all && cp .env.example .env
cd .. && export LLM_API_KEY=sk-... LLM_BASE_URL=https://api.deepseek.com LLM_MODEL_NAME=deepseek-chat ZEP_LOCAL=1
#    (or put the same four keys in a .env at the repo root; env vars win, .env is the fallback)

# 1) one event, end to end (2 simulation rounds) -- the v0.1 single-run runner
pip install -r requirements.txt      # httpx, only needed for this line
python scripts/backtest_runner.py --ids 21 --rounds 2

# 2) the v0.2 grid: every event, three times
python scripts/repeat_runs.py --runs 3 --rounds 2 --out output_v2

# 3) score each run with the same judge prompt and thresholds as v0.1
python scripts/score_repeat.py --out output_v2

# 4) merge Top-3 items by meaning (needed for STA; the shipped merge is a file you can inspect)
python scripts/cluster_items.py --out output_v2

# 5) event-mean hit rate + 95% CI (t and 10k bootstrap) + variance, then stability
python scripts/ci_stats.py --out output_v2
python scripts/sta_stats.py --out output_v2
```

The full grid is 90 runs × ~4 minutes — roughly six hours of wall-clock on one machine — plus a few dollars of API credit. `repeat_runs.py` is resumable (existing reports are skipped) and `--ids` shards the grid across processes. `-h` on each script prints the full flag set.

## Repository layout

```
data/events.csv              # 30 public crisis events with sources + outcomes
data/seeds/{id}.md           # pre-crisis (T-72h) information packs used as simulation seeds
data/repeat_v02/             # v0.2 evidence: 90 judge records, v0.1 baseline, item merge, summaries
data/failures.md             # events where we missed -- with post-mortem notes
data/judge_calibration.md    # human calibration of the judge: status + template (not yet run; see docs/methodology.md §4)
data/reports/{6,25}.md       # single-report samples from the v0.1 grid: Luckin Coffee, livestream mooncakes
patches/000*.patch           # 5 patches against upstream commit 7657031: local Zep adapter + 4 hooks (see docs/patches.md)
scripts/backtest_runner.py   # v0.1 headless pipeline: graph -> simulation -> report (one run per event)
scripts/score.py             # v0.1 LLM judge with fixed protocol
scripts/make_seeds.py        # draft T-72h packs from data/events.csv (drafts only -- data/seeds/ is the frozen official set)
scripts/repeat_runs.py       # v0.2: N repeated runs per event, resumable output layout
scripts/score_repeat.py      # v0.2: score every repeat, same rubric as v0.1
scripts/cluster_items.py     # v0.2: merge the same risk item across runs (for STA)
scripts/ci_stats.py          # v0.2: event-mean hit rate, t-CI, bootstrap CI, variance
scripts/sta_stats.py         # v0.2: stability (STA), item agreement, CV, Kendall W
docs/methodology.md          # hit definitions, information-clean-room rules, scoring protocol
docs/patches.md              # the 6 changes needed for upstream MiroFish
docs/reports/{1,28}.md       # generated rehearsal reports, full length (~8.4k characters each)
requirements.txt             # httpx for the v0.1 runner scripts; v0.2 statistics scripts are stdlib-only
```

## License & commercial boundary

- **Code**: AGPL-3.0, same as upstream MiroFish. Run it, modify it, offer it as a service — but if you modify and serve it, publish your source.
- **What we keep closed**: industry ontology (agent persona rules), client corpora, delivery playbooks. We sell **rehearsal reports and workshops**, not the engine.
- **No client data in this repo.** All events are public news; seeds were written by us from public sources only.

## Who it is for

- **PR / IR agencies** that want a white-label rehearsal engine instead of an enterprise suite.
- **Listed companies and funds** that face reputation risk and want to rehearse before it lands.
- **Cross-border brands** (Chinese brands going global): we rehearse two-way spillover between domestic and overseas opinion.

## Contact

Open an issue, or email **yepinggu@outlook.com**. We will run a free 30-minute rehearsal of one real past event for your team. Chinese site: https://pingguye.cn

Maintainer: [@PingguYe](https://x.com/PingguYe).

---

*Built on [MiroFish](https://github.com/666ghj/MiroFish) (AGPL-3.0) and [OASIS](https://github.com/camel-ai/oasis) (Apache-2.0). Thanks to both teams.*
