# Contributing

Thanks for wanting to improve Crisis Rehearsal. This project's whole credibility rests on one
thing: **the numbers in the README can be checked**. Contributions are welcome if they keep that
property intact.

## Ways to contribute

- **Reproduce and report.** Run `crh verify`, `crh stats`, `crh demo` on your machine; open an
  issue if a number does not match `data/repeat_v02/`.
- **Find a post-T0 leak in a seed pack.** This is high-value: see §3.
- **Add a public event** to the event library with a proper T-72h pack (§3).
- **Report a failure case** you think the corpus is missing — negative samples are kept on
  purpose.
- **Code**: CLI, report generator, scenario-pack validator, tests, packaging (§4).
- **Docs**: corrections, clearer wording, translations. Marketing language is not an
  improvement; accuracy is (§5).

## 1. Development setup

```bash
git clone https://github.com/yepinggu66/crisis-rehearsal
cd crisis-rehearsal
python -m pip install -e .
python -m pytest -q            # after the v0.3 test suite lands
crh verify
crh stats
crh demo --out /tmp/crh-demo
```

Requirements: Python ≥ 3.9. The runtime must stay **standard library only** for the `crh` CLI;
`httpx` is an optional extra (`[llm]`) used only by the upstream-pipeline scripts.

Windows: set `$env:PYTHONIOENCODING='utf-8'` so the Chinese event names print correctly.
The patch files in `patches/` are LF-only and must stay that way (`.gitattributes` enforces
this) — never let an editor rewrite their line endings.

## 2. Ground rules for the evidence pack

`data/` is the citation base. The following are not negotiable:

1. **Evidence files are immutable.** Never edit `data/repeat_v02/scores.jsonl`,
   `scores_v01.jsonl`, `item_clusters.json`, or `data/events.csv`'s published rows to make a
   number "better". If a file must change (e.g. a factual correction with a source), it needs:
   a) a documented reason in the PR, b) a regenerated `data/evidence.sha256`, c) re-running the
   stats and updating every document that quotes the number. This is a maintainer-level change,
   not a casual PR.
2. **No post-T0 information in `data/seeds/`.** The T-72h clean-room rule is in
   `docs/methodology.md` §1: no outcomes, penalties, stock reactions, or anything published
   after T0. When in doubt, omit. A leaked future fact invalidates the backtest, not just the
   seed.
3. **Every claim needs a source.** `events.csv` rows carry `source_url`; a seed pack cites the
   public sources it used. "I remember this happened" is not a source.
4. **Do not fabricate or anonymise events into generic ones.** Real public events, real sources.
5. **Negative samples stay.** Low-predictability events are in the corpus and count against the
   score; removing them would be fraud.

## 3. Data contribution workflow

### Adding a public event

1. Pick a publicly documented corporate crisis with a clear trigger and a documented outcome
   (penalty, delisting, resignation, settlement) and public sources.
2. Add a row to `data/events.csv` using the existing columns:
   `id,event_name_en,event_name_zh,entity,year,date,crisis_type,trigger,outcome,penalty,source_url,predictability`.
   Use the next free id; keep the Chinese and English names consistent with the sources.
3. Author `data/seeds/{id}.md` — the T-72h pack. Follow the structure in
   `docs/methodology.md` §1 (entity/disclosures, trigger, early signals, three hypotheses,
   provenance) and state the sources used.
4. Ask a second reviewer to check the seed **against the T0 timestamp**: every clause must be
   defensible as pre-T0 knowledge. Record the review in the PR description.
5. Do not re-run the whole grid in a PR; maintainers schedule grid runs. A new event is merged
   as an addition and the README stays explicit until the grid is re-run.

### Reporting a seed leak

Open an issue titled `seed leak: event <id>` with the clause and the source that proves it is
post-T0. If confirmed, maintainers truncate the clause, bump the seed-hygiene version note, and
record the change. Do not open a PR that quietly deletes text — an audit trail matters.

## 4. Code contributions

- **Runtime:** stdlib only for `crisis_rehearsal/`; Python ≥ 3.9; no new required dependency
  without prior discussion in an issue.
- **Compatibility:** Windows and Linux both matter (the maintainer develops on Windows; the
  CI workflow in `docs/ci/github-actions.yml` covers both once enabled). PowerShell should be
  able to run every documented command.
- **Tests:** every CLI behaviour change needs a test. The statistics tests assert the published
  numbers against `data/repeat_v02`; do not weaken them to make a change pass.
- **The CLI contract is fixed** for v0.3: command names `crh` / `crisis_rehearsal` /
  `crisis-rehearsal`, subcommands `verify / stats / report / demo / pack / site`. Renaming is a
  breaking change and needs a version bump and a migration note.
- **Report generator:** the HTML dossier must remain a **single self-contained file** — no
  external stylesheets, fonts, images or JS; no network fetch at open time. Untrusted pack text
  must be escaped. Add a test for both properties.
- **`crh stats` must never invent a metric.** It reproduces: 82.2%, t-CI 78.5–85.9, bootstrap
  78.7–85.6, within-event SD 0.26/3, 5/30 identical, STA 58 (failed, pass line 60).
- Style: readable over clever; type hints where they help; no silent `except: pass`; error
  messages should tell the operator what file/flag is wrong.

## 5. Documentation contributions

- **Numbers carry their source file.** Every quoted figure should be traceable to `data/`.
  Example: "82.2% event-mean Top-3 hit rate (`data/repeat_v02/ci_summary.md`)".
- **Keep the wording discipline.** 82.2% is an event-mean **graded** score over 30 events, not a
  binary hit rate, not a probability, not a forecast. Do not "round up" in prose.
- **Do not add marketing claims.** No "revolutionary", "world's first", "100%", "guaranteed",
  "AGI". If a sentence would not survive a CISO reading it alongside `data/failures.md`, it does
  not go in.
- **Certifications:** never write that the project is certified/assessed. Compliance statements
  are mappings with gaps (`docs/enterprise/compliance.md`).
- **Customer/gov claims:** no invented customers, references, logos, government endorsements or
  procurement claims.
- **Links:** use relative links inside the repository; check they resolve. Keep commands
  copy-pasteable and consistent with `docs/cli.md`.
- Chinese docs use UTF-8. A Chinese version should read naturally (not a literal translation)
  and use 「危机预演」 consistently.

## 6. Pull request process

1. Open an issue first for anything non-trivial (new command, schema change, data change).
2. Fork, branch, keep the change focused. One concern per PR.
3. Run `python -m pytest -q` (when present) and `crh verify` locally; paste the relevant output
   in the PR.
4. Fill the PR template: what changed, why, which numbers are affected, how it was verified.
5. By submitting, you agree your contribution is licensed under **AGPL-3.0** (the project
   licence). No CLA is required. A `Signed-off-by` line (DCO) is welcome but not mandatory.
6. Maintainers review for correctness and for the red lines above. A PR that improves the
   product but inflates a claim will be sent back, not merged.

## 7. Review checklist (maintainers)

- [ ] Numbers in the diff match `data/`; no document quotes a figure without a source.
- [ ] `crh verify` passes; no evidence file changed without a manifest regeneration and a stats
      re-run.
- [ ] Seeds pass the clean-room review (pre-T0 only).
- [ ] Tests cover the new behaviour; the statistics assertions are untouched.
- [ ] HTML output is self-contained and escapes untrusted text.
- [ ] No new runtime dependency; Python 3.9 compatibility.
- [ ] Docs do not overclaim (certification, customers, accuracy, government cases).
- [ ] CLI names match the v0.3 contract.

## 8. What will be rejected

- Fabricated events, sources, outcomes or judge records.
- Post-T0 information presented as a T-72h signal.
- Editing published scores or seeds to improve the headline.
- Removing or weakening the honest-limitations text.
- Marketing language that changes the meaning of a metric.
- Claims of certification, government adoption, or named customers without evidence.
- A "fix" that makes `crh stats` stop matching `data/repeat_v02/`.

## 9. Good first contributions

- Improve a seed pack's sourcing or readability **without** adding post-T0 facts.
- Add a test for a CLI edge case (missing file, bad `--event`, unwritable output dir).
- Fix a broken link or a command that does not run on Windows PowerShell.
- Translate a document into Chinese/English while keeping the numbers and wording discipline.

## 10. Questions

Open an issue, or email **yepinggu@outlook.com**. Behaviour expectations are in
[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md); security reports follow [`SECURITY.md`](SECURITY.md).
