# Enterprise overview

> **Who this document is for:** a buyer's evaluation team — CRO/PR/IR, CISO/CIO, legal and
> compliance, board secretary, risk management — deciding whether a crisis rehearsal is worth
> a pilot.
>
> **What it is not:** a claim of deployed enterprise customers, certifications or proven
> production scale. The open-source evidence is public and recomputable; the commercial
> offering is reports and workshops around it. No named client deployments are published in
> this repository, and we do not invent references.

## 1. The problem it addresses

Reputation crises are decided in the first 24 hours, and most organisations only own
**monitoring** — a system that tells them a crisis exists after it has started. The rehearsal
happens before: take a real or realistic crisis, rewind 72 hours, give a simulation engine only
what was public then, and force the response team to see its own escalation paths on paper
before the board asks.

The published evidence behind the method is small and honest: 30 public Chinese corporate
crises (2018–2026), each rehearsed three times, Top-3 risk hit rate **82.2%** (event-mean
graded score, 95% CI 78.5–85.9), stability **STA 58** against our own pass line of 60. It is
directional evidence, not a forecast. See `README.md` and `data/repeat_v02/` for the full
protocol and the failures.

## 2. Who gets what

| Role | Question they bring | What a rehearsal gives them | What it does not replace |
|---|---|---|---|
| **CRO / Head of Risk** | "What are we not seeing before the board meeting?" | A ranked Top-3 risk sheet with escalation paths and a decision log, produced from a T-72h information pack | Risk register ownership; legal advice; a response playbook already tested by humans |
| **PR / IR / Corporate Comms** | "Will our first statement make it worse?" | Three scenario branches (silence / apology / confrontation) exercised against simulated journalists, investors, regulators, competitors | Media monitoring, spokesperson training, live social listening |
| **CISO / CIO** | "Can this run inside our perimeter, with audit and no data egress?" | Offline evidence workstation; private model gateway; file-based outputs; hash-verified evidence; documented gaps | A certified product — it is not certified (see `compliance.md`) |
| **Legal / Compliance** | "Are we rehearsing with data we are allowed to process?" | Public-only corpus; customer scenarios stay customer-owned; DPA points documented | Legal opinion; data-protection impact assessment done for you |
| **Board secretary / General counsel** | "Can the output go into the board pack?" | Self-contained HTML dossier: event, assumptions, Top-3, evidence hashes, limitations page | A signed audit opinion; it is a rehearsal artefact, clearly labelled as such |
| **Emergency / crisis management office** (public sector) | "Can we tabletop a real scenario without a live feed?" | Offline rehearsal + workshop structure + packaged scenario JSON | Operational command systems; see `docs/government.md` |

## 3. Scenarios that fit the method

| Situation | What the rehearsal produces | What it costs you |
|---|---|---|
| Product safety / recall / food safety | Top-3 risks, likely escalation to regulators, first-statement branches, supplier-blame trap | one T-72h pack + 3–5 runs + workshop |
| Executive misconduct / viral remarks | Persona reaction, internal-resolution vs counter-attack branches (our published failure mode is exactly the wrong counter-attack prior — useful to surface) | same |
| Data breach / regulatory action | Regulator / media / customer reaction paths; disclosure timing questions | same |
| Layoffs, labour disputes, plant closure | Employee, local-government and media escalation paths | same |
| Antitrust / policy exposure | Policy-chain reading, competitor and investor responses | same |
| Cross-border brand spillover | Domestic ↔ overseas opinion interaction in one simulated feed | same |
| Short-seller / accounting allegation | Investor and journalist escalation, disclosure discipline | same |
| Bond default / liquidity event | Creditor, rating-agency and regulatory paths | same |

If the scenario depends on live classified intelligence, a rehearsal is the wrong tool. If the
scenario is "what will the first 72 hours look like and what do we decide in them", it fits.

## 4. What an engagement looks like

1. **Scope one event.** Either a past public event (best for calibration: you know the outcome)
   or one customer scenario written as a T-72h pack (`crh pack init`).
2. **Clean-room the pack.** Only pre-T0 facts; every claim gets a source; review signs it off.
   This is the step that most improves quality, and the one that most vendors skip.
3. **Run 3–5 times, read the consensus.** The published within-event SD is 0.26/3 and only
   17% of events score identically across three runs. A single run is noise; we sell the
   consensus, not the best draw.
4. **Generate the dossier.** Self-contained HTML: event file, T-72h pack, simulation config,
   Top-3 vs real outcome, three-run scores and stability reading, evidence hashes, limitations.
5. **Run the tabletop.** 90–120 minutes with the people who would actually be in the room;
   decisions are logged with owners and deadlines.
6. **Debrief against the rubric.** What the rehearsal caught, what it missed, what changes in
   the playbook. The failures file (`data/failures.md`) sets the expectation: we publish our
   misses, so the debrief can be honest.

## 5. Deliverables

| Deliverable | Format | Notes |
|---|---|---|
| Evidence workstation reproduction | `crh verify`, `crh stats`, `crh demo` output | Buyer runs it on their own hardware; no API key |
| Rehearsal dossier per event | Single self-contained HTML (inline CSS, no external assets) | Archivable, attachable, printable; timestamped evidence hash |
| Scenario pack | JSON, schema-validated (`crh pack validate`) | Customer-owned; reusable for the next exercise |
| Tabletop workshop | 90–120 min facilitated session + decision log | Usually the part that changes behaviour |
| Written readout | 1–2 page memo: Top-3, consensus, disagreements, limitations | Correctly labelled "rehearsal, not forecast" |
| Pilot acceptance report | Measured against the criteria agreed before the pilot | See `docs/enterprise/procurement.md` |

## 6. Open core: what is open, what is commercial

| | Open source (AGPL-3.0) | Commercial engagement |
|---|---|---|
| CLI + evidence pack + scoring protocol | ✅ in this repo | — |
| Seed-authoring protocol and clean-room rules | ✅ documented | — |
| Scenario-pack schema and validator | ✅ in this repo | — |
| Rehearsal reports and workshops | — | ✅ sold as a service |
| Sector ontology / persona rules tuned per industry | — | commercial |
| Customer packs and client corpora | customer-owned, never in this repo | handled under DPA |
| Enterprise packaging: SSO, RBAC, audit log, air-gap installer, support SLA | **roadmap** (see `ROADMAP.md`) | roadmap — not sold as shipped today |

The code is not crippled: `crh verify/stats/report/demo` is the same code the buyer runs. The
commercial value is the work around the engine — packs, workshops, tuning, support — which is
also why AGPL is workable: if you modify and serve the engine, publish your modifications.

## 7. Pilot path: 30 / 60 / 90 days

| Window | Goal | Activities | Exit criterion |
|---|---|---|---|
| **Days 1–30** | Trust the numbers | Install offline workstation; run `crh verify/stats/demo`; re-run one past public event against its known outcome; review the limitations and failures docs with CISO/legal | Buyer reproduces 82.2% / CI / STA 58 on their own hardware and accepts the wording discipline |
| **Days 31–60** | Trust the method on your scenarios | 2–3 customer scenarios authored as T-72h packs; 3–5 runs each with the chosen model; two tabletop workshops; decision logs | At least one scenario produces a Top-3 that the response team had not already written down, and the decision log changes an action |
| **Days 61–90** | Integrate | Add rehearsal to the crisis playbook; schedule the annual board rehearsal; decide on support/enterprise packaging; agree data-classification rules for packs | Playbook updated; owner and calendar named; go/no-go on commercial support |

## 8. How to evaluate us (a buyer's checklist)

- **Demand the numbers, then recompute them.** `crh stats` on your machine; the CI must match
  `data/repeat_v02/ci_summary.md` and `sta_summary.md`. If a document quotes a number that is
  not in `data/`, treat it as a red flag.
- **Check the evidence integrity claim.** `crh verify` must pass; ask what happens if a file is
  edited (answer: exit 1).
- **Read the limitations before the marketing.** `README.md` §Honest limitations,
  `data/failures.md`, `data/judge_calibration.md` (status: **not run**), and the STA failure.
- **Ask what is not certified.** The answer is in `docs/enterprise/compliance.md`: no 等保
  assessment, no ISO/SOC 2 certification, no government case.
- **Insist on the clean-room audit.** Pick one seed pack and ask for the public source of every
  claim; the review rules are in `docs/methodology.md` §1.
- **Run it on your own infrastructure.** The demo is offline by design; a vendor that cannot
  show you an offline run on your laptop has not built the thing this repo describes.
- **Ask what breaks.** Model change, language change, live-feed expectation, classified data,
  multi-tenancy — each has a documented "no" somewhere in these docs.

## 9. Honest status (read before the pilot)

- **No named customers in this repository.** The commercial offer (reports, workshops) exists;
  no logos, references or endorsements are published here, and none may be inferred. Any future
  reference would require the customer's written consent.
- **No certifications or assessments.** Compliance documents are requirement mappings with
  gaps, explicitly labelled as design notes.
- **Chinese-market corpus.** 30 events, 2018–2026; an English corpus is roadmap. Don't assume
  the number transfers to another market.
- **Stability is not solved.** 17% of events reproduce identically across three runs; the
  method commits to a consensus of repeats, never to "the same conclusion every time".
- **The judge is an LLM and is not human-calibrated yet** (`data/judge_calibration.md`). The
  published interval excludes judge error.
- **Local models are unbenchmarked** on the grid. If you deploy Ollama/vLLM, you get a
  rehearsal, but not necessarily the published rate — re-score and treat it as your baseline.

## 10. Contact

Open an issue on GitHub or email **yepinggu@outlook.com**. A reasonable first conversation is
30 minutes: one real past event, your classification rules, and the decision you are trying to
de-risk. We will tell you if the method does not fit.

## Related documents

- [Security design notes](security.md) — STRIDE, data flow, no-egress default, audit/RBAC design.
- [Compliance mapping and gaps](compliance.md) — 等保 / DSL / PIPL / GDPR / ISO 27001 / SOC 2.
- [Procurement answer pack](procurement.md) — acceptance criteria, SLA, POC, DPA, 15 FAQs.
- [Deployment guide](../deployment.md) — offline workstation, private cloud, air-gap.
- [Government edition](../government.md) — 政务场景、分级分类、信创 roadmap.
- [Roadmap](../../ROADMAP.md) — what is planned, what is explicitly not promised.
