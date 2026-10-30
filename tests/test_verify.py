# -*- coding: utf-8 -*-
"""`crh verify`: sha256 integrity of the shipped evidence pack."""
import shutil

from crisis_rehearsal import cli
from crisis_rehearsal.evidence import (MODIFIED, MISSING, OK, UNLISTED,
                                       build_manifest_text, data_files,
                                       manifest_path, verify, write_manifest)


def test_real_repository_passes(repo):
    result = verify(repo)
    assert result["manifest_present"] is True
    assert result["ok"] is True
    counts = result["counts"]
    assert counts[MODIFIED] == counts[MISSING] == counts[UNLISTED] == 0
    assert counts[OK] == len(data_files(repo)) == result["n_files"]
    assert all(row["status"] == OK for row in result["rows"])
    # Canonical hash of the LF-normalised blob (.gitattributes stores and checks
    # out every text file as LF, so this value is platform-independent). The v0.2
    # evidence pack recorded 562be6853fba6906 from a CRLF Windows checkout;
    # data/evidence.sha256 supersedes it (docs/cli.md §3 explains the difference).
    scores = repo / "data" / "repeat_v02" / "scores.jsonl"
    row = next(row for row in result["rows"]
               if row["path"].endswith("scores.jsonl"))
    assert row["actual"].startswith("0bfd42d4be1f16db")
    assert row["actual"] == __import__("hashlib").sha256(
        scores.read_bytes()).hexdigest()


def test_manifest_is_deterministic_and_excludes_itself(repo):
    first = build_manifest_text(repo)
    second = build_manifest_text(repo)
    assert first == second
    assert "data/evidence.sha256" not in first
    assert "data/events.csv" in first
    assert "data/repeat_v02/scores.jsonl" in first
    listed = [line for line in first.splitlines()
              if line and not line.startswith("#")]
    assert len(listed) == len(data_files(repo))
    # 30 seeds + events.csv + 4 data notes + 6 repeat_v02 files + 2 reports = 43
    assert len(listed) >= 43


def test_manifest_write_is_idempotent(mini_repo):
    before = manifest_path(mini_repo).read_bytes()
    write_manifest(mini_repo)
    assert manifest_path(mini_repo).read_bytes() == before


def test_modified_file_is_detected(mini_repo):
    target = mini_repo / "data" / "events.csv"
    target.write_bytes(target.read_bytes() + b"\n# tampered\n")
    result = verify(mini_repo)
    assert result["ok"] is False
    assert result["counts"][MODIFIED] == 1
    bad = next(row for row in result["rows"] if row["status"] == MODIFIED)
    assert bad["path"] == "data/events.csv"
    assert bad["expected"] != bad["actual"]


def test_missing_file_is_detected(mini_repo):
    (mini_repo / "data" / "seeds" / "7.md").unlink()
    result = verify(mini_repo)
    assert result["ok"] is False
    assert result["counts"][MISSING] == 1
    assert any(row["status"] == MISSING and row["path"] == "data/seeds/7.md"
               for row in result["rows"])


def test_unlisted_file_is_detected(mini_repo):
    (mini_repo / "data" / "extra.md").write_text("not in the manifest", encoding="utf-8")
    result = verify(mini_repo)
    assert result["ok"] is False
    assert result["counts"][UNLISTED] == 1
    assert any(row["status"] == UNLISTED and row["path"] == "data/extra.md"
               for row in result["rows"])


def test_missing_manifest_is_an_error(tmp_path):
    empty = tmp_path / "empty"
    (empty / "data").mkdir(parents=True)
    result = verify(empty)
    assert result["ok"] is False
    assert result["manifest_present"] is False
    assert "crh verify --write" in result["message"]


def test_cli_exit_codes(mini_repo, capsys):
    assert cli.main(["verify", "--repo", str(mini_repo), "--quiet"]) == 0
    capsys.readouterr()
    (mini_repo / "data" / "README.md").write_text("changed", encoding="utf-8")
    assert cli.main(["verify", "--repo", str(mini_repo), "--quiet"]) == 1
    assert "FAIL" in capsys.readouterr().out


def test_cli_write_roundtrip(mini_repo, capsys):
    target = mini_repo / "data" / "seeds" / "9.md"
    target.write_text(target.read_text(encoding="utf-8") + "\nextra\n",
                      encoding="utf-8")
    assert cli.main(["verify", "--repo", str(mini_repo), "--quiet"]) == 1
    capsys.readouterr()
    assert cli.main(["verify", "--repo", str(mini_repo), "--write",
                     "--quiet"]) == 0
    assert cli.main(["verify", "--repo", str(mini_repo), "--quiet"]) == 0


def test_repository_has_no_ignored_evidence(tmp_path, repo):
    """A copy without data/ must not be mistaken for a repository."""
    fake = tmp_path / "not-a-repo"
    fake.mkdir()
    shutil.copy(repo / "data" / "events.csv", fake / "events.csv")
    assert cli.main(["verify", "--repo", str(fake)]) == 2
