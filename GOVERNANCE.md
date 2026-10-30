# Governance

Crisis Rehearsal is a small open-source project. This document says who decides what, how
releases and evidence changes happen, and how the commercial boundary is kept honest.

## 1. Principles

1. **Evidence outranks opinion.** A decision that changes a published number, a seed pack or the
   scoring protocol is judged by whether it keeps the numbers reproducible.
2. **Honesty is a feature.** Limitations, failures and gaps are part of the product. A change
   that hides one is rejected regardless of who proposes it.
3. **Open core, no crippleware.** The code in this repository is the code buyers run. Commercial
   value comes from packs, workshops, tuning and support — not from withholding the engine.
4. **Small project, explicit bus factor.** One maintainer today. We say so rather than pretending
   to be a foundation.

## 2. Roles

| Role | Who | Can do |
|---|---|---|
| **Maintainer** | `yepinggu66` (PingguYe) | Merge to `main`, cut releases, maintain the evidence pack, approve evidence changes, represent the project |
| **Committers** | Contributors granted review rights over an area (docs/CLI/data) | Review and approve PRs in their area; cannot cut a release alone |
| **Contributors** | Anyone with a merged PR | Propose changes, add events/seeds through review, report failures and leaks |
| **Users** | Anyone | Open issues, reproduce numbers, ask for corrections |

There is no foundation, no board, and no formal membership. Roles are granted by the maintainer
based on sustained, high-quality contribution, and can be revoked for violations of the Code of
Conduct or the red lines in `CONTRIBUTING.md`.

## 3. Decision process

- **Lazy consensus.** For ordinary changes: open an issue or PR, describe the change and the
  evidence, and if no maintainer objects within **7 days**, it can merge when review passes.
- **RFC for structural changes.** Changes to the CLI contract, the scoring rubric, the
  evidence-pack schema, the data model, or the licence need a written proposal (issue labelled
  `rfc`) and an explicit maintainer approval, not lazy consensus.
- **Evidence changes are maintainer-level.** Editing `data/repeat_v02/*`, `data/events.csv`
  published rows, or the seed clean-room rules requires: a documented reason, a regenerated
  `data/evidence.sha256`, a stats re-run, and an update to every document that quotes the
  number. These are never merged as drive-by PRs.
- **Numbers must survive the diff.** A PR that changes a number must show the before/after and
  the command output that produces it.
- **Disagreement.** Argue with evidence in the issue. If consensus fails, the maintainer decides
  and writes the reasoning in the issue; a decision can be revisited with new evidence.

## 4. Releases

- **Semantic versioning** for the CLI and package: `major.minor.patch`. v0.3.0 adds the
  installable CLI and dossiers; patch releases fix bugs and docs without changing published
  numbers.
- **Evidence versioning is separate.** The v0.2 evidence pack (`data/repeat_v02/`) stays as
  published. A new backtest batch gets a new directory and a new version note; it never silently
  overwrites old records.
- **Release checklist:** tests green and CI matrix passes → `crh verify`/`stats`/`demo` run and
  pasted into the release PR → docs and links checked → CHANGELOG entry (maintainer) → tag →
  release notes state what did **not** change (evidence, numbers).
- **No release may claim certification, customer adoption, government endorsement, or a metric
  that is not in `data/`.**

## 5. Commercial boundary

The maintainer may sell rehearsal reports, workshops, sector tuning and support. To keep that
from corrupting the public project:

1. **No client data in the repository.** Public events only; customer packs are customer-owned.
2. **No client-tuned ontology in the open corpus.** Sector tuning stays commercial; the open
   scoring protocol and corpus stay comparable.
3. **Commercial work cannot change the public numbers.** A client engagement may re-score its
   own scenarios, but it cannot rewrite `data/repeat_v02/`.
4. **Disclose conflicts.** If a commercial engagement is relevant to a decision, say so in the
   issue.
5. **Open code stays runnable.** Feature work paid for by a client lands in the open core when
   it is generally useful, unless it exposes client data or sector-confidential tuning.

## 6. Funding and sustainability

There is no foundation, grant, or sponsor today. GitHub Sponsors/FUNDING, if enabled, is
managed by the maintainer and does not buy influence over published results. If funding grows
to the point of paid maintainers, this document will be updated before the first hire, and the
evidence-custody rules will not change.

## 7. Becoming a maintainer

Sustained contribution over time — reviewed data/seed work, code with tests, honest docs — plus
agreement with the principles above. Ask in an issue, or the maintainer will ask you. There is
no exam and no fee.

## 8. Changing this document

Governance changes follow the RFC process and require maintainer approval. They are never part
of an unrelated PR.

## 9. Contact

Open an issue for project matters, or email **yepinggu@outlook.com** for anything that should
not be public.
