# -*- coding: utf-8 -*-
"""End-to-end: `crh demo` completeness and the packaged/offline contract.

These are the assertions a buyer would make in a first meeting: one command, no
network, no API key, under ten seconds, and the numbers on the page are the
published ones.
"""
import time
from pathlib import Path

import pytest

from crisis_rehearsal import cli, demo
from crisis_rehearsal.evidence import verify


def test_demo_returns_a_complete_summary(repo, tmp_path, capsys):
    started = time.perf_counter()
    assert cli.main(["demo", "--repo", str(repo), "--out", str(tmp_path)]) == 0
    wall = time.perf_counter() - started
    output = capsys.readouterr().out

    assert wall < 10.0
    assert "PASS" in output
    assert "82.2%" in output
    assert "78.5-85.9" in output
    assert "0.26/3" in output
    assert "5/30" in output
    assert "STA 58" in output
    assert "matches published README numbers: yes" in output

    files = sorted(path.name for path in tmp_path.iterdir())
    assert "index.html" in files
    assert [name for name in files if name.startswith("event-")] == [
        "event-1.html", "event-25.html", "event-28.html", "event-6.html"]


def test_demo_index_links_every_dossier(repo, tmp_path, capsys):
    assert cli.main(["demo", "--out", str(tmp_path)]) == 0
    capsys.readouterr()
    index = (tmp_path / "index.html").read_text(encoding="utf-8")
    for event_id in ("1", "6", "25", "28"):
        assert f'href="event-{event_id}.html"' in index
    assert "<script" not in index.lower()
    assert "no external" in index.lower() or "self-contained" in index.lower()


def test_demo_uses_machine_independent_paths(repo, tmp_path, capsys):
    """The archived transcript should not leak the maintainer's home directory."""
    if Path.cwd().resolve() != Path(repo).resolve():
        pytest.skip("relative-path demo output assumes the repository is the cwd")
    out = tmp_path / "demo_out"
    assert demo.run(repo=repo, out=out)["ok"] is True
    output = capsys.readouterr().out
    assert "repo      : ." in output
    assert "output    : " in output


def test_demo_does_not_write_into_the_repository(repo, tmp_path, capsys):
    before = verify(repo)
    assert demo.run(repo=repo, out=tmp_path / "demo")["ok"] is True
    capsys.readouterr()
    after = verify(repo)
    assert before["counts"] == after["counts"]
    assert after["ok"] is True


def test_demo_refuses_missing_manifest(tmp_path, capsys):
    fake = tmp_path / "repo"
    (fake / "data" / "repeat_v02").mkdir(parents=True)
    (fake / "data" / "events.csv").write_text("id\n", encoding="utf-8")
    (fake / "data" / "repeat_v02" / "scores.jsonl").write_text("", encoding="utf-8")
    assert cli.main(["demo", "--repo", str(fake), "--out", str(tmp_path / "out")]) == 1
    assert "FAILED" in capsys.readouterr().out
