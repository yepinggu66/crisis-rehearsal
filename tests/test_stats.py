# -*- coding: utf-8 -*-
"""The published numbers must come out of the shipped evidence pack unchanged."""
import json
import re
import subprocess
import sys

import pytest

from crisis_rehearsal import stats


def test_headline_matches_published(stats_result):
    result = stats_result
    assert result["published_match"] is True
    hit = result["hit"]
    assert round(hit["rate_pct"], 1) == 82.2
    assert [round(value, 1) for value in hit["ci_t_pct"]] == [78.5, 85.9]
    assert [round(value, 1) for value in hit["ci_bootstrap_pct"]] == [78.7, 85.6]
    assert round(hit["mean_score"], 2) == 2.47
    assert hit["df"] == 29


def test_statistical_unit_is_the_event(stats_result):
    result = stats_result
    assert result["n_events"] == 30
    assert result["n_runs"] == 90
    assert result["runs_per_event_min"] == result["runs_per_event_max"] == 3
    assert len(result["per_event"]) == 30
    for per_event in result["per_event"].values():
        assert per_event["n_runs"] == 3
        assert len(per_event["scores"]) == 3


def test_variance_numbers(stats_result):
    variance = stats_result["variance"]
    assert round(variance["within_sd"], 2) == 0.26
    assert round(variance["within_sd_median"], 2) == 0.24
    assert round(variance["between_sd"], 2) == 0.30
    assert stats_result["identical"]["n"] == 5
    assert stats_result["identical"]["of"] == 30
    assert round(stats_result["identical"]["pct"]) == 17
    assert stats_result["unstable"]["ids"] == [21, 23]
    assert stats_result["perfect"]["all_runs"] == 0
    assert stats_result["perfect"]["any_run"] == 14
    assert stats_result["perfect"]["runs"] == 21


def test_paired_replication_against_v01(stats_result):
    paired = stats_result["paired_v01"]
    assert paired is not None and paired["n_events"] == 30
    assert round(paired["diff_per_3"], 2) == -0.02
    assert round(paired["half_per_3"], 2) == 0.18


def test_early_warning(stats_result):
    early = stats_result["early_warning"]
    assert round(early["mean"]) == 78
    assert round(early["lo"]) == 75
    assert round(early["hi"]) == 81


def test_sta_is_fifty_eight_and_fails(stats_result):
    sta = stats_result["sta"]
    assert round(sta["batch"]) == 58
    assert sta["verdict"] == "FAILED"
    assert sta["pass_line"] == 60
    assert sta["funding_line"] == 75
    assert round(sta["jbar"], 2) == 0.54
    assert round(sta["cvbar"], 2) == 0.08
    assert round(sta["w"], 2) == 0.29
    assert "LLM semantic merge" in sta["item_merge"]


@pytest.mark.parametrize("event_id,expected", [
    ("6", {"mean": 2.0, "scores": [1.5, 2.0, 2.5], "sta": 34}),
    ("8", {"mean": 2.0, "scores": [2.0, 2.0, 2.0], "sta": 46}),
    ("23", {"mean": 1.8333, "scores": [1.0, 2.0, 2.5], "sta": 51}),
    ("21", {"mean": 2.3333, "scores": [1.5, 3.0, 2.5], "sta": 63}),
])
def test_per_event_spot_checks(stats_result, event_id, expected):
    per_event = stats_result["per_event"][event_id]
    assert [round(score, 1) for score in per_event["scores"]] == expected["scores"]
    assert round(per_event["mean"], 4) == pytest.approx(expected["mean"], abs=1e-3)
    assert round(per_event["sta"]["value"]) == expected["sta"]


def test_event_8_score_stable_content_unstable(stats_result):
    per_event = stats_result["per_event"]["8"]
    assert per_event["sd"] == 0.0
    assert round(per_event["sta"]["d"], 2) == 0.60
    assert per_event["sta"]["disagreement"] is True


def test_per_event_hit_rates_use_graded_scores(stats_result):
    per_event = stats_result["per_event"]["6"]
    assert round(per_event["hit_rate_pct"], 1) == 66.7
    per_event = stats_result["per_event"]["23"]
    assert round(per_event["sd"], 2) == 0.62


def test_recomputes_the_published_scripts(repo, stats_result):
    """Run scripts/ci_stats.py + scripts/sta_stats.py and compare their output."""
    ci = subprocess.run(
        [sys.executable, str(repo / "scripts" / "ci_stats.py"), "--no-md"],
        cwd=str(repo), capture_output=True, text=True, encoding="utf-8")
    assert ci.returncode == 0, ci.stderr
    sta = subprocess.run(
        [sys.executable, str(repo / "scripts" / "sta_stats.py"), "--no-md"],
        cwd=str(repo), capture_output=True, text=True, encoding="utf-8")
    assert sta.returncode == 0, sta.stderr

    hit = stats_result["hit"]
    variance = stats_result["variance"]
    stability = stats_result["sta"]

    def expect(pattern, text, label):
        match = re.search(pattern, text)
        assert match, f"{label}: pattern not found in script output"
        return match.group(1)

    assert expect(r"Top-3 risk hit rate.*?\*\*([\d.]+)%\*\*", ci.stdout, "hit rate") == \
        f"{hit['rate_pct']:.1f}"
    assert "t, df=29" in ci.stdout
    assert expect(r"\| ([\d.]+)-([\d.]+)% \(t, df=29\)", ci.stdout, "t ci") == \
        f"{hit['ci_t_pct'][0]:.1f}"
    ci_high = re.search(r"\| ([\d.]+)-([\d.]+)% \(t, df=29\)", ci.stdout).group(2)
    assert ci_high == f"{hit['ci_t_pct'][1]:.1f}"
    boot = re.search(r"bootstrap \| [\d.]+% \| ([\d.]+)-([\d.]+)%", ci.stdout)
    assert boot and boot.group(1) == f"{hit['ci_bootstrap_pct'][0]:.1f}"
    assert boot.group(2) == f"{hit['ci_bootstrap_pct'][1]:.1f}"
    assert expect(r"Within-event SD \(mean\) \| ([\d.]+)/3", ci.stdout, "within sd") == \
        f"{variance['within_sd']:.2f}"
    assert expect(r"Events identical in every run \| (\d+)/30", ci.stdout, "identical") == \
        str(stats_result["identical"]["n"])

    assert expect(r"\*\*STA\*\* \| \*\*(\d+)\*\*", sta.stdout, "STA") == \
        f"{stability['batch']:.0f}"
    assert expect(r"J-bar item agreement \| ([\d.]+)", sta.stdout, "jbar") == \
        f"{stability['jbar']:.2f}"
    assert expect(r"CV-bar coefficient of variation \| ([\d.]+)", sta.stdout, "cvbar") == \
        f"{stability['cvbar']:.2f}"
    assert expect(r"W rank agreement \| ([\d.]+)", sta.stdout, "kendall w") == \
        f"{stability['w']:.2f}"


def test_json_is_machine_readable(stats_result):
    payload = stats.as_json(stats_result)
    parsed = json.loads(payload)
    for key in ("n_events", "n_runs", "hit", "variance", "sta", "per_event",
                "published_check", "published_match"):
        assert key in parsed
    assert json.loads(json.dumps(parsed)) == parsed
    assert parsed["per_event"]["1"]["name"]


def test_text_report_contains_the_discipline(stats_result):
    text = stats.as_text(stats_result)
    assert "82.2%" in text
    assert "78.5% - 85.9%" in text or "78.5%" in text
    assert "STA 58" in text
    assert "EVENT-MEAN GRADED SCORE" in text
    assert "NOT 90 independent samples" in text
    assert "directional" in text.lower() or "DIRECTIONAL EVIDENCE" in text
    assert "Published-number check" in text
