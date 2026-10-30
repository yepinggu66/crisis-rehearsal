# Procurement answer pack

> **模板与示例，不是报价、不是合同、不是承诺。** This document is an evaluation template:
> it lists what can be delivered, how acceptance can be measured, what an SLA could look like,
> and the questions a procurement team will ask. Amounts are marked **示例 / placeholder** and
> are not an offer. Any engagement is defined by a signed contract after scoping.

## 1. What is free, and what is commercial

| Item | Open source (AGPL-3.0) | Commercial engagement |
|---|---|---|
| `crh` CLI, evidence pack, scoring protocol, scenario-pack schema | ✅ free to install and use, including internally in a company or government body | — |
| Re-runnable numbers (`crh verify`, `crh stats`, `crh demo`) | ✅ | — |
| Rehearsal dossier generation for the four shipped events | ✅ | — |
| Custom T-72h packs, rehearsals, workshops, readouts | — | ✅ |
| Sector tuning (ontology / persona rules), facilitated tabletop | — | ✅ |
| Private-deployment support, air-gap installation help | — | ✅ (best-effort today; formal SLA is roadmap) |
| Enterprise packaging: SSO, RBAC, audit log, installer | **roadmap** | roadmap — not sold as shipped |

AGPL note for procurement: **internal use inside your organisation does not trigger source
publication.** If you modify the engine and offer it as a network service to third parties, the
AGPL requires you to publish your modifications. The rehearsal outputs belong to you; the
licence covers the software, not your documents.

## 2. Deliverables and acceptance criteria

Define acceptance **before** the pilot. Suggested measurable criteria:

| # | Deliverable | Acceptance criterion (verifiable) |
|---|---|---|
| 1 | Offline evidence workstation | `pipx install git+https://github.com/yepinggu66/crisis-rehearsal` (or `pip install -e .`), then `crh --version` prints `crh 0.3.0` |
| 2 | Evidence integrity | `crh verify` exits **0**; editing any covered file makes it exit **1** (demonstrate once with a scratch copy) |
| 3 | Published numbers | `crh stats` prints 82.2%, 95% CI 78.5–85.9, within-event SD 0.26/3, 5/30 identical, STA 58 (failed, pass line 60) |
| 4 | Dossier generation | `crh demo --out demo` produces 4 self-contained HTML dossiers + an index; opening one works with the network disconnected |
| 5 | No hidden egress | Run `crh verify/stats/demo` with egress blocked and DNS disabled; all pass |
| 6 | Scenario pack | `crh pack validate <path>` accepts a customer-authored pack; a pack with a missing required field is rejected |
| 7 | Documented limits | Buyer can find the honest-limitations statements (judge not human-calibrated, 17% stability, small corpus) without asking |
| 8 | Rehearsal readout (commercial) | One past public event rehearsed; Top-3 risk sheet, three-run consensus, decisions with owners; limitations page included |
| 9 | Workshop (commercial) | 90–120 min session, decision log with owners and dates, written debrief |

Do not accept "the vendor says the number is 82.2%" as acceptance. The buy-side can reproduce it
in under a minute; that is the point of the shipped evidence pack.

## 3. Delivery cycle (example schedule)

| Week | Activity | Buyer involvement |
|---|---|---|
| 0 | Kick-off, scope, data-classification rules, NDA/DPA | Security, legal, business owner |
| 1 | Offline install; acceptance items 1–5 on buyer hardware | IT / platform team |
| 2–3 | Author 1–3 T-72h packs; clean-room review; choose model endpoint | Business owner + legal |
| 3–4 | 3–5 runs per scenario; dossier generation | Analyst |
| 4 | Tabletop workshop and readout | Crisis team, CRO/PR |
| 5 | Decide: integrate, extend, or stop | Sponsor |

This is a **suggested** schedule. It assumes one business owner and roughly one day per week of
buyer time; it does not assume access to classified material.

## 4. SLA template (建议，需合同化)

The open-source software is provided **as-is** under AGPL, without SLA. A paid support agreement
would set the terms below — the numbers are **examples**, not commitments. There is no 24×7
support commitment today.

| Severity | Definition (example) | First response | Workaround target | Fix target |
|---|---|---|---|---|
| P1 | Dossier generation impossible / published numbers not reproducible / security issue with a known exploit | 1 business day | 3 business days | 10 business days |
| P2 | A CLI subcommand fails for a supported case | 2 business days | 10 business days | next release |
| P3 | Documentation error, cosmetic defect | 5 business days | — | next release |
| P4 | Feature request, roadmap question | 10 business days | — | evaluated in roadmap review |

Also agree: support channel (email/ticket), covered versions (current minor + previous minor),
security-fix handling (see `SECURITY.md`), and the buyer's responsibility for the model
endpoint, OS, network and backups.

## 5. Price structure example (示例，非报价)

Prices are agreed per engagement after scoping; the structure below is what a proposal would
look like, with **placeholder amounts**. Treat the numbers as illustrative units, not 2026
prices.

| Line item | Basis | Placeholder unit (示例) |
|---|---|---|
| Pilot / proof of concept (2 weeks, 1–2 events, workshop) | fixed fee | `CNY ___ / EUR ___` per pilot |
| Rehearsal of one additional scenario | per event, 3–5 runs | `CNY ___` per event |
| Tabletop workshop facilitation | per half-day session | `CNY ___` per session |
| Sector tuning (persona/ontology for one industry) | time & materials | `CNY ___` per industry track |
| Private deployment support / air-gap install | days | `CNY ___` per engineer-day |
| Annual support agreement (SLA above) | annual | `CNY ___ / year` |
| Training (analyst + reviewer) | per cohort | `CNY ___` per cohort |
| Custom feature / enterprise packaging | roadmap, quoted separately | not offered in v0.3 |

What is deliberately **not** in this table: a per-seat licence, a "certification" fee, or a
charge for the open-source code. Both are wrong for this project and we will not put them in a
proposal.

## 6. POC plan (2 weeks, offline)

| Phase | Days | Content | Exit criterion |
|---|---|---|---|
| Setup | 1–2 | Install on buyer hardware, egress blocked; `crh verify/stats/demo` | Acceptance items 1–5 pass |
| Calibration | 3–4 | Rehearse one **past public event** whose outcome is known; compare to the shipped dossier | Buyer can explain why the score is what it is, including a failure |
| Own scenario | 5–7 | Author 1–2 customer packs (T-72h); clean-room review; choose model (local preferred) | Packs validate; model choice documented with its data-egress consequence |
| Runs | 8–9 | 3–5 runs per scenario; consensus reading; stability note | Dossier + consensus; disagreement across runs documented, not hidden |
| Tabletop | 10 | 90–120 min facilitated session; decision log | At least one decision changes, or the buyer documents why not |
| Readout | 10 | Written readout vs. the acceptance criteria agreed in week 0 | Go / no-go decision |

POC rules: no client data in the public repo; buyer data stays in buyer storage; delete the
POC copies at the end and record the deletion; if a cloud model is used, name it in the POC
records as a subprocessor.

## 7. Data-processing agreement (DPA) — key points

The open project does not publish a standard DPA template. A customer-specific agreement should
cover at least:

1. **Roles** — customer is controller of its scenario packs and dossiers; vendor is processor
   for data it handles during an engagement; for the public corpus the project is the
   publisher, not a processor of customer data.
2. **Scope and purpose** — rehearsal only; no secondary use; no model training on customer data.
3. **Data minimisation** — packs contain only what the exercise needs; avoid personal data;
   prefer public or synthetic company data for the pilot.
4. **Subprocessors** — if the engagement uses a cloud LLM API, name the provider, its location
   and retention terms in the DPA; local models avoid this line item.
5. **Retention and deletion** — the vendor deletes working copies at the end; the buyer keeps
   dossiers; the vendor certifies deletion on request.
6. **Security measures** — encrypted transfer and storage, least-privilege access, MFA on
   vendor accounts, incident notification.
7. **Cross-border transfer** — explicitly addressed if a cloud model is used; "no transfer" is
   the default configuration.
8. **Audit and cooperation** — buyer may ask for the evidence is reproducible on its own
   hardware; vendor provides the `crh verify` outputs.
9. **Liability and termination** — standard contract terms; on termination, data deletion and
   handover of deliverables.

This is a checklist, not legal advice; have counsel draft the agreement.

## 8. Fifteen questions a procurement team will ask

1. **Is the product certified (ISO 27001 / SOC 2 / 等保)?** No. There is a requirement mapping
   with gaps (`compliance.md`); no certification, no assessment.
2. **Can it make our system pass 等保 2.0 三级?** No single component can. It supports an
   offline, hash-verified, no-egress component design; identity, audit and management remain
   buyer-side or roadmap.
3. **Does our data leave our network?** Not for `verify/stats/report/demo` or a local-model
   deployment. A cloud LLM API is an explicit egress path chosen by configuration.
4. **How accurate is it?** 82.2% is an **event-mean graded Top-3 hit rate** on 30 Chinese
   public events, 3 runs each (95% CI 78.5–85.9). It is directional evidence, not a forecast,
   and only 17% of events reproduce identically across runs.
5. **Can it predict our next crisis?** No, and we will not sell it that way. It rehearses
   escalation paths and decisions before they are needed.
6. **What languages are supported?** Chinese event corpus and judge prompt; English
   documentation (plus Chinese README). An English corpus is roadmap.
7. **Which model do we need?** DeepSeek API reproduces the published grid (~$0.03/run, ~4 min,
   measured); Ollama/vLLM keep data in-perimeter but are not benchmarked against the grid.
8. **Can it run fully air-gapped?** The evidence workstation: yes. The full rehearsal: yes with
   a local model and offline installs, with the caveats in `deployment.md` §4.
9. **What does AGPL mean for us?** Internal use is fine. If you modify and serve the software
   to third parties over a network, publish your modifications. Your documents are yours.
10. **Do you offer source escrow?** No. The code is open; escrow adds nothing.
11. **What support do we get?** Community issues by default, as-is; a paid SLA is available by
    agreement (template above). No 24×7 today.
12. **Do you have customer references?** No named customer references are published in this
    repository, and none may be implied. Any reference requires the customer's written consent.
13. **How does it integrate with our systems?** File-based: self-contained HTML dossiers and
    JSON scenario packs. No server API, no live feed ingestion, no connector marketplace.
14. **How often is it updated, and are versions pinned?** Tagged releases; the evidence pack and
    upstream engine commit are pinned so a version cannot silently change a number.
15. **Can we modify it and remove the limitations section?** AGPL lets you modify the software;
    removing honest limitations from a dossier would misrepresent the method. We ask that
    derivative work keep the limitations page — and if you need a different arrangement, talk to
    the maintainers first.

## 9. Buyer's due-diligence checklist

- [ ] Reproduce 82.2% / CI / STA 58 on your own hardware (`crh stats`).
- [ ] Run `crh verify` and confirm the failure mode (scratch copy).
- [ ] Read `data/failures.md` and the limitations in `README.md`.
- [ ] Confirm whether a cloud model is acceptable, or budget for a local one.
- [ ] Check `compliance.md` gap list against your own framework obligations.
- [ ] Agree the classification of every pack before it is written.
- [ ] Agree acceptance criteria before the POC starts.
- [ ] Have counsel draft the DPA; name every subprocessor.
- [ ] Agree deletion and retention in writing.

## 10. Contact

Open an issue or email **yepinggu@outlook.com**. We will answer a questionnaire honestly,
including the rows where the answer is "not covered".

## Related documents

- [Enterprise overview](overview.md) — roles, scenarios, deliverables, open-core boundary, pilot.
- [Security design notes](security.md) — threat model and gaps.
- [Compliance mapping](compliance.md) — the document to attach to a questionnaire.
- [Deployment guide](../deployment.md) — sizing, model options, air-gap.
- [Government edition](../government.md) — the public-sector answer pack.
