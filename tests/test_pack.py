# -*- coding: utf-8 -*-
"""`crh pack init` / `crh pack validate`: scenario-pack schema and scaffolding."""
import json
from pathlib import Path

import pytest

from crisis_rehearsal import cli, scenariopack
from crisis_rehearsal.scenariopack import PackError


def test_schema_is_valid_json_and_copies_are_identical(repo):
    root_schema = repo / "schema" / "scenario_pack.schema.json"
    packaged_schema = repo / "crisis_rehearsal" / "schema" / "scenario_pack.schema.json"
    assert root_schema.is_file() and packaged_schema.is_file()
    assert root_schema.read_bytes() == packaged_schema.read_bytes()
    data = json.loads(root_schema.read_text(encoding="utf-8"))
    assert data["type"] == "object"
    for field in ("pack_version", "meta", "timeline", "stakeholders",
                  "regulatory_triggers", "escalation_ladder", "kpis",
                  "decision_log", "evidence", "provenance"):
        assert field in data["required"], field
        assert field in data["properties"], field
    for field in ("id", "name", "sector", "jurisdiction", "classification", "lang"):
        assert field in data["properties"]["meta"]["required"]


def test_example_pack_is_valid(repo, capsys):
    path = repo / "schema" / "examples" / "example_enterprise_pack.json"
    assert path.is_file()
    assert cli.main(["pack", "validate", str(path)]) == 0
    output = capsys.readouterr().out
    assert "VALID" in output
    assert "TEMPLATE (not a delivered case)" in output
    assert "template=true" in output


def test_init_writes_a_valid_pack(tmp_path, capsys):
    out = tmp_path / "packs"
    assert cli.main(["pack", "init", "--id", "acme-2026", "--name",
                     "ACME 2026 outage", "--sector", "government",
                     "--out", str(out)]) == 0
    target = out / "acme-2026.json"
    assert target.is_file()
    pack = json.loads(target.read_text(encoding="utf-8"))
    assert pack["template"] is True
    assert pack["meta"]["id"] == "acme-2026"
    assert pack["meta"]["sector"] == "government"
    assert pack["meta"]["classification"] == "internal"
    assert set(pack["timeline"]) >= {"T-72h", "T-24h", "T0", "T+24h", "T+7d"}
    assert len(pack["stakeholders"]) >= 1
    assert len(pack["escalation_ladder"]) >= 1
    assert len(pack["kpis"]) >= 1
    assert pack["decision_log"] == [] and pack["evidence"] == []
    assert "template=YES" not in capsys.readouterr().out  # printed as 'template: YES'
    assert cli.main(["pack", "validate", str(target)]) == 0


def test_init_refuses_to_overwrite(tmp_path, capsys):
    out = tmp_path / "packs"
    args = ["pack", "init", "--id", "dupe-1", "--name", "dupe", "--out", str(out)]
    assert cli.main(args) == 0
    capsys.readouterr()
    assert cli.main(args) == 2
    assert "refusing to overwrite" in capsys.readouterr().err
    assert cli.main(args + ["--force"]) == 0


@pytest.mark.parametrize("field,value,needle", [
    ("sector", "hospital", "meta.sector"),
    ("classification", "secret", "meta.classification"),
    ("jurisdiction", "", "meta.jurisdiction"),
    ("lang", "", "meta.lang"),
])
def test_meta_enum_and_length_errors(repo, tmp_path, capsys, field, value, needle):
    pack = scenariopack.skeleton("bad-pack-1", "bad pack")
    pack["meta"][field] = value
    target = tmp_path / "pack.json"
    target.write_text(json.dumps(pack, ensure_ascii=False), encoding="utf-8")
    assert cli.main(["pack", "validate", str(target)]) == 1
    output = capsys.readouterr().out
    assert "INVALID" in output
    assert needle in output


def test_missing_required_field_is_reported(repo, tmp_path, capsys):
    pack = scenariopack.skeleton("bad-pack-2", "bad pack")
    del pack["meta"]["id"]
    pack["stakeholders"] = []
    target = tmp_path / "pack.json"
    target.write_text(json.dumps(pack, ensure_ascii=False), encoding="utf-8")
    assert cli.main(["pack", "validate", str(target)]) == 1
    output = capsys.readouterr().out
    assert "meta.id: required field is missing" in output
    assert "stakeholders: must contain at least 1 item(s)" in output


def test_unknown_field_is_rejected(tmp_path, capsys):
    pack = scenariopack.skeleton("bad-pack-3", "bad pack")
    pack["surprise"] = True
    target = tmp_path / "pack.json"
    target.write_text(json.dumps(pack, ensure_ascii=False), encoding="utf-8")
    assert cli.main(["pack", "validate", str(target)]) == 1
    assert "unknown field" in capsys.readouterr().out


def test_bad_json_and_missing_file(tmp_path, capsys):
    target = tmp_path / "broken.json"
    target.write_text("{not json", encoding="utf-8")
    assert cli.main(["pack", "validate", str(target)]) == 2
    assert "not valid JSON" in capsys.readouterr().err
    assert cli.main(["pack", "validate", str(tmp_path / "nope.json")]) == 2
    assert "not found" in capsys.readouterr().err


def test_validate_accepts_a_directory(tmp_path, capsys):
    directory = tmp_path / "one-pack"
    payload = scenariopack.skeleton("dir-pack-1", "directory pack")
    (directory).mkdir()
    (directory / "scenario_pack.json").write_text(
        json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    assert cli.main(["pack", "validate", str(directory)]) == 0


def test_skeleton_rejects_bad_ids_and_sectors():
    with pytest.raises(PackError):
        scenariopack.skeleton("BAD ID", "name")
    with pytest.raises(PackError):
        scenariopack.skeleton("ok-id-1", "name", sector="hospital")


def test_template_field_is_required(tmp_path, capsys):
    pack = scenariopack.skeleton("bad-pack-4", "bad pack")
    del pack["template"]
    target = tmp_path / "pack.json"
    target.write_text(json.dumps(pack, ensure_ascii=False), encoding="utf-8")
    assert cli.main(["pack", "validate", str(target)]) == 1
    assert "template: required field is missing" in capsys.readouterr().out


def test_pack_without_action_exits_2(capsys):
    assert cli.main(["pack"]) == 2
    assert "usage: crh pack" in capsys.readouterr().err


def test_evidence_digest_rule(tmp_path, capsys):
    pack = scenariopack.skeleton("bad-pack-5", "bad pack")
    pack["evidence"] = [{"path": "a.md", "sha256": "NOT-A-DIGEST", "kind": "other"}]
    target = tmp_path / "pack.json"
    target.write_text(json.dumps(pack, ensure_ascii=False), encoding="utf-8")
    assert cli.main(["pack", "validate", str(target)]) == 1
    assert "evidence[0].sha256" in capsys.readouterr().out
