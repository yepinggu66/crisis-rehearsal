<!--
Thanks for the PR. This repository ships an evidence pack, so two things are held to a
higher standard than a normal code repo:
  1) files under data/** are evidence — they are appended to with sources, never "fixed" to make a test pass;
  2) every published number (82.2%, CI 78.5–85.9, STA 58) must stay recomputable.
-->

## Summary

<!-- What does this PR change, and why? Link the issue: Closes #... -->

## Type of change

- [ ] Bug fix (no change to published numbers)
- [ ] Documentation / links / examples
- [ ] New scenario / new event (appends to `data/**`, with sources and a T-72h clean-room check)
- [ ] CLI or report feature (changes `crh`)
- [ ] Statistics or methodology (affects published numbers — link the methodology issue)
- [ ] Build / CI / packaging

## Verification (paste real output, not screenshots)

```text
$ crh verify
$ crh stats
$ crh demo
$ pytest -q
```

- [ ] `crh verify` passes (or: this PR is *intentionally* adding evidence files and the manifest is left for the maintainer to regenerate)
- [ ] `crh stats` still prints 82.2% / 78.5–85.9 / STA 58 (or the PR explicitly changes methodology and says so)
- [ ] `pytest -q` passes locally
- [ ] New/changed HTML reports have no external CSS/JS/font references (self-contained)

## Evidence-pack rules (check if you touched `data/**` or `data/seeds/**`)

- [ ] I did **not** edit existing rows/files to make a test pass; changes are additive.
- [ ] Every new claim has a live public source URL (trigger, outcome, penalty).
- [ ] Seeds contain only information public in the 72 hours before T0 — no post-T0 outcomes, no `待核` placeholders, no `可预测性` label.
- [ ] I did **not** regenerate `data/evidence.sha256` (the maintainer does that on merge, so the diff is reviewable).
- [ ] If this adds an event, a pipeline run + judge score is recorded in the same format as the existing grid.

## Honesty checklist

- [ ] No customer/government names, certifications, or accuracy claims were added.
- [ ] Numbers are stated with their denominator and method (event-mean graded score, n=30 events × 3 repeats; not a binary hit rate, not a forecast).
- [ ] Limitations were not weakened. If this PR changes a limitation, explain why.

## Notes for reviewers

<!-- Anything risky, deferred, or needing a maintainer decision. -->
