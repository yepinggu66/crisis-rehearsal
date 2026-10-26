# Judge calibration — status: **NOT RUN**

> **Status: not yet run. Human calibration pending.**
> No human spot-check of the judge's scores has been performed for v0.1 or v0.2. The 82.2%
> headline is **LLM-judged only**, and the 95% CI excludes judge error by construction.
> This file exists to say that out loud and to hold the template the calibration will be
> recorded in. It is **not** evidence of anything yet — nothing below the protocol is filled
> in.

Planned release for the first calibration batch: **v0.2.2**. Owner: maintainers.

## Why this exists

The judge and the simulator are the same model family (`deepseek-chat`), so their errors can
be correlated: the judge may accept a risk because it "sounds like" what the simulator was
primed to produce. Every number in the README is therefore conditional on the judge being
right, and we have not verified that with a human. `docs/methodology.md` §4 defines the hit
codes; the README limitations section states the same caveat.

## Planned sample — 5 reports, one run each

Fixed in advance so the sample cannot be chosen after seeing the verdicts. Event choice is
driven by the failures already published in `data/failures.md` (the worst and the most
volatile events), plus one high-scoring control so the exercise can also catch a human who
just rubber-stamps the judge.

| # | Event | Why this event | Planned run |
|---|---|---|---|
| 6 | Luckin Coffee financial fraud (瑞幸咖啡财务造假) | The judge accepted the core risk but scored the padding slots `partial`/`no`; this is where the "grades risk type, not severity" blind spot shows up. | run 2 |
| 8 | Brilliance Group bond default (华晨集团债券违约) | All three runs scored exactly 2.0 (SD 0.00) while the Top-3 *items* drifted (D = 0.60). Tests whether a human agrees that a stable score can hide unstable reasoning. | run 2 |
| 21 | Jiangxi vocational college "rat head vs duck neck" (江西工职院鼠头鸭脖事件) | 1.5 / 3.0 / 2.5 across runs, driven by one fabricated branch. Tests the `no` the judge gave to "legal pressure on the whistleblower". | run 2 |
| 23 | Baidu VP Qu Jing short video remarks (百度副总裁璩静短视频言论) | Lowest event mean in the corpus (1.83/3), two `no` slots on a counter-attack branch that never happened. | run 2 |
| 7 | Ant Group IPO suspension (蚂蚁集团暂缓上市) | High-scoring control (3.0 / 3.0 / 2.5). Checks the human does not simply agree with every `yes`. | run 2 |

Run 2 is chosen for all five for the same reason: it is fixed before the human sees anything,
and it is neither the best nor the worst run of each event.

## Recording protocol (to be executed, not yet executed)

1. The human receives the same three inputs the judge received: the event metadata from
   `data/events.csv` (event, entity, crisis type, trigger, **outcome**, **penalty**), and the
   report excerpt truncated to 7,000 characters — see `scripts/score_repeat.py`.
2. The human does **not** see the judge's `top3`, `path_hit` or `comment` before writing their
   own verdict. The judge's record for the pair `(id, run)` is opened only afterwards.
3. The human applies the H1 definition from `docs/methodology.md` §3 to the report's own
   Top-3 items, in the report's own wording: `yes` / `partial` / `no` per slot, plus
   `path_hit`. `early_warning` is out of scope for calibration (it is a 0–100 quality score
   with no ground truth to check against).
4. Each slot is compared with the judge's code and classified:
   - `agree` — same code;
   - `too_lenient` — judge `yes`/`partial`, human `no`;
   - `too_strict` — judge `no`, human `yes`/`partial`;
   - `magnitude` — same direction, different weight (`yes` vs `partial`).
5. Every disagreement is written into the log below with the reason, in one sentence. Known
   judge weaknesses (`data/failures.md`: false escalation, magnitude blindness) are expected
   to show up as `too_lenient` / `magnitude`, not to disappear.
6. Reported result (planned): slot-level agreement over 15 slots (5 reports × 3 slots), the
   split by disagreement class, and a stated pass line of **≥ 80% slot agreement**
   (12/15). If the batch scores below that, the headline number gets relabelled
   "LLM-judged, human calibration failed" everywhere it is quoted, and the rubric is revised
   before any further promotion.

## Not shipped: report texts

The calibration needs the report texts. The v0.2 reports are not in this repository (only
the judge's records are), so calibration is run on the maintainers' `output_v2/` tree. The
`md5` field in `data/repeat_v02/scores.jsonl` is the first 10 hex chars of the md5 of the
7,000-character excerpt that was judged, so each completed record below can be tied back to a
shipped judge record even though the report itself is not public.

## Log — empty until the checks are actually run

Do not pre-fill this table. One row per report, filled in by hand after the comparison.

| Date | Event | Run | md5 (from scores.jsonl) | Judge H1 slots | Human H1 slots | Judge path_hit | Human path_hit | Agreement (n/3) | Disagreement classes | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | — | — | — | not yet run |

## Summary — empty until the batch is finished

| Batch | Reports | Slots | Agreement | too_lenient | too_strict | magnitude | Pass line (≥80%) | Verdict |
|---|---|---|---|---|---|---|---|---|
| v0.2 (planned, v0.2.2) | 5 | 15 | — | — | — | — | 12/15 | not yet run |
