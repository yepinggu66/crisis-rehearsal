# -*- coding: utf-8 -*-
"""Self-contained HTML rehearsal dossiers (``crh report``).

One event per page. The page is assembled **only** from artifacts that ship in
this repository: the event catalogue, the T-72h seed, the three judge records and
— for the four events where one exists — the verbatim rehearsal report.

Two honesty rules are structural, not editorial:

* the real outcome is always shown in a section labelled as hindsight, separate
  from the pre-crisis information pack;
* an event without a shipped report gets a page **without a report body**. There
  are exactly four shipped reports (events 1, 6, 25, 28); for the other 26 the
  page shows the seed, the outcome and the three-run scores and says so. No
  placeholder prose is generated to make a page look complete.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from . import __version__
from .data import (DataError, Event, event_ids, load_events, load_failure_note,
                   load_scores, load_seed, scores_for_event, shipped_report_path)
from .evidence import verify as verify_evidence
from .html import (badge, callout, chips, esc, evidence_block, kpis, page,
                   section, table)
from .markdown import md_to_html
from .paths import MANIFEST_REL, rel, sha256_file
from .stats import StatsUnavailable, compute as compute_stats

#: Events whose full rehearsal report is shipped in the repository. Kept in
#: sync with data/docs by ``tests/test_report.py`` (which probes the files).
SHIPPED_REPORT_EVENTS = ("1", "6", "25", "28")

HIT_LABEL = {"yes": "yes (1)", "partial": "partial (0.5)", "no": "no (0)"}
HIT_KIND = {"yes": "ok", "partial": "warn", "no": "danger"}

LIMITATIONS = (
    ("The judge is an LLM, not a human panel.",
     "Same model family, fixed prompt, fixed thresholds: reproducible, but "
     "human calibration has not been run yet (template in data/judge_calibration.md). "
     "The 95% CI excludes judge error by construction."),
    ("The judge grades risk type, not consequence severity.",
     "A rehearsal that names the right risk at the wrong scale can still score 2.5/3. "
     "We consider this a bigger limitation than the stability number."),
    ("The dominant error is a false escalation.",
     "In the five worst events, 5 of the 6 zero-scoring Top-3 slots were "
     "'legal pressure / blame the supplier' branches that never happened. It is a "
     "systematic false-positive mode, documented in data/failures.md."),
    ("30 events is small and Chinese-market only (2018-2026).",
     "A binary framing of the same data is roughly ±17pp at 95%; generalization "
     "outside this corpus is unproven."),
    ("There is no control condition in this release.",
     "No human-analyst baseline, no ablation. 82.2% describes the pipeline against a "
     "fixed rubric; it is not a claim that it beats an analyst."),
    ("Two simulation rounds is a simplification of real opinion dynamics.",
     "It is enough to produce escalation paths and the right questions; it is not a "
     "model of society."),
    ("A single run of a single event is noise.",
     "Only 5 of 30 events scored identically across three runs. The delivery rule is "
     "3-5 repeated runs read as a consensus, never the best draw."),
    ("The v0.1 report bodies carry an empty-interview caveat.",
     "Every v0.1 report says the agent interview interface returned 0 valid records "
     "(0/19), so the Top-3 rests on graph relations and propagation paths, not on "
     "first-person testimony. The step has not been re-run on v0.2 output."),
    ("82.2% is an event-mean graded score, not a probability.",
     "The statistical unit is 30 events, not 90 runs; the score is not a forecast and "
     "not a statement about the next crisis."),
    ("This page does not re-run anything.",
     "It assembles published artifacts. Every number can be recomputed offline "
     "(`crh stats`), but the 90 reports cannot be independently re-judged from this "
     "repository alone: only four report bodies are shipped."),
)


class ReportError(RuntimeError):
    """Raised for an unknown event id or unreadable inputs."""


def build_context(repo: Path, stats_result: Optional[dict] = None,
                  check_evidence: bool = True) -> dict:
    """Load everything a dossier needs, once, for one or many pages."""
    repo = Path(repo)
    try:
        catalogue = load_events(repo)
    except DataError as exc:
        raise ReportError(str(exc)) from exc
    if stats_result is None:
        try:
            stats_result = compute_stats(repo)
        except StatsUnavailable as exc:
            raise ReportError(str(exc)) from exc
    context = {
        "repo": repo,
        "events": catalogue,
        "scores": load_scores(repo),
        "stats": stats_result,
        "manifest": verify_evidence(repo) if check_evidence else None,
        "shipped": {},
    }
    for eid in catalogue:
        context["shipped"][eid] = _shipped_info(repo, eid)
    return context


def _shipped_info(repo: Path, eid: str) -> dict:
    path = shipped_report_path(repo, eid)
    if path is None:
        return {"present": False, "rel": None, "sha256": None, "text": None}
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        text = None
    return {"present": text is not None, "rel": rel(repo, path),
            "sha256": sha256_file(path), "text": text}


def _hit_badge(hit: object) -> str:
    key = str(hit or "").strip().lower()
    if key in HIT_KIND:
        return badge(HIT_LABEL[key], HIT_KIND[key])
    return badge(key or "n/a", "neutral")


def _run_section(eid: str, record: dict, index: int) -> tuple:
    """Build one 'run N' sub-block; returns (html, score)."""
    score = sum({"yes": 1.0, "partial": 0.5}.get(
        str(item.get("hit", "")).strip().lower(), 0.0)
        for item in (record.get("top3") or []))
    rows = []
    for item in record.get("top3") or []:
        rank = item.get("rank", "")
        risk = item.get("risk", "")
        why = item.get("why", "") or item.get("hit_note", "") or ""
        rows.append([
            esc(rank),
            esc(risk),
            _hit_badge(item.get("hit")),
            f'<span class="muted small">{esc(why)}</span>',
        ])
    run_label = esc(record.get("run", index + 1))
    heading = (
        f'<h3>Run {run_label} <span class="muted">— graded score '
        f'{score:.1f}/3</span></h3>'
    )
    notes = []
    if record.get("path_hit"):
        notes.append(f"Path hit: <b>{esc(record['path_hit'])}</b>")
    if record.get("early_warning") is not None:
        notes.append(f"Early-warning quality: <b>{esc(record['early_warning'])}/100</b>")
    if record.get("md5"):
        notes.append(f"Report md5: <code>{esc(record['md5'])}</code>")
    meta = ('<p class="small muted">' + " &middot; ".join(notes) + "</p>") if notes else ""
    comment = record.get("comment")
    comment_html = (f'<p><b>Judge comment.</b> <span class="muted">{esc(comment)}</span></p>'
                    if comment else "")
    body = meta + table(["Rank", "Top-3 risk as reported", "Judge verdict", "Judge reasoning"],
                        rows, numeric_columns=(0,)) + comment_html
    return heading + body, score


def render_dossier(repo: Path, eid: str, context: Optional[dict] = None,
                   nav_html: str = "") -> str:
    """Render one self-contained dossier page for event *eid*."""
    repo = Path(repo)
    context = context or build_context(repo)
    eid = str(eid)
    events = context["events"]
    if eid not in events:
        valid = ", ".join(event_ids(repo))
        raise ReportError(f"unknown event id {eid!r}; shipped events: {valid}")
    event: Event = events[eid]
    per_event = context["stats"]["per_event"].get(eid)
    if per_event is None:
        raise ReportError(f"event {eid} has no judge records in the shipped evidence pack")
    shipped = context["shipped"].get(eid) or {"present": False}
    seed_text = load_seed(repo, eid)
    records = scores_for_event(context["scores"], eid)
    sta = per_event["sta"]
    sta_value = sta["value"]

    # ---------------------------------------------------------------- hero --
    report_badge = (badge("rehearsal report shipped", "ok") if shipped["present"]
                    else badge("no report body shipped", "neutral"))
    hero_chips = chips([
        ("event", f"#{eid}"),
        ("type", event.crisis_type),
        ("date", event.date),
        ("predictability", event.predictability),
        ("statistical unit", "event mean of 3 runs"),
    ])
    hero_sub = " · ".join(
        part for part in (event.event_name_en, event.entity, event.year) if part)
    kpi_html = kpis([
        ("3-run mean score", f"{per_event['mean']:.2f}/3",
         f"runs: {' / '.join(f'{s:.1f}' for s in per_event['scores'])}"),
        ("Top-3 hit rate", f"{per_event['hit_rate_pct']:.1f}%",
         "event-mean graded score, not a probability"),
        ("Run-to-run SD", f"{per_event['sd']:.2f}/3",
         "same event, three runs"),
        ("Stability STA", f"{sta_value:.0f}/100",
         f"pass line 60 — {sta['reading']}"),
        ("report body", "shipped" if shipped["present"] else "not shipped",
         "the four shipped reports are events 1, 6, 25, 28"),
    ])
    header_callout = callout(
        "info", "What this page is",
        "<p>An archived rehearsal dossier assembled from the public evidence pack: "
        "the pre-crisis seed, the swarm-simulation configuration, the three judge "
        "records and, where one exists, the verbatim 8k-character rehearsal report. "
        f"{report_badge}</p>"
        "<p class=\"small muted\">The simulation is not re-run to produce this page. "
        "Every number below is recomputable offline with <code>crh stats</code>; "
        "nothing here is a forecast.</p>",
    )

    # ------------------------------------------------- 1. event dossier ----
    source_lines = "<br>".join(esc(url) for url in event.sources()) or "—"
    dossier_rows = [
        ["Entity / 主体", esc(event.entity)],
        ["Event / 事件", esc(event.title) + f'<br><span class="muted small">'
                                           f'{esc(event.event_name_en)}</span>'],
        ["Crisis type / 危机类型", esc(event.crisis_type)],
        ["Date / 事发时间", esc(event.date)],
        ["Predictability label / 可预测性", esc(event.predictability)
         + '<br><span class="muted small">high/medium/low; the three low-predictability '
           "events are kept as negative samples</span>"],
        ["Real trigger / 真实触发点", esc(event.trigger)],
        ["Real outcome / 真实结局", esc(event.outcome)],
        ["Penalty &amp; fallout / 处罚与处置", esc(event.penalty)],
        ["Public sources / 公开来源", f'<span class="mono">{source_lines}</span>'],
    ]
    dossier_html = (
        callout("warn", "Hindsight boundary",
                "<p>Everything in this section is what actually happened, and it is "
                "in the pack <b>only</b> to score the rehearsal. The simulation never "
                "saw it: the seed it received is restricted to public information "
                "available 72 hours before T0.</p>")
        + table(["Field", "Value"], dossier_rows)
        + f'<p class="small muted">Source: <code>data/events.csv</code>, row #{esc(eid)}.</p>'
    )

    # ------------------------------------------- 2. T-72h information pack --
    if seed_text:
        seed_html = (
            callout("info", "Information clean room (docs/methodology.md §1)",
                    "<p>The seed contains only what a careful analyst could have known "
                    "72 h before the crisis went public: no outcome, no penalty, no "
                    "stock reaction. The v0.2.2 sweep removed 91 unfilled placeholders, "
                    "moved the outcome-derived predictability rating out of the seeds "
                    "and truncated any chain that started describing post-T0 events.</p>")
            + f'<div class="doc">{md_to_html(seed_text)}</div>'
            + f'<p class="small muted">Source: <code>data/seeds/{esc(eid)}.md</code> '
              f'· sha256 <code>{esc(sha256_file(repo / "data" / "seeds" / f"{eid}.md"))}</code></p>'
        )
    else:
        seed_html = callout(
            "warn", "Seed not shipped for this event",
            "<p>This checkout does not contain <code>data/seeds/"
            f"{esc(eid)}.md</code>, so the pre-crisis pack cannot be shown.</p>")

    # --------------------------------------- 3. simulation configuration -----
    run_md5 = [(str(record.get("run", "")), record.get("md5") or "n/a")
               for record in records]
    config_rows = [
        ["Engine", "MiroFish (AGPL-3.0), pinned to upstream commit "
                   "<code>7657031ac01184afe2cb220f5ee3545573b5e843</code>, plus 5 "
                   "reviewed patches (local graph adapter + 4 hooks)"],
        ["Knowledge graph", "Local JSON graph adapter — no Zep Cloud, no cloud graph "
                            "service; ~12 nodes per event"],
        ["Persona agents", "7–12 per event: journalists, retail investors, regulators, "
                           "short sellers, competitors, consumers"],
        ["Simulation", "2 rounds on a simulated Twitter/Reddit feed"],
        ["Model", "DeepSeek or any OpenAI-compatible endpoint (LLM_API_KEY / "
                  "LLM_BASE_URL / LLM_MODEL_NAME)"],
        ["Seed", f"<code>data/seeds/{esc(eid)}.md</code> — identical for all three runs"],
        ["Judge", "Fixed Chinese prompt, unchanged since v0.1 "
                  "(<code>scripts/score_repeat.py</code>): returns "
                  "<code>top3[{rank,risk,hit(yes/partial/no),why}]</code>, "
                  "<code>path_hit</code>, <code>early_warning(0-100)</code>"],
        ["Scoring", "hit = yes 1 / partial 0.5 / no 0 → one run scores 0–3; the event "
                    "score is the mean of its runs; hit rate = event mean / 3"],
        ["Observed cost", "≈ $0.03 and ≈ 4 minutes per run (v0.2 measurement)"],
        ["Report size", "≈ 8,000 characters per run (≈ 23 KB)"],
    ]
    md5_html = "<br>".join(
        f"run {esc(run)}: <code>{esc(md5)}</code>" for run, md5 in run_md5) or "n/a"
    config_html = (
        table(["Component", "Configuration"], config_rows)
        + evidence_block([("judge record md5", "each run is scored against its own "
                                              "report — md5 recorded by the judge")])
        + f'<div class="evidence">report md5 per run<br>{md5_html}</div>'
        + callout("info", "What is not here",
                  "<p>This page does not re-run the simulation. Regenerating the grid "
                  "needs a running MiroFish and an LLM key: 90 runs × ~4 minutes plus "
                  "a few dollars of API credit (README, reproduce level B). The "
                  "evidence workstation reads what that pipeline already produced.</p>")
    )

    # ------------------------------- 4. Top-3 risks vs the real outcome -----
    run_blocks = []
    for index, record in enumerate(records):
        block, _score = _run_section(eid, record, index)
        run_blocks.append(block)
    top3_html = (
        callout("info", "How to read the matrix",
                "<p>Each run's Top-3 risks are graded against the real outcome by the "
                "fixed judge prompt. <b>yes</b> = same risk type and mechanism; "
                "<b>partial</b> = same type, different mechanism; <b>no</b> = absent. "
                "The judge is told not to reward writing quality.</p>")
        + "".join(run_blocks)
        + callout("warn", "Reading discipline",
                  "<p>A single run is noise: only 5 of 30 events scored identically "
                  "across three runs. Read the consensus, never the best draw. The "
                  "rubric grades <b>risk type</b>, not consequence severity.</p>")
    )
    shipped_callout = ""
    if not shipped["present"]:
        shipped_callout = callout(
            "danger", "No rehearsal report body is published for this event",
            "<p>The evidence pack contains the T-72h seed, the real outcome and three "
            "judge records for this event — no 8k-character rehearsal report. "
            "Only four report bodies are shipped in this repository (events 1, 6, 25, "
            "28). We do not fabricate a report to fill this page: what you see is "
            "exactly what the pack contains.</p>")

    # -------------------------------- 5. three-run scores and stability -----
    score_rows = []
    for record in records:
        score = sum({"yes": 1.0, "partial": 0.5}.get(
            str(item.get("hit", "")).strip().lower(), 0.0)
            for item in (record.get("top3") or []))
        score_rows.append([
            esc(record.get("run", "")),
            f"{score:.1f}",
            esc(record.get("early_warning") if record.get("early_warning") is not None
                else "n/a"),
            esc(record.get("path_hit") or "n/a"),
            f'<code>{esc(record.get("md5") or "n/a")}</code>',
        ])
    verdict_kind = ("ok" if sta_value >= 75 else
                    "warn" if sta_value >= 60 else "danger")
    sta_rows = [
        ["STA (weighted stability score)", f"{sta_value:.0f}/100",
         f"{'PASS' if sta_value >= 60 else 'FAILED'} — pass line 60, funding line 75"],
        ["J̄ item agreement", f"{sta['jbar']:.2f}", "Top-3 item overlap after merging "
                                                    "items by meaning (Jaccard)"],
        ["D disagreement", f"{sta['d']:.2f}",
         "D ≥ 0.40 must be reported as a split, not a single number"],
        ["Kendall's W", f"{sta['w']:.2f}", "rank agreement across runs"],
        ["CV(HR@3)", f"{sta['cv_hr']:.2f}", "coefficient of variation of the score"],
        ["CV̄ (HR@3 and early warning)", f"{sta['cv_bar']:.2f}", "metric-level variation"],
    ]
    score_html = (
        table(["Run", "Graded score /3", "Early warning", "Path hit", "Report md5"],
              score_rows, numeric_columns=(1,)) +
        table(["Stability component", "Value", "Meaning"], sta_rows, numeric_columns=()) +
        f'<p>Event mean <b>{per_event["mean"]:.2f}/3</b> = '
        f'<b>{per_event["hit_rate_pct"]:.1f}%</b> of the maximum; run-to-run SD '
        f'<b>{per_event["sd"]:.2f}/3</b>. Stability verdict: '
        f'{badge("STA " + format(sta_value, ".0f"), verdict_kind)} '
        f'<span class="muted small">{esc(sta["reading"])}</span></p>'
        + f'<p class="small muted">STA = 100 × [0.40·J̄ + 0.30·(1 − CV̄) + 0.30·Kendall W], '
          f'fixed before the v0.2 run (internal evaluation template §2.5); item merge: '
          f'{esc(context["stats"]["sta"]["item_merge"])}.</p>'
    )
    if sta.get("disagreement"):
        score_html += callout(
            "danger", "Disagreement flag: report a split, not a number",
            f"<p>D = {sta['d']:.2f} ≥ 0.40: the three runs do not describe the same "
            "Top-3. Deliver this event as 'consensus + disagreement' with the run "
            f"scores ({' / '.join(f'{s:.1f}' for s in per_event['scores'])}) shown "
            "next to it — never as one score.</p>")

    # ---------------------------------- 6. evidence and sha256 provenance ---
    hash_rows = []

    def add_hash(label: str, relpath: str) -> None:
        path = repo / relpath
        digest = sha256_file(path)
        hash_rows.append([esc(label), f'<code>{esc(relpath)}</code>',
                          f'<code class="mono">{esc(digest)}</code>'])

    add_hash("event catalogue", "data/events.csv")
    add_hash("judge records (90)", "data/repeat_v02/scores.jsonl")
    add_hash("v0.1 baseline", "data/repeat_v02/scores_v01.jsonl")
    add_hash("STA item merge", "data/repeat_v02/item_clusters.json")
    if seed_text:
        add_hash("T-72h seed", f"data/seeds/{eid}.md")
    if shipped["present"]:
        add_hash("verbatim report", shipped["rel"])
    manifest = context.get("manifest")
    if manifest is None:
        manifest_line = "not checked"
    elif not manifest["manifest_present"]:
        manifest_line = "manifest missing"
    elif manifest["ok"]:
        manifest_line = (f"PASS — {manifest['counts']['OK']} files match "
                         f"data/evidence.sha256")
    else:
        counts = manifest["counts"]
        manifest_line = (f"FAIL — {counts['MODIFIED']} modified, {counts['MISSING']} "
                         f"missing, {counts['UNLISTED']} unlisted")
    provenance_html = (
        table(["Artifact", "Path", "sha256"], hash_rows)
        + evidence_block([
            ("manifest", MANIFEST_REL.as_posix()),
            ("integrity", manifest_line),
            ("verify", "crh verify"),
            ("recompute", "crh stats --json"),
            ("page", f"generated by crh {__version__}; no external requests, no JS"),
        ])
        + callout("info", "Audit trail",
                  "<p>The sha256 values above are of the exact bytes this page was "
                  "built from. Run <code>crh verify</code> in the repository to check "
                  "the whole pack against <code>data/evidence.sha256</code>; a silent "
                  "edit to the evidence shows up as <code>MODIFIED</code> and fails "
                  "the command. Regenerate a manifest only with "
                  "<code>crh verify --write</code>, and review the diff.</p>")
    )

    # ------------------------------------------- 7. honest limitations -------
    limitation_items = "".join(
        f"<li><b>{esc(head)}</b> {esc(body)}</li>" for head, body in LIMITATIONS)
    limitations_html = (
        f"<p>This section is the part most benchmark write-ups skip. Hold us to it.</p>"
        f"<ul>{limitation_items}</ul>"
    )
    failure_note = load_failure_note(repo, eid)
    if failure_note:
        limitations_html += (
            "<h3>Published post-mortem for this event</h3>"
            f'<div class="doc">{md_to_html(failure_note)}</div>'
            '<p class="small muted">Source: <code>data/failures.md</code> — written '
            "after the fact, quoting the judge's own recorded justifications.</p>"
        )

    # --------------------------------- 8. shipped rehearsal report (if any) --
    report_html = ""
    if shipped["present"] and shipped["text"]:
        report_html = section(
            "", "Shipped rehearsal report (verbatim)",
            callout("ok", "Verbatim, not edited",
                    "<p>The report below was generated by the engine and is "
                    "reproduced byte-for-byte from "
                    f"<code>{esc(shipped['rel'])}</code> (sha256 "
                    f"<code>{esc(shipped['sha256'])}</code>). It contains the "
                    "engine's own caveats, including the empty-interview note on "
                    "v0.1 output. Editorial changes would make the backtest "
                    "unfalsifiable, so there are none.</p>")
            + f'<div class="doc">{md_to_html(shipped["text"])}</div>',
            subtitle="The full ~8k-character report generated by the MiroFish "
                     "ReportAgent, reproduced without edits. This is the artifact the "
                     "judge scored.",
        )

    body = (
        kpi_html
        + header_callout
        + section("1", "Event dossier — what really happened", dossier_html,
                  subtitle="After-the-fact record used only as the scoring ground "
                           "truth.")
        + section("2", "T-72h information pack — what the engine was allowed to see",
                  seed_html,
                  subtitle="Public information available 72 hours before T0. No "
                           "hindsight.")
        + section("3", "Group simulation configuration", config_html)
        + section("4", "Top-3 risks vs the real outcome", shipped_callout + top3_html,
                  subtitle="Three independent runs, one fixed judge rubric.")
        + section("5", "Three-run scores and stability", score_html,
                  subtitle="A single run is noise; STA tells you whether the three runs "
                           "describe the same thing.")
        + section("6", "Evidence and sha256 provenance", provenance_html)
        + section("7", "Honest limitations", limitations_html,
                  subtitle="Known weaknesses, in the order that matters for a buyer.")
        + report_html
    )

    footer = (
        f"<footer>"
        f"<p><b>Crisis Rehearsal Engine</b> v{esc(__version__)} — dossier for event "
        f"#{esc(eid)}. Generated from the public evidence pack in this repository; "
        f"no client data, no network access, no JavaScript, no external assets.</p>"
        "<p>This is a rehearsal / backtest producing <b>directional evidence</b>, not a "
        "forecast and not a probability. 82.2% is an event-mean graded score over 30 "
        "statistical units (30 events × 3 runs); read README “Honest limitations” "
        "before quoting any number from this page.</p>"
        f"<p>Verify the pack with <code>crh verify</code>; recompute every figure with "
        f"<code>crh stats</code>; rebuild this page with "
        f"<code>crh report --event {esc(eid)}</code>.</p>"
        "</footer>"
    )

    title = f"Event #{eid} {event.title} — crisis rehearsal dossier"
    return page(
        title=title,
        kicker=f"Crisis rehearsal dossier · event #{eid} · v0.2 public backtest",
        heading=esc(event.title),
        subtitle=hero_sub,
        chips_html=hero_chips,
        body=body,
        footer_html=footer,
        nav_html=nav_html,
        lang="zh-CN",
    )


def output_path(repo: Path, eid: str, out: Optional[object] = None) -> Path:
    """Resolve the output file for one dossier.

    ``out`` may be a directory, or a file path ending in ``.html``. Default is
    ``<repo>/reports/event-{id}.html``.
    """
    if out is None:
        return Path(repo) / "reports" / f"event-{eid}.html"
    target = Path(str(out)).expanduser()
    if target.suffix.lower() == ".html":
        return target
    return target / f"event-{eid}.html"


def write_dossier(repo: Path, eid: str, out: Optional[object] = None,
                  context: Optional[dict] = None, nav_html: str = "") -> Path:
    """Render and write one dossier; returns the file path."""
    html_text = render_dossier(repo, eid, context=context, nav_html=nav_html)
    target = output_path(Path(repo), str(eid), out)
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(str(target), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html_text)
    return target
