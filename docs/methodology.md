# Methodology: how we backtest a crisis rehearsal

> This document is the part most "AI prediction" projects skip. We publish it so you can check our numbers instead of trusting them.

## 1. The information clean room

For every event we write a **T-72h information pack** (`data/seeds/{id}.md`) that contains **only** what a careful analyst could have known 72 hours before the crisis became public:

- the entity and its recent public disclosures;
- the trigger (a recall notice, a complaint cluster, a policy draft, a public conflict);
- early signals (small-scale social discussion, prior incidents, regulatory signals);
- three scenario hypotheses (silence / apology / confrontation).

**Rules (enforced in review):**
1. No post-outcome facts, penalties, or stock reactions.
2. No information published after T0 (we check the source dates).
3. When in doubt, omit — we would rather under-supply the engine than leak the future.

## 2. What the engine does

MiroFish (upstream) runs the swarm simulation. We contribute:
- a **local knowledge graph adapter** (`patches/zep_local.py`) so the pipeline runs with no cloud graph database;
- the **seed authoring protocol** above;
- a **deterministic config fast-path** for reproducible local runs.

Per event: ontology → graph (~12 nodes) → 7–12 personas → 2 rounds on simulated Twitter/Reddit → an ~8,000-character rehearsal report.

## 3. How we define a "hit"

We do **not** ask the model to output probabilities. Instead, a judge (an LLM, with human spot checks) compares the report against the ground-truth outcome in `data/events.csv`:

| Code | Definition | What counts |
|---|---|---|
| **H1 — Risk-type hit** | Does a top-3 risk in the report correspond to a risk that actually materialised? | `yes` = same type and same mechanism; `partial` = same type, different mechanism; `no` = absent |
| **H2 — Timing** | Does the report's escalation window overlap the real escalation (within ±6h)? | `yes` / `partial` / `no` |
| **H3 — Path** | Does the report's propagation path share the real key nodes? | LCS-based score |

The headline metric is **top-3 H1 hit rate**: `mean(1·yes + 0.5·partial) / 3`.

**Negative samples.** Three events are labelled *low predictability* (sudden attack, sudden accident). If the engine claims to predict them, that counts as a false positive. A method that only reports successes is not a method.

## 4. Judge protocol

- The judge receives: the event metadata, the ground-truth outcome, and the report (truncated to 7k chars).
- It must return JSON: `top3[{rank,risk,hit(yes/partial/no),why}]`, `path_hit`, `early_warning(0-100)`, `comment`.
- The judge is told **not** to reward writing quality, only correspondence to what happened.
- We manually spot-check ≥5 reports per batch and record disagreements in `data/judge_calibration.md`.

## 5. Known limitations (do not quote the headline number without these)

1. **Stochastic engine**: one run per event. Re-running changes the report. The number is directional.
2. **Small sample**: 30 events ⇒ ≈±17pp at 95% confidence. A 100+ event benchmark is required before claiming a stable rate.
3. **LLM judge**: correlated with the generator model. Human calibration is ongoing.
4. **Chinese-market events only** in v0.1. An English event library is the next milestone.
5. **2-round simulation** is a cost compromise; more rounds may improve path fidelity.

## 6. Reproduce a batch

```bash
python scripts/backtest_runner.py --ids 25,7,11,12,28 --rounds 2
python scripts/score.py 25,7,11,12,28
```

Outputs: `output/{id}/report.md` + `output/scores.jsonl` + a summary table.
