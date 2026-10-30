# Changelog

All notable changes to this repository are documented here. The evidence pack in
`data/` is the source of truth for every published number; a release that changes
code without changing `data/` must not change the numbers (`crh verify` enforces
byte-level integrity, `crh stats` recomputes them).

## v0.3.0 — 2026-10-31 — Enterprise & public-sector readiness

The headline numbers do **not** change in this release: 82.2% top-3 risk hit rate
(event-mean graded score, 95% CI 78.5–85.9, 30 events × 3 runs), STA 58 (below our
own pass line of 60). v0.3.0 is about making the same evidence executable,
inspectable and procurable — not about a better score.

### Added — a 60-second, offline entry point

- **Installable CLI** (`pip install -e .`; entry points `crh` and `crisis-rehearsal`),
  Python ≥ 3.9, **zero runtime dependencies**, standard library only. Wheel and sdist
  both build; the wheel installs in a clean, network-isolated venv.
- `crh verify` — checks every evidence file against `data/evidence.sha256` (43 files),
  exits 1 on any modification or missing file.
- `crh stats` — recomputes the published numbers by importing the shipped
  `scripts/ci_stats.py` and `scripts/sta_stats.py`, then cross-checks them against the
  values quoted in the README (`published_match=True`).
- `crh demo` — one command, offline, no API key, ~0.2 s: verify → stats → four
  self-contained HTML dossiers (events 1, 6, 25, 28) + an index page.
- `crh report --event ID` — a single self-contained HTML dossier: event file, T−72h
  information pack, simulation configuration, Top-3 risks vs the documented outcome,
  three-run scores with the stability read, sha256 provenance and the honest-limits
  block. For the 26 events without a shipped report the dossier explicitly says no
  report body is published — it never fabricates one.
- `crh pack init` / `crh pack validate` + `schema/scenario_pack.schema.json` — the
  portable scenario-pack contract (timeline, stakeholders, regulatory triggers,
  escalation ladder, KPIs, decision log, evidence, provenance) with a
  standard-library validator, so a sector scenario is machine-checkable.
- `crh site` — a static index of all 30 events as dossiers.
- `Makefile`, `Dockerfile` (non-root, read-only compose service) and
  `docker-compose.yml` for an offline evidence workstation. The container is **not**
  the full MiroFish engine and is documented as such.
- 90 tests covering number reproduction, evidence tamper detection, dossier content
  rules, schema validation and CLI exit codes. The GitHub Actions matrix (Python
  3.9–3.12, Windows smoke, sdist/wheel build that installs the wheel in a clean venv
  and re-runs `crh demo`) is defined in [`docs/ci/github-actions.yml`](docs/ci/github-actions.yml);
  it is not enabled yet — pushing a workflow file needs a credential with the
  `workflow` scope, which the release token does not have. Every job runs only
  commands that work offline and are listed in `docs/cli.md`.

### Added — enterprise & public-sector documentation

- `docs/architecture.md` (components, data contracts, deployment topologies, extension
  points, upstream relationship), `docs/deployment.md` (offline workstation, private
  cloud, air-gap; DeepSeek API / Ollama / vLLM; sizing and cost transparency).
- `docs/enterprise/overview.md`, `docs/enterprise/security.md` (STRIDE, default
  no-egress, audit-log/RBAC design), `docs/enterprise/compliance.md` (requirement
  **mapping with gaps** for 等保 2.0 三级, 数据安全法, 个保法, GDPR, ISO 27001, SOC 2 —
  explicitly not a certification or assessment), `docs/enterprise/procurement.md`
  (acceptance criteria, SLA template, price-structure example, POC, DPA points, FAQs).
- `docs/government.md` — public-sector scenarios, classification and isolation levels,
  file-based integration with monitoring/command systems, pilot process, 信创/国密
  roadmap. Clearly labelled a design note: no procurement case, no assessment, no
  classified deployment.
- `docs/cli.md` — command reference with real output, exit codes and data provenance.

### Added — open-source governance and launch material

- `SECURITY.md`, `CONTRIBUTING.md` (including the T−72h clean-room and
  evidence-immutability rules), `CODE_OF_CONDUCT.md`, `GOVERNANCE.md`, `ROADMAP.md`,
  `CITATION.cff`, `docs/README.md` (documentation index).
- `launch_kit/` — distribution plan and channel copy (including a star/benchmark
  research note built from GitHub API snapshots), repository settings, demo script,
  enterprise/government outreach templates.
- GitHub issue forms (bug / feature / government pilot) and a pull-request template.

### Changed

- `README.md` rewritten around a 30-second quick start; `README-ZH.md` added.
- `.gitignore` extended for build output, demo output and caches (existing lines
  untouched); `requirements.txt` comments clarified (the CLI needs nothing; `httpx`
  is only for the v0.1 runner scripts).
- `data/evidence.sha256` added (no evidence file was modified — verified by
  `crh verify`).
- `.gitattributes` now stores and checks out **every text file as LF** (`data/**`
  explicitly), so the evidence manifest and the sha256 printed in generated
  dossiers are identical on Windows, Linux and GitHub source tarballs. The v0.2
  record `scores.jsonl = 562be6853fba6906` came from a CRLF Windows checkout; the
  canonical value is `0bfd42d4be1f16db` and `data/evidence.sha256` carries it.
  No evidence blob changed — only the checkout conversion did (`docs/cli.md` §3).

### Not done / known gaps

- The Docker image was written but not built in this environment (no Docker daemon);
  build it with `docker build -t crisis-rehearsal:0.3.0 .`.
- GitHub Actions is **not enabled yet**: the workflow definition ships in
  `docs/ci/github-actions.yml` and needs a credential with the `workflow` scope (or a
  copy-paste through the GitHub web UI) before it can live in `.github/workflows/`.
  The same commands pass locally and are documented in `docs/cli.md`.
- The judge is still **not human-calibrated**, only 5/30 events are score-stable, there
  is no human-analyst control condition, and 26/30 events ship no report body. See
  README → *Honest limitations*.
- No certification, no assessment, no government procurement case, no 信创/国密
  verification. These are stated as gaps, not roadmap promises.

## v0.2.2 — 2026-10-27 (documented in the README; no separate git tag)

- Seed hygiene sweep: removed 91 unfilled placeholders, moved the outcome-derived
  predictability label out of the seeds, truncated post-T0 clauses; shipped the
  Luckin Coffee (event #6) raw rehearsal report; disclosed that the v0.1 agent
  interviews returned no records (0/19).

## v0.2.0 — 2026-10-26

- Replication pack: 30 events × 3 runs (90 runs), identical rubric; event-mean hit
  rate 82.2% (95% CI 78.5–85.9; bootstrap 78.7–85.6); within-event SD 0.26/3; 5/30
  events score-identical; stability STA 58 (pass line 60 → failed, published anyway);
  paired difference vs v0.1 −0.02/3 (±0.18); five verified upstream patches.

## v0.1.0 — 2026-10-25

- First public benchmark: 30 events, one run each, 82.8% top-3 hit rate; fixed LLM
  judge protocol; local Zep adapter.
