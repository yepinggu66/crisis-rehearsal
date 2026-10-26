# Failures and post-mortems

A method that only reports its successes is not a method. This file documents the events
where the v0.2 rehearsal grid scored worst, using the judge's own recorded justifications
from `data/repeat_v02/scores.jsonl` — no narrative added afterwards, no case invented.

**How to read the scores.** Each run's Top-3 risks are graded `yes` = 1, `partial` = 0.5,
`no` = 0, so a single run scores 0–3 and an event's score is the mean of its three runs.
Event-level scores and their spread are reproducible with `python scripts/ci_stats.py
--out data/repeat_v02`. Quotes below are translated from the Chinese `why` / `comment`
fields; the originals live in `scores.jsonl`.

The five events below are the four lowest-scoring events of the corpus plus the two
highest-variance ones (#21, #23). Together they account for 6 of the 45 scored Top-3 slots —
and **5 of those 6 zero-scoring slots are the same mistake**: the report predicted an
escalation branch (legal action against the source, blaming a supplier) that never happened.
In all 15 runs the *core* risk was still detected; every point lost came from slots 2–3.

---

## #23 Baidu VP Qu Jing short-video remarks — 1.83/3 (lowest in the corpus)

- Runs: **1.0 / 2.0 / 2.5**, SD 0.62 (joint most volatile event)
- Real outcome: she resigned (2024-05-09); Baidu's image damaged, HK shares fell, reported
  market-value loss ~HKD 6.0bn; the real resolution was *internal* (resignation + management
  reassurance), not a counter-attack.
- What the judge accepted: run 1 correctly identified the cold-blooded remarks and the
  spillover from the individual to Baidu's values (`yes`, "与真实引爆点完全对应").
- **Failure mode — fabricated escalation.** Two of run 1's three slots predicted "blaming a
  supplier" and "legal pressure on the source"; the judge scored both `no` because neither
  happened. Run 2 lost its third slot to the same package. The engine also missed the
  actual ending: the report rehearsed an "apology + recall" path, not resignation.
- **What we admit.** Our simulation's prior for a corporate misstep includes a stock
  "counter-attack → second crisis" branch. When that branch does not fire, the report has
  already spent two of its three slots on it and the real outcome never enters the Top-3.
  This is a systematic false-positive mode, not bad luck: it is why the same failure
  appears in three of the five events below.

## #6 Luckin Coffee financial fraud — 2.00/3

- Runs: **1.5 / 2.0 / 2.5**, SD 0.41
- Real outcome: Nasdaq delisting, ~RMB 61m penalty from SAMR, USD 180m SEC penalty.
- What the judge accepted: the core allegation (inflated sales and ad spend from the
  Muddy Waters short report) is found in all three runs.
- **Failure mode — slot padding and magnitude blindness.** Run 1 spent slots 2–3 on
  related-party transactions (`partial`) and insider selling (`no`); run 3 padded with the
  same derivative themes. Ranking also flipped: run 2 put "the anonymous report circulating
  early" first (`partial`) and the actual allegation second (`yes`). Nothing in the report
  anticipated the *magnitude* — delisting plus two jurisdictions of penalties.
- **What we admit.** Top-3 is a scarce resource and we fill it with plausible derivatives of
  the trigger instead of stopping at three. Worse, our rubric scores risk *type*, not
  consequence severity, so a rehearsal that names the right risk at the wrong scale still
  scores 2.5/3. That is a limitation of the metric we chose, and we would rather say it
  than hide it.

## #8 Brilliance Group bond default — 2.00/3

- Runs: **2.0 / 2.0 / 2.0**, SD 0.00 — identical scores, yet disagreement D = 0.60
- Real outcome: RMB 1.0bn principal and interest on "17 Huaqi 05" unpaid; bankruptcy
  restructuring; CSRC investigation and RMB 53.6m fine; former chairman arrested.
- What the judge accepted: the default itself was caught in all three runs ("风险点三……
  未能按期兑付本息10亿元").
- **Failure mode — a stable score hiding moving content.** All three runs scored exactly
  2.0, but the *items and their order* drifted: bank-loan-recall rumours, rating downgrades and
  the payment failure swapped places across runs (D = 0.60). The rating downgrade and the
  loan-recall rumour were never the legally decisive risk, and the report never reached the
  escalation that actually happened: regulatory investigation, criminal liability,
  restructuring.
- **What we admit.** Reporting only SD would have made this event look perfectly stable.
  That is exactly why we also publish STA and the disagreement list: a score can be stable
  while the reasoning underneath it is not.

## #14 Meituan exclusive-dealing antitrust penalty — 2.00/3

- Runs: **2.5 / 2.0 / 1.5**, SD 0.41
- Real outcome: RMB 3.442bn fine, RMB 1.289bn of merchant deposits returned; investigation
  opened 2021-04-26.
- What the judge accepted: the policy-chain framing (this penalty read as "antitrust is now
  routine") was a `yes` in **all three** runs.
- **Failure mode — branch selection swings the score by a full point.** Run 1 scored 2.5;
  run 3 scored 1.5 because one slot went to "platform ecosystem backlash — blaming suppliers
  and legal pressure on the source" (`no`, it never happened) and another to a "focus drift"
  risk the judge could only call `partial`. The report also never quantified the merchant
  deposit refund, which is the part the public actually reacted to.
- **What we admit.** Here the variance is *entirely* in slots 2–3: the core judgement is
  stable, the tail is a coin flip between real derivative risks and invented branches. For
  delivery this means: never sell a single run of an event like this; read the consensus.

## #21 Jiangxi vocational college "rat head vs duck neck" — 2.33/3, but 1.5 in run 1

- Runs: **1.5 / 3.0 / 2.5**, SD 0.62 (joint most volatile event)
- Real outcome: the "duck neck" initial finding was overturned, rat head confirmed by a
  provincial investigation team; the caterer was fined ~RMB 7.06m and lost its licence; the
  college's responsible officials were disciplined.
- What the judge accepted: run 2 is a perfect 3/3 — the botched initial classification, the
  historical complaint record, and the Douyin-first propagation structure were all correct;
  run 3 scored 2.5.
- **Failure mode — one fabricated branch costs 1.5 points.** Run 1 predicted "legal pressure
  on the whistleblower" (`no`) and only a `partial` on the complaint history, turning a
  correct main line into 1.5/3. Its own comment still reads "精准预判了……主线".
- **What we admit.** When the engine gets its three slots right this event is a 3/3, and
  when it pads with the counter-attack branch it is a 1.5/3. Nothing about the event
  became harder between runs — the difference is the branch prior. That is the clearest
  evidence we have that a single-run score on a single event is noise, and it is why our
  delivery rule is 3–5 repeats read as a consensus.

---

## What this file means for anyone quoting our numbers

1. The core risk is usually found; the tail of the Top-3 is where we lose points.
2. The dominant error is a **false escalation** (legal/pressure/supplier-blame branches),
   which the judge scores `no`. It is systematic, so the 82.2% is not inflated by lucky
   padding — if anything it is depressed by it.
3. Score stability and content stability are different things (#8). We publish both SD and
   STA/agreement for that reason.
4. Our rubric grades risk type, not severity or consequence magnitude (#6, #8). A human
   analyst would consider that a bigger limitation than the 17% stability figure.
