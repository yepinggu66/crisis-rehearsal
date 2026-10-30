# -*- coding: utf-8 -*-
"""CLI surface: version, exit codes, demo/site, packaging contract, docs asset."""
import ast
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from crisis_rehearsal import __version__, cli
from crisis_rehearsal.evidence import verify

STDLIB_FALLBACK = {
    "__future__", "argparse", "ast", "collections", "csv", "dataclasses",
    "datetime", "functools", "hashlib", "html", "importlib", "io", "itertools",
    "json", "math", "os", "pathlib", "re", "shutil", "statistics", "sys",
    "tempfile", "textwrap", "time", "typing", "unittest", "urllib", "uuid",
}


def test_version(capsys):
    with pytest.raises(SystemExit) as exit_info:
        cli.main(["--version"])
    assert exit_info.value.code == 0
    assert capsys.readouterr().out.strip() == f"crh {__version__}"


def test_version_is_single_sourced(repo):
    text = (repo / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version = "([^"]+)"', text, re.MULTILINE)
    assert match and match.group(1) == __version__


def test_no_args_prints_help(capsys):
    assert cli.main([]) == 0
    output = capsys.readouterr().out
    assert "usage: crh" in output
    assert "verify" in output and "stats" in output and "demo" in output


def test_python_dash_m_equivalent(repo):
    result = subprocess.run(
        [sys.executable, "-m", "crisis_rehearsal", "--version"],
        cwd=str(repo), capture_output=True, text=True, encoding="utf-8")
    assert result.returncode == 0
    assert result.stdout.strip() == f"crh {__version__}"


def test_stats_json_cli(repo, capsys):
    assert cli.main(["stats", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["n_events"] == 30
    assert payload["published_match"] is True
    assert round(payload["sta"]["batch"]) == 58
    assert round(payload["hit"]["ci_t_pct"][0], 1) == 78.5


def test_stats_with_fewer_resamples_is_explicit(repo, capsys):
    """A non-published resample count must be labelled, not silently substituted."""
    assert cli.main(["stats", "--json", "--bootstrap", "500"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["hit"]["bootstrap_resamples"] == 500
    assert round(payload["hit"]["ci_t_pct"][0], 1) == 78.5
    assert payload["hit"]["bootstrap_method"] in ("numpy", "stdlib fallback")
    bootstrap_rows = [row for row in payload["published_check"]
                      if row["metric"].startswith("ci_bootstrap")]
    assert len(bootstrap_rows) == 2
    assert all(isinstance(row["match"], bool) for row in bootstrap_rows)


def test_stats_text_cli(repo, capsys):
    assert cli.main(["stats"]) == 0
    output = capsys.readouterr().out
    assert "82.2%" in output
    assert "STA 58" in output
    assert "[OK  ]" in output


def test_stats_bad_repo_exits_2(tmp_path, capsys):
    assert cli.main(["stats", "--repo", str(tmp_path)]) == 2
    assert "not a crisis-rehearsal repository" in capsys.readouterr().err


def test_demo_cli(repo, tmp_path, capsys):
    out = tmp_path / "demo_out"
    assert cli.main(["demo", "--out", str(out)]) == 0
    output = capsys.readouterr().out
    assert "PASS" in output
    assert "82.2%" in output
    assert "STA 58" in output
    assert "no API key" in output
    assert "done in" in output
    # under ten seconds by contract
    match = re.search(r"done in ([\d.]+)s", output)
    assert match and float(match.group(1)) < 10.0
    for name in ("index.html", "event-1.html", "event-6.html", "event-25.html",
                 "event-28.html"):
        assert (out / name).is_file(), name
    index = (out / "index.html").read_text(encoding="utf-8")
    assert "82.2%" in index and "STA 58" in index
    assert "<script" not in index.lower()


def test_demo_refuses_a_tampered_pack(mini_repo, tmp_path, capsys):
    target = mini_repo / "data" / "repeat_v02" / "scores.jsonl"
    target.write_text(target.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    assert cli.main(["demo", "--repo", str(mini_repo), "--out", str(tmp_path)]) == 1
    output = capsys.readouterr().out
    assert "FAILED" in output
    assert "MODIFIED" in output


def test_site_cli(repo, tmp_path, capsys):
    out = tmp_path / "site"
    assert cli.main(["site", "--out", str(out)]) == 0
    pages = list(out.glob("event-*.html"))
    assert len(pages) == 30
    index = (out / "index.html").read_text(encoding="utf-8")
    assert "82.2%" in index
    assert 'href="event-1.html"' in index
    capsys.readouterr()


def test_commands_do_not_touch_the_evidence(repo, tmp_path, capsys):
    """stats / report / demo / site / pack must be read-only with respect to data/."""
    assert verify(repo)["ok"] is True
    assert cli.main(["stats", "--json", "--bootstrap", "100"]) == 0
    assert cli.main(["report", "--event", "6", "--out", str(tmp_path)]) == 0
    assert cli.main(["demo", "--out", str(tmp_path / "demo")]) == 0
    assert cli.main(["pack", "init", "--id", "readonly-check", "--name", "check",
                     "--out", str(tmp_path / "packs")]) == 0
    capsys.readouterr()
    result = verify(repo)
    assert result["ok"] is True, [row for row in result["rows"]
                                  if row["status"] != "OK"]


def test_packaging_contract(repo):
    text = (repo / "pyproject.toml").read_text(encoding="utf-8")
    assert 'name = "crisis-rehearsal"' in text
    assert 'requires-python = ">=3.9"' in text
    assert "dependencies = []" in text, "runtime dependencies must stay empty"
    assert 'crh = "crisis_rehearsal.cli:main"' in text
    assert 'crisis-rehearsal = "crisis_rehearsal.cli:main"' in text
    assert 'llm = ["httpx>=0.24"]' in text
    assert (repo / "MANIFEST.in").is_file()
    assert (repo / "crisis_rehearsal" / "schema" / "scenario_pack.schema.json").is_file()


def test_cli_is_standard_library_only(repo):
    allowed = set(getattr(sys, "stdlib_module_names", ())) | STDLIB_FALLBACK
    offenders = []
    for path in sorted((repo / "crisis_rehearsal").rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            modules = []
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0:
                modules = [node.module or ""]
            for module in modules:
                root = module.split(".")[0]
                if root and root != "crisis_rehearsal" and root not in allowed:
                    offenders.append(f"{path.name}: {module}")
    assert not offenders, f"non-stdlib imports: {offenders}"


def test_workflow_and_containers_exist_and_are_honest(repo):
    # The workflow is shipped as a ready-to-enable asset rather than under
    # .github/workflows/: publishing a workflow file needs the OAuth `workflow`
    # scope, which the release credential does not have. The test pins the
    # content so the file keeps working when someone enables it.
    workflow_path = repo / "docs" / "ci" / "github-actions.yml"
    assert workflow_path.exists()
    assert not (repo / ".github" / "workflows" / "ci.yml").exists()
    workflow = workflow_path.read_text(encoding="utf-8")
    assert "3.9" in workflow and "3.12" in workflow
    for command in ("crh verify", "crh stats", "crh demo"):
        assert command in workflow
    assert "sdist" in workflow or "dist" in workflow
    # the copy step must be documented in the file itself
    assert "cp docs/ci/github-actions.yml .github/workflows/ci.yml" in workflow

    dockerfile = (repo / "Dockerfile").read_text(encoding="utf-8")
    lowered = dockerfile.lower()
    assert "python:3.12-slim" in dockerfile
    assert "not the full mirofish" in lowered
    assert "user crh" in lowered

    compose = (repo / "docker-compose.yml").read_text(encoding="utf-8")
    assert "not the full MiroFish engine" in compose
    assert "证据工作站" in compose
    assert "read_only: true" in compose


def test_makefile_has_the_documented_targets(repo):
    text = (repo / "Makefile").read_text(encoding="utf-8")
    for target in ("install:", "test:", "verify:", "stats:", "demo:", "check:"):
        assert target in text


def test_docs_assets_cli_demo_transcript(repo):
    """The captured terminal transcript used by the README must be real output."""
    path = repo / "docs" / "assets" / "cli-demo.txt"
    assert path.is_file(), "docs/assets/cli-demo.txt is missing"
    text = path.read_text(encoding="utf-8")
    assert "Crisis Rehearsal Engine" in text
    assert "82.2%" in text
    assert "STA 58" in text
    assert "no API key" in text
    assert text.count("[1/4]") == 1

    image = repo / "docs" / "assets" / "cli-demo.png"
    assert image.is_file(), "docs/assets/cli-demo.png is missing"
    assert image.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def test_docs_cli_reference_exists(repo):
    path = repo / "docs" / "cli.md"
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    for command in ("crh verify", "crh stats", "crh report", "crh demo",
                    "crh pack init", "crh pack validate", "crh site"):
        assert command in text
    assert "Exit codes" in text or "exit code" in text.lower()
