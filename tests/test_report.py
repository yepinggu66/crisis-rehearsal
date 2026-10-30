# -*- coding: utf-8 -*-
"""`crh report`: self-contained dossiers, with an honest body/no-body distinction."""
import re

import pytest

from crisis_rehearsal import cli
from crisis_rehearsal.data import load_events, load_seed, shipped_report_path
from crisis_rehearsal.paths import sha256_file
from crisis_rehearsal.report import (SHIPPED_REPORT_EVENTS, ReportError,
                                     output_path, render_dossier, write_dossier)

EXTERNAL_RESOURCE = re.compile(
    r'(<script\b|<link\b|\bsrc\s*=|@import|url\(\s*["\']?https?:|'
    r'<iframe\b|srcset\s*=)')


@pytest.mark.parametrize("event_id", ["1", "2", "6", "8", "21", "23", "25", "28", "30"])
def test_dossier_is_self_contained(context, repo, event_id):
    html = render_dossier(repo, event_id, context=context)
    assert html.startswith("<!DOCTYPE html>")
    assert EXTERNAL_RESOURCE.search(html) is None, "external resource reference found"
    assert "<script" not in html.lower()
    assert "http" not in "".join(
        match for match in re.findall(r'<[^>]+>', html)
        if re.search(r'\b(src|href|action)=', match))  # no remote attributes


def test_all_thirty_events_render(context, repo):
    events = load_events(repo)
    assert len(events) == 30
    for event_id in sorted(events, key=int):
        html = render_dossier(repo, event_id, context=context)
        assert events[event_id].event_name_zh[:6] in html
        assert "Honest limitations" in html


def test_required_sections(context, repo):
    html = render_dossier(repo, "6", context=context)
    for marker in (
        "Event dossier — what really happened",
        "T-72h information pack — what the engine was allowed to see",
        "Group simulation configuration",
        "Top-3 risks vs the real outcome",
        "Three-run scores and stability",
        "Evidence and sha256 provenance",
        "Honest limitations",
    ):
        assert marker in html, marker
    assert "hindsight" in html.lower()
    assert "82.2% is an event-mean graded score" in html
    assert "STA" in html


def test_real_outcome_and_sources_rendered(context, repo):
    events = load_events(repo)
    event = events["6"]
    html = render_dossier(repo, "6", context=context)
    assert event.outcome[:6] in html
    assert event.trigger[:6] in html
    assert event.penalty[:6] in html
    assert "data/events.csv" in html


def test_seed_pack_is_rendered(context, repo):
    seed = load_seed(repo, "6")
    assert seed
    html = render_dossier(repo, "6", context=context)
    assert seed.splitlines()[0].lstrip("# ")[:8] in html
    assert "Information clean room" in html


def test_shipped_events_include_the_verbatim_report(context, repo):
    for event_id in SHIPPED_REPORT_EVENTS:
        path = shipped_report_path(repo, event_id)
        assert path is not None, f"expected a shipped report for event {event_id}"
        text = path.read_text(encoding="utf-8")
        html = render_dossier(repo, event_id, context=context)
        assert "Shipped rehearsal report (verbatim)" in html
        assert text.splitlines()[0].lstrip("# ")[:10] in html
        assert sha256_file(path) in html
        assert "Verbatim, not edited" in html


@pytest.mark.parametrize("event_id", ["2", "8", "14", "21", "30"])
def test_non_shipped_events_do_not_fabricate_a_body(context, repo, event_id):
    assert shipped_report_path(repo, event_id) is None
    html = render_dossier(repo, event_id, context=context)
    assert "Shipped rehearsal report (verbatim)" not in html
    assert "No rehearsal report body is published for this event" in html
    assert "Shipped report" not in html
    # no report text from the four shipped reports may leak into another event
    for shipped_id in SHIPPED_REPORT_EVENTS:
        text = shipped_report_path(repo, shipped_id).read_text(encoding="utf-8")
        first_heading = text.splitlines()[0].lstrip("# ")[:12]
        assert first_heading not in html


def test_sha256_provenance(context, repo):
    html = render_dossier(repo, "6", context=context)
    full = sha256_file(repo / "data" / "repeat_v02" / "scores.jsonl")
    assert full in html
    assert "crh verify" in html
    assert "data/evidence.sha256" in html
    assert "files match" in html and "PASS" in html


def test_failure_postmortem_is_included_when_published(context, repo):
    html6 = render_dossier(repo, "6", context=context)
    assert "slot padding" in html6
    assert "Published post-mortem for this event" in html6
    html2 = render_dossier(repo, "2", context=context)
    assert "Published post-mortem for this event" not in html2


def test_hit_badges_and_judge_reasoning(context, repo):
    html = render_dossier(repo, "6", context=context)
    assert "yes (1)" in html or "partial (0.5)" in html
    assert "Judge comment." in html
    assert "partial (0.5)" in html


def test_unknown_event_raises_and_cli_exits_2(repo, capsys):
    with pytest.raises(ReportError):
        render_dossier(repo, "999")
    assert cli.main(["report", "--event", "999"]) == 2
    assert "unknown event id" in capsys.readouterr().err.lower()


def test_write_dossier_to_directory_and_file(repo, tmp_path, context):
    directory = write_dossier(repo, "6", out=tmp_path, context=context)
    assert directory == tmp_path / "event-6.html"
    assert directory.is_file() and directory.stat().st_size > 20000
    explicit = write_dossier(repo, "1", out=tmp_path / "custom.html", context=context)
    assert explicit == tmp_path / "custom.html"
    assert explicit.is_file()


def test_output_path_defaults_to_reports_dir(repo):
    path = output_path(repo, "6")
    assert path == repo / "reports" / "event-6.html"


def test_cli_report_output(repo, tmp_path, capsys):
    target = tmp_path / "dossiers"
    assert cli.main(["report", "--event", "6", "--out", str(target)]) == 0
    output = capsys.readouterr().out
    assert "self-contained" in output
    assert "verbatim" in output
    assert (target / "event-6.html").is_file()
    assert cli.main(["report", "--event", "2", "--out", str(target)]) == 0
    assert "no rehearsal report is shipped" in capsys.readouterr().out
