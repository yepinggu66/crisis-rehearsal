# -*- coding: utf-8 -*-
"""``crh demo`` — the 30-second proof path.

One command, offline, no API key, no network, no MiroFish: verify the evidence
pack, recompute every published number, render the four event dossiers whose
rehearsal report is shipped, and write an index page that links them.

This is what a reader should run first. It is deliberately not a simulation: the
demo proves the evidence and the tooling, and it says so.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Optional

from . import __version__
from .evidence import verify as verify_evidence
from .html import badge, callout, esc, chips, kpis, page, section, table
from .paths import find_repo
from .report import (SHIPPED_REPORT_EVENTS, build_context, write_dossier)
from .stats import compute as compute_stats

DEMO_LIMIT_SECONDS = 10.0


class DemoFailed(RuntimeError):
    """Raised when the demo cannot honestly finish (e.g. evidence drift)."""


def _display_path(path: Path, cwd: Optional[Path] = None) -> str:
    """Machine-independent path for console output and archived transcripts."""
    cwd = (cwd or Path.cwd()).resolve()
    try:
        resolved = Path(path).resolve()
    except OSError:  # pragma: no cover - defensive
        return str(path)
    if resolved == cwd:
        return "."
    try:
        return resolved.relative_to(cwd).as_posix()
    except ValueError:
        return resolved.as_posix()


def nav_html(items) -> str:
    """Build the top-bar navigation fragment from (label, href) pairs."""
    return "".join(f'<a href="{esc(href)}">{esc(label)}</a>' for label, href in items)


def run(repo: Optional[object] = None, out: Optional[object] = None,
        echo=None) -> dict:
    """Run the offline demo. Returns a summary dict (also used by the tests)."""
    write = echo or (lambda line="": print(line))
    started = time.perf_counter()
    root = find_repo(repo)
    out_dir = Path(str(out)).expanduser() if out is not None else root / "demo_out"
    if not Path(str(out_dir)).is_absolute():
        out_dir = (Path.cwd() / str(out_dir)).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    write(f"Crisis Rehearsal Engine {__version__} — offline demo")
    write("=" * 74)
    write(f"repo      : {_display_path(root)}")
    write(f"output    : {_display_path(out_dir)}")
    write(f"python    : {sys.version.split()[0]}")
    write("")

    # [1/4] evidence integrity ------------------------------------------------
    verification = verify_evidence(root)
    if not verification["manifest_present"]:
        write(f"[1/4] evidence integrity : FAILED — {verification['message']}")
        raise DemoFailed(verification["message"])
    counts = verification["counts"]
    if not verification["ok"]:
        write(f"[1/4] evidence integrity : FAILED — {counts['OK']} OK, "
              f"{counts['MODIFIED']} modified, {counts['MISSING']} missing, "
              f"{counts['UNLISTED']} unlisted")
        for row in verification["rows"]:
            if row["status"] != "OK":
                write(f"        {row['status']}: {row['path']}")
        write("        The evidence pack does not match data/evidence.sha256; the demo")
        write("        refuses to present numbers derived from a drifted pack.")
        raise DemoFailed("evidence integrity check failed")
    write(f"[1/4] evidence integrity : PASS — {counts['OK']} files match "
          "data/evidence.sha256")

    # [2/4] published numbers -------------------------------------------------
    stats_result = compute_stats(root)
    hit = stats_result["hit"]
    variance = stats_result["variance"]
    sta = stats_result["sta"]
    write(f"[2/4] published numbers  : {hit['rate_pct']:.1f}% Top-3 hit rate "
          f"(95% CI {hit['ci_t_pct'][0]:.1f}-{hit['ci_t_pct'][1]:.1f}, "
          f"n={stats_result['n_events']} events)")
    write(f"                           within-event SD {variance['within_sd']:.2f}/3, "
          f"{stats_result['identical']['n']}/{stats_result['n_events']} identical, "
          f"STA {sta['batch']:.0f} ({sta['verdict']}, pass line {sta['pass_line']})")
    write(f"                           matches published README numbers: "
          f"{'yes' if stats_result['published_match'] else 'NO — see crh stats'}")

    # [3/4] dossiers ----------------------------------------------------------
    context = build_context(root, stats_result=stats_result, check_evidence=False)
    context["manifest"] = verification
    written = []
    for eid in SHIPPED_REPORT_EVENTS:
        if eid not in context["events"]:
            continue
        path = write_dossier(root, eid, out=out_dir, context=context,
                             nav_html=nav_html([("Demo index", "index.html")]))
        written.append((eid, path))
    names = ", ".join(eid for eid, _ in written)
    write(f"[3/4] event dossiers     : {len(written)} written "
          f"(events with a shipped rehearsal report: {names})")

    # [4/4] index -------------------------------------------------------------
    elapsed = time.perf_counter() - started
    index_path = out_dir / "index.html"
    index_path.write_text(
        _render_index(stats_result, verification, context, written, elapsed),
        encoding="utf-8", newline="\n")
    write(f"[4/4] index              : {_display_path(out_dir / 'index.html')}")
    write("")

    elapsed = time.perf_counter() - started
    if elapsed > DEMO_LIMIT_SECONDS:  # pragma: no cover - would need a very slow disk
        write(f"WARNING: the demo took {elapsed:.1f}s, over the {DEMO_LIMIT_SECONDS:.0f}s "
              "budget. Check the disk and the Python build.")
    write(f"done in {elapsed:.2f}s — offline, no API key, no network.")
    write(f"Open {_display_path(out_dir / 'index.html')} to read the dossiers.")
    write("Next: `crh stats --json` for the full number set, `crh report --event N` "
          "for any of the 30 events.")
    return {
        "ok": True,
        "repo": str(root),
        "out": str(out_dir),
        "elapsed_seconds": elapsed,
        "verify": verification,
        "stats": stats_result,
        "dossiers": [str(path) for _eid, path in written],
        "index": str(index_path),
    }


def _render_index(stats_result: dict, verification: dict, context: dict,
                  written, elapsed: float) -> str:
    hit = stats_result["hit"]
    variance = stats_result["variance"]
    sta = stats_result["sta"]
    counts = verification["counts"]

    hero = chips([
        ("mode", "offline demo"),
        ("API key", "not required"),
        ("network", "not used"),
        ("events", str(stats_result["n_events"])),
        ("runs", str(stats_result["n_runs"])),
    ])

    headline = kpis([
        ("Top-3 hit rate", f"{hit['rate_pct']:.1f}%",
         f"event mean · 95% CI {hit['ci_t_pct'][0]:.1f}-{hit['ci_t_pct'][1]:.1f}"),
        ("Bootstrap CI", f"{hit['ci_bootstrap_pct'][0]:.1f}-"
                         f"{hit['ci_bootstrap_pct'][1]:.1f}%",
         f"{hit['bootstrap_resamples']:,} resamples, seed {hit['bootstrap_seed']}"),
        ("Within-event SD", f"{variance['within_sd']:.2f}/3",
         "re-running the same event moves the score"),
        ("Identical runs", f"{stats_result['identical']['n']}/"
                           f"{stats_result['identical']['of']}",
         f"{stats_result['identical']['pct']:.0f}% of events scored the same 3x"),
        ("Stability STA", f"{sta['batch']:.0f}",
         f"pass line {sta['pass_line']} — {sta['verdict']}"),
        ("Evidence files", f"{counts['OK']}",
         "sha256 verified, 0 drift"),
    ])

    dossier_rows = []
    for eid, path in written:
        per_event = stats_result["per_event"].get(eid) or {}
        event = context["events"].get(eid)
        name = event.title if event else (per_event.get("name") or eid)
        name_html = esc(name)
        if event and event.event_name_en:
            name_html += f'<br><span class="muted small">{esc(event.event_name_en)}</span>'
        scores = " / ".join(f"{score:.1f}" for score in per_event.get("scores", []))
        dossier_rows.append([
            f'<a href="{esc(path.name)}">#{esc(eid)}</a>',
            name_html,
            esc(event.crisis_type if event else ""),
            f"{per_event.get('mean', 0):.2f}/3",
            esc(scores),
            f"{per_event.get('sta', {}).get('value', 0):.0f}",
            badge("report body shipped", "ok"),
        ])

    verify_html = f"""
<ul>
  <li><b>Evidence integrity:</b> {counts['OK']} files under <code>data/</code> match
      <code>data/evidence.sha256</code> ({counts['MODIFIED']} modified,
      {counts['MISSING']} missing, {counts['UNLISTED']} unlisted).</li>
  <li><b>Published numbers:</b> recomputed by importing
      <code>scripts/ci_stats.py</code> and <code>scripts/sta_stats.py</code> from this
      checkout — not by copying their formulas. Published-number check:
      <b>{'all match' if stats_result['published_match'] else 'MISMATCH'}</b>.</li>
  <li><b>Dossiers:</b> {len(written)} self-contained HTML files (inline CSS, no
      JavaScript, no external assets) — safe to archive or attach to an email.</li>
</ul>"""

    dossiers_html = (
        f'<p class="section-sub">Events 1, 6, 25 and 28 are the only events with a '
        f'shipped rehearsal report body. The other 26 events have a seed, a real '
        f'outcome and three judge records; <code>crh report --event N</code> renders '
        f'them, but their pages contain no report body — we do not fabricate one.</p>'
        + table(["Event", "Scenario", "Crisis type", "Event mean", "Three runs", "STA",
                 "Report"],
                dossier_rows, numeric_columns=(3, 5))
        + '<p class="small muted">Open: '
        + ", ".join(f'<a href="{esc(path.name)}">event-{esc(eid)}.html</a>'
                    for eid, path in written)
        + "</p>"
    )

    reading_html = """
<p>Each dossier contains, in this order: the event dossier (the real outcome, clearly
marked as hindsight) · the T-72h information pack the engine was allowed to see · the
simulation configuration · Top-3 risks vs the real outcome for all three runs · the
three-run scores and the stability verdict · sha256 provenance for every artifact · the
honest limitations · and, for these four events only, the verbatim rehearsal report.</p>
<p class="small muted">Every page is one file: open it from a USB stick on an air-gapped
machine and it renders identically. There is no telemetry to switch off.</p>"""

    limits_html = f"""
<p>This demo does not run the swarm simulation. Regenerating the 90-run grid needs a
running MiroFish engine and an LLM API key — about 6 hours of wall clock and a few
dollars of API credit for the whole grid (README, reproduce level B). This page reads
what that pipeline already produced.</p>
<p>This is a rehearsal / backtest producing <b>directional evidence</b>, not a forecast.
82.2% is an event-mean graded score over 30 statistical units (30 events × 3 runs), and
our own stability score — STA {sta['batch']:.0f} — is below our pass line of 60. Both
facts are published on purpose: <b>a metric you only show when it passes is
marketing.</b></p>"""

    body = (
        headline
        + callout(
            "info", "What this page is",
            "<p>One command that proves the evidence and the tooling without running a "
            "simulation: verify the sha256 manifest, recompute every published number "
            "from the 90 judge records, render the four dossiers whose rehearsal report "
            "is shipped. <b>It is not a simulation and it is not a forecast.</b></p>")
        + section("1", "What was verified in this run", verify_html)
        + section("2", "Dossiers in this demo", dossiers_html,
                  subtitle="Four events, three runs each, one self-contained HTML file "
                           "per event.")
        + section("3", "How to read a dossier", reading_html)
        + section("4", "What this demo does not do", limits_html)
    )

    footer = (
        f"<footer><p>Generated by <code>crh demo</code> (Crisis Rehearsal Engine "
        f"v{esc(__version__)}) in {elapsed:.2f}s — offline, no API key, no network.</p>"
        f"<p>Every number on this page is recomputable with <code>crh stats</code>; "
        f"rebuild the page with <code>crh demo --out demo_out</code>. "
        f"Read README “Honest limitations” before quoting any figure.</p></footer>"
    )
    return page(
        title="Crisis Rehearsal Engine — offline demo",
        kicker="Offline evidence workstation · demo",
        heading="30 events, 90 judge records, one command, no API key.",
        subtitle="The published backtest, recomputed and rendered on your machine in "
                 "under ten seconds.",
        chips_html=hero,
        body=body,
        footer_html=footer,
    )
