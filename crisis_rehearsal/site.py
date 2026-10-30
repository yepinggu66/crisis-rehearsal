# -*- coding: utf-8 -*-
"""``crh site`` — a static, self-contained dossier site for all 30 events.

No server, no framework, no JavaScript: a directory of HTML files that can be
hosted on an intranet, a government file share or GitHub Pages. Every page is a
full dossier from :mod:`crisis_rehearsal.report`; the index adds the cross-event
view (scores, stability, which events ship a rehearsal report).
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import Optional

from . import __version__
from .demo import _display_path, nav_html
from .evidence import verify as verify_evidence
from .html import badge, callout, esc, kpis, page, section, table
from .paths import find_repo
from .report import build_context, render_dossier, write_dossier
from .stats import compute as compute_stats


def generate(repo: Optional[object] = None, out: Optional[object] = None,
             echo=None) -> dict:
    """Render the index + one dossier per event. Returns a summary dict."""
    write = echo or (lambda line="": print(line))
    started = time.perf_counter()
    root = find_repo(repo)
    out_dir = Path(str(out)).expanduser() if out is not None else root / "site"
    if not Path(str(out_dir)).is_absolute():
        out_dir = (Path.cwd() / str(out_dir)).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    write(f"Crisis Rehearsal Engine {__version__} — static dossier site")
    write("=" * 74)
    write(f"repo      : {_display_path(root)}")
    write(f"output    : {_display_path(out_dir)}")

    stats_result = compute_stats(root)
    context = build_context(root, stats_result=stats_result, check_evidence=False)
    context["manifest"] = verify_evidence(root)

    ids = sorted(context["events"], key=lambda value: int(value))
    files = []
    for eid in ids:
        files.append(write_dossier(
            root, eid, out=out_dir, context=context,
            nav_html=nav_html([("All 30 events", "index.html"),
                               ("Recompute", "index.html#numbers")])))

    index_path = out_dir / "index.html"
    index_path.write_text(
        _render_index(stats_result, context, ids, time.perf_counter() - started),
        encoding="utf-8", newline="\n")
    elapsed = time.perf_counter() - started
    write(f"pages     : {len(files)} event dossiers + index")
    write(f"index     : {_display_path(index_path)}")
    write(f"done in {elapsed:.2f}s — offline, no API key. Open "
          f"{_display_path(index_path)}.")
    return {
        "ok": True,
        "repo": str(root),
        "out": str(out_dir),
        "index": str(index_path),
        "pages": [str(path) for path in files],
        "elapsed_seconds": elapsed,
    }


def _render_index(stats_result: dict, context: dict, ids, elapsed: float) -> str:
    hit = stats_result["hit"]
    variance = stats_result["variance"]
    sta = stats_result["sta"]
    counts = context["manifest"]["counts"] if context.get("manifest") else {}

    headline = kpis([
        ("Events", str(stats_result["n_events"]), "public crises, 2018-2026"),
        ("Runs", str(stats_result["n_runs"]), "3 repeats per event"),
        ("Top-3 hit rate", f"{hit['rate_pct']:.1f}%",
         f"event mean · 95% CI {hit['ci_t_pct'][0]:.1f}-{hit['ci_t_pct'][1]:.1f}"),
        ("Within-event SD", f"{variance['within_sd']:.2f}/3", "run-to-run noise"),
        ("Stability STA", f"{sta['batch']:.0f}",
         f"pass line {sta['pass_line']} — {sta['verdict']}"),
    ])

    rows = []
    for eid in ids:
        event = context["events"][eid]
        per_event = stats_result["per_event"].get(eid) or {}
        sta_value = (per_event.get("sta") or {}).get("value", 0)
        kind = "ok" if sta_value >= 75 else "warn" if sta_value >= 60 else "danger"
        shipped = context["shipped"].get(eid) or {}
        scores = " / ".join(f"{score:.1f}" for score in per_event.get("scores", []))
        rows.append([
            f'<a href="event-{esc(eid)}.html">#{esc(eid)}</a>',
            esc(event.title) + f'<br><span class="muted small">'
                               f'{esc(event.event_name_en)}</span>',
            esc(event.crisis_type),
            esc(event.predictability),
            esc(scores),
            f"{per_event.get('mean', 0):.2f}/3",
            badge(f"{sta_value:.0f}", kind),
            badge("shipped", "ok") if shipped.get("present")
            else badge("seed + scores only", "neutral"),
        ])

    numbers_html = f"""
<p>Headline (recomputed from <code>data/repeat_v02/scores.jsonl</code>, the 90 shipped
judge records):</p>
{table(["Metric", "Value", "Note"], [
    ['Top-3 risk hit rate (event mean)', f"{hit['rate_pct']:.1f}%",
     f"95% CI {hit['ci_t_pct'][0]:.1f}-{hit['ci_t_pct'][1]:.1f} (t, df={hit['df']}); "
     f"bootstrap {hit['ci_bootstrap_pct'][0]:.1f}-{hit['ci_bootstrap_pct'][1]:.1f}%"],
    ["Within-event SD", f"{variance['within_sd']:.2f}/3",
     f"median {variance['within_sd_median']:.2f}/3"],
    ["Events identical across all 3 runs", f"{stats_result['identical']['n']}"
     f"/{stats_result['identical']['of']}",
     f"{stats_result['identical']['pct']:.0f}%"],
    ["Stability STA", f"{sta['batch']:.0f}",
     f"pass line {sta['pass_line']}, funding line {sta['funding_line']} — "
     f"{sta['verdict']}"],
    ["Evidence files verified", str(counts.get("OK", 0)),
     "sha256 against data/evidence.sha256"],
], numeric_columns=())}
<p class="small muted">Scoring discipline: 82.2% is an <b>event-mean graded score</b>
(0-3 per event, averaged across 30 events), not a binary hit rate and not a
probability. The 90 runs are not 90 independent samples; the statistical unit is the
event. Read a consensus of 3-5 repeats, never a single run.</p>"""

    body = (
        headline
        + callout("info", "What this site is",
                  "<p>One self-contained dossier per event of the public v0.2 backtest."
                  " Each dossier is a single HTML file: inline CSS, no JavaScript, no "
                  "external assets. This index adds the cross-event view. For the four "
                  "events with a shipped rehearsal report the dossier includes the "
                  "verbatim report; for the other 26 it contains the T-72h seed, the "
                  "real outcome and the three-run judge records only — no report body "
                  "is fabricated.</p>")
        + section("1", "All 30 events", table(
            ["Event", "Scenario", "Crisis type", "Predictability", "Three runs",
             "Event mean", "STA", "Report"],
            rows, numeric_columns=(5,)), anchor="events")
        + section("2", "The numbers this site is built on", numbers_html,
                  anchor="numbers")
        + section("3", "Honest limitations", f"""
<ul>
  <li>The judge is an LLM; human calibration has not been run yet.</li>
  <li>The rubric grades risk type, not consequence severity.</li>
  <li>Only {stats_result['identical']['n']} of {stats_result['n_events']} events score
      identically across three runs: a single run is noise.</li>
  <li>STA {sta['batch']:.0f} is below our own pass line of
      {sta['pass_line']}: we fail our own bar and publish it.</li>
  <li>30 events, Chinese-market, 2018-2026: generalization is unproven. This is
      directional evidence, not a forecast.</li>
</ul>""")
    )

    return page(
        title="Crisis Rehearsal Engine — 30-event dossier site",
        kicker="Public backtest · v0.2 · 30 events × 3 runs",
        heading="Rehearse the crisis 72 hours before it happens.",
        subtitle="A dossier per event, generated offline from the shipped evidence "
                 "pack. Every figure is recomputable; the failures are published too.",
        chips_html="",
        body=body,
        footer_html=(
            f"<footer><p>Generated by <code>crh site</code> (Crisis Rehearsal Engine "
            f"v{esc(__version__)}) in {elapsed:.2f}s — offline, no API key.</p>"
            f"<p>Recompute every number with <code>crh stats</code>; verify the pack "
            f"with <code>crh verify</code>.</p></footer>"),
    )
