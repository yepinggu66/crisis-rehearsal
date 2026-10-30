# Roadmap

> **What this is:** direction, not a commitment. There are no dates, no promised features, and
> no promised numbers. The evidence pack is versioned separately from the code: v0.3.0 does not
> change a single published statistic. If a milestone would change a number, it says so here
> before it happens.

## Where we are: v0.3.0 (current)

Shipped:

- A standard-library CLI — `crh` (alias `crisis-rehearsal`) with `verify`, `stats`, `report`,
  `demo`, `pack init`, `pack validate`, `site`.
- `data/evidence.sha256` + `crh verify`: the evidence pack can be checked, and an edit fails
  loudly (exit 1).
- Self-contained HTML rehearsal dossiers for the four shipped report events (1, 6, 25, 28);
  other events get an intelligence pack + real outcome + three-run scores — never an invented
  report body.
- Scenario-pack schema and validator (sector: enterprise / government / finance).
- Enterprise and government evaluation documents: architecture, deployment, security,
  compliance mapping, procurement pack, government design note.
- CI matrix (Python 3.9–3.12), tests, container/offline demo.

Unchanged and still true:

- 82.2% event-mean Top-3 hit rate, 95% CI 78.5–85.9 (bootstrap 78.7–85.6), 30 events × 3 runs.
- STA 58 against a pass line of 60 — **we still fail our own stability bar**.
- The judge is an LLM and is **not human-calibrated**.
- The event corpus is Chinese, 2018–2026, 30 events.

## v0.4 — make the evidence harder to dismiss

### Human calibration of the judge (highest priority)

- Run the calibration batch already specified in `data/judge_calibration.md`: 5 reports, blind
  human re-judging, 15 slots, pass line **≥ 80% slot agreement**.
- Record every disagreement with its class (`too_lenient` / `too_strict` / `magnitude`) in the
  shipped log.
- If the batch fails, relabel the headline everywhere as "LLM-judged, human calibration failed"
  and revise the rubric before any promotion. That is the plan we committed to; it is not
  optional.

### More runs where the numbers are weak

- Re-run the two unstable events (#21, #23) and the lowest-scoring events (#6, #8, #14) with
  more repeats to estimate their variance better.
- Publish the run-to-run consensus rule as a documented delivery procedure, not just advice.

### English event library (small, honest)

- Start with ~10 well-sourced English-language public crises; the goal is to test whether the
  method transfers, not to claim it does.
- Label it a **pilot corpus** until it has been through the same 3-run protocol and the same
  limitations apply.
- Do not quote a combined hit rate across languages unless the judge and rubric are shown to be
  comparable.

### Sector packs (templates first)

- `finance` and `government` scenario-pack templates with regulatory triggers, escalation
  ladders and KPIs, written by practitioners where possible.
- Status: **template / design**, not backtested. No hit rate is claimed for a pack until it has
  its own runs and outcome labels.

## v1.0 — a benchmark that can be cited without an asterisk

The v1.0 bar is deliberately hard; if it takes longer, it takes longer.

- **100+ events** in the library, with a documented sampling and inclusion rule.
- **Human-calibrated judge** with a published agreement rate and a stable rubric.
- **Multi-language** corpus (Chinese + English at minimum) with language-specific judge
  calibration.
- **More than 2 simulation rounds** evaluated against cost; ablation studies (no-graph,
  no-persona, human-analyst baseline) so the 82.2% figure can be read as "better than what",
  not just "a number".
- **Reproducibility budget:** every headline number recomputable from the repository with no
  API key, as today.
- **Deployment readiness, not certification:** a documented 等保/ISO/SOC 2 gap-closure plan a
  customer can execute, an SBOM, dependency scanning, and an audit-log/RBAC implementation in
  the enterprise packaging. Certifications are not promised — they require a certification body.

## Explicitly not planned

These are not "backlog"; they are things we will not claim or build as the project stands:

- A crisis **prediction** product or an "accuracy" guarantee. The method produces directional
  evidence; the stability number is published precisely because precision is not there yet.
- **Real-time monitoring / early-warning** feed ingestion. That is a different product.
- **Classified-network** support. No 涉密 qualification; see `docs/government.md`.
- **Certification or测评 timelines.** We are not a certification body and will not put a date on
  someone else's audit.
- **Named customer logos, government references or endorsements.** None are published and none
  may be inferred.
- **信创/国密 certification** claims. The adaptation work is roadmap and currently unverified.
- **A hosted SaaS** of the simulation engine. The open tool is single-operator and file-based by
  design; a multi-tenant service would need RBAC/audit/tenancy that do not exist in v0.3.

## How priorities are chosen

1. Anything that protects the credibility of a published number (calibration, stability, data
   integrity) before anything that adds a feature.
2. Anything that lets a buyer verify the product on their own hardware without trust.
3. Anything that broadens the corpus honestly (new events with sources) before marketing.
4. Enterprise packaging (RBAC, audit, SSO) when there is a pilot that needs it — not
   speculatively.

## Proposing a change

Open an issue with the change, the evidence, and the cost (who maintains it). Structural
changes follow the RFC process in [`GOVERNANCE.md`](GOVERNANCE.md) §3. If you want to work on a
roadmap item, say so in the issue first so two people do not build the same thing.
