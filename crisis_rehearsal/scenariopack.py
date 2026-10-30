# -*- coding: utf-8 -*-
"""Scenario packs: scaffolding (``crh pack init``) and validation (``crh pack validate``).

A scenario pack is the portable input contract for a rehearsal: what the
organisation knows at T-72h, who matters, which regulatory hooks apply, who
decides what at which severity, which KPIs will be measured, what has already
been decided and which evidence backs it all.

Validation is a pure-standard-library JSON-Schema subset validator (no
``jsonschema`` dependency, because the CLI must install with zero third-party
packages). The schema is shipped twice — at ``schema/scenario_pack.schema.json``
for integrators and inside the package for installed wheels — and a test asserts
the two copies are byte-identical.
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import List, Optional, Tuple

SCHEMA_NAME = "scenario_pack.schema.json"
PACK_FILENAME = "scenario_pack.json"
SECTORS = ("enterprise", "government", "finance", "other")
CLASSIFICATIONS = ("public", "internal", "confidential", "restricted")

_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{1,63}$")

#: Keywords this validator understands. Anything else in the schema is ignored
#: (descriptions, titles, $id, $schema, $comment, ...).
_KNOWN = {
    "type", "properties", "required", "additionalProperties", "enum", "const",
    "pattern", "minLength", "maxLength", "minimum", "maximum", "minItems",
    "maxItems", "uniqueItems", "items", "description", "title", "$schema", "$id",
    "$comment", "default", "examples", "format",
}


class PackError(RuntimeError):
    """Raised when a pack cannot be read or the schema is unavailable."""


def schema_path(repo: Optional[Path] = None) -> Path:
    """Locate the schema: repository copy first, packaged copy as fallback."""
    if repo is not None:
        candidate = Path(repo) / "schema" / SCHEMA_NAME
        if candidate.is_file():
            return candidate
    packaged = Path(__file__).resolve().parent / "schema" / SCHEMA_NAME
    if packaged.is_file():
        return packaged
    raise PackError(
        f"scenario-pack schema not found (looked in {repo or '<repo>'}/schema and "
        f"{packaged}). Reinstall the package or pass --repo.")


def load_schema(repo: Optional[Path] = None) -> dict:
    path = schema_path(repo)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PackError(f"cannot read schema {path}: {exc}") from exc


# ---------------------------------------------------------------- validate --
def _type_name(value: object) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def _type_ok(value: object, wanted: object) -> bool:
    names = wanted if isinstance(wanted, list) else [wanted]
    for name in names:
        if name == "object" and isinstance(value, dict):
            return True
        if name == "array" and isinstance(value, list):
            return True
        if name == "string" and isinstance(value, str):
            return True
        if name == "boolean" and isinstance(value, bool):
            return True
        if name == "integer" and isinstance(value, int) and not isinstance(value, bool):
            return True
        if name == "number" and isinstance(value, (int, float)) and not isinstance(value, bool):
            return True
        if name == "null" and value is None:
            return True
    return False


def _join(path: str, key: object) -> str:
    if isinstance(key, int):
        return f"{path}[{key}]" if path else f"[{key}]"
    return f"{path}.{key}" if path else str(key)


def _validate(node: object, schema: dict, path: str, errors: List[str],
              root_schema: dict) -> None:
    if not isinstance(schema, dict):
        return
    if "$ref" in schema:  # not used by the shipped schema; fail loudly if it appears
        errors.append(f"{path or '(root)'}: $ref is not supported by this validator")
        return

    wanted = schema.get("type")
    if wanted is not None and not _type_ok(node, wanted):
        expected = wanted if isinstance(wanted, str) else " or ".join(wanted)
        errors.append(f"{path or '(root)'}: expected {expected}, got {_type_name(node)}")
        return

    if "const" in schema and node != schema["const"]:
        errors.append(f"{path or '(root)'}: must equal {schema['const']!r}")
    if "enum" in schema and node not in schema["enum"]:
        errors.append(f"{path or '(root)'}: {node!r} is not one of "
                      f"{schema['enum']!r}")

    if isinstance(node, str):
        if "pattern" in schema and not re.search(schema["pattern"], node):
            errors.append(f"{path or '(root)'}: {node!r} does not match pattern "
                          f"{schema['pattern']!r}")
        if "minLength" in schema and len(node) < schema["minLength"]:
            errors.append(f"{path or '(root)'}: shorter than {schema['minLength']} "
                          "character(s)")
        if "maxLength" in schema and len(node) > schema["maxLength"]:
            errors.append(f"{path or '(root)'}: longer than {schema['maxLength']} "
                          "character(s)")

    if isinstance(node, (int, float)) and not isinstance(node, bool):
        if "minimum" in schema and node < schema["minimum"]:
            errors.append(f"{path or '(root)'}: {node!r} is below the minimum "
                          f"{schema['minimum']!r}")
        if "maximum" in schema and node > schema["maximum"]:
            errors.append(f"{path or '(root)'}: {node!r} is above the maximum "
                          f"{schema['maximum']!r}")

    if isinstance(node, list):
        if "minItems" in schema and len(node) < schema["minItems"]:
            errors.append(f"{path or '(root)'}: must contain at least "
                          f"{schema['minItems']} item(s)")
        if "maxItems" in schema and len(node) > schema["maxItems"]:
            errors.append(f"{path or '(root)'}: must contain at most "
                          f"{schema['maxItems']} item(s)")
        if schema.get("uniqueItems"):
            seen: List[str] = []
            for item in node:
                marker = json.dumps(item, sort_keys=True, ensure_ascii=False)
                if marker in seen:
                    errors.append(f"{path or '(root)'}: duplicate item {marker!r}")
                seen.append(marker)
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(node):
                _validate(item, item_schema, _join(path, index), errors, root_schema)

    if isinstance(node, dict):
        properties = schema.get("properties") or {}
        for key in schema.get("required", []):
            if key not in node:
                errors.append(f"{_join(path, key)}: required field is missing")
        additional = schema.get("additionalProperties", True)
        for key, value in node.items():
            if key in properties:
                _validate(value, properties[key], _join(path, key), errors, root_schema)
            elif additional is False:
                errors.append(f"{_join(path, key)}: unknown field (additionalProperties "
                              "is false)")
            elif isinstance(additional, dict):
                _validate(value, additional, _join(path, key), errors, root_schema)


def validate_pack(data: object, schema: dict) -> List[str]:
    """Validate *data* against *schema*; returns a list of human-readable errors."""
    errors: List[str] = []
    _validate(data, schema, "", errors, schema)
    return errors


# ------------------------------------------------------------------ scaffold --
def skeleton(pack_id: str, name: str, sector: str = "enterprise",
             jurisdiction: str = "CN", classification: str = "internal",
             lang: str = "zh", created: Optional[str] = None) -> dict:
    """Build a valid, clearly-marked template pack.

    Every content field begins with ``[TEMPLATE]`` or ``TODO`` so a pack that was
    never filled in cannot be mistaken for a delivered case.
    """
    if not _ID_RE.match(str(pack_id)):
        raise PackError(
            f"invalid pack id {pack_id!r}: use 2-64 lower-case characters "
            "[a-z0-9._-] starting with a letter or digit")
    if sector not in SECTORS:
        raise PackError(f"invalid sector {sector!r}: choose one of {SECTORS}")
    if classification not in CLASSIFICATIONS:
        raise PackError(f"invalid classification {classification!r}: choose one of "
                        f"{CLASSIFICATIONS}")
    creator = created or date.today().isoformat()
    return {
        "pack_version": "0.3.0",
        "template": True,
        "meta": {
            "id": str(pack_id),
            "name": str(name),
            "sector": sector,
            "jurisdiction": jurisdiction,
            "classification": classification,
            "lang": lang,
            "owner": "TODO: team accountable for this pack",
            "updated": creator,
        },
        "timeline": {
            "T-72h": "[TEMPLATE] Public information available 72 hours before T0 only: "
                     "what the organisation, regulators, media and customers could "
                     "already see. No outcome, no penalty, no stock reaction.",
            "T-48h": "[TEMPLATE] Optional checkpoint: signals that became public.",
            "T-24h": "[TEMPLATE] Optional checkpoint: internal signals, draft "
                     "statements, pending disclosures.",
            "T0": "[TEMPLATE] The public trigger: the first public, attributable event.",
            "T+24h": "[TEMPLATE] Planned first-24h response: statement, escalation "
                     "level, owners.",
            "T+72h": "[TEMPLATE] Planned 72h posture: what has been said and decided.",
            "T+7d": "[TEMPLATE] Planned one-week review: what the team will assess.",
        },
        "stakeholders": [
            {
                "role": "[TEMPLATE] Corporate spokesperson / 新闻发言人",
                "kind": "internal",
                "influence": 5,
                "stance": "[TEMPLATE] describes the expected or observed stance",
                "interests": ["[TEMPLATE] interest 1", "[TEMPLATE] interest 2"],
            },
            {
                "role": "[TEMPLATE] Primary regulator / 行业主管部门",
                "kind": "regulator",
                "influence": 5,
                "stance": "[TEMPLATE] describe how the regulator is likely to react",
                "interests": ["[TEMPLATE] mandate the regulator is protecting"],
            },
        ],
        "regulatory_triggers": [
            {
                "framework": "TODO: name the law, regulation or standard that applies",
                "jurisdiction": jurisdiction,
                "requirement": "TODO: what the framework requires in plain language",
                "status": "unverified",
                "evidence": "TODO: where the mapping is documented (not a certificate)",
            },
        ],
        "escalation_ladder": [
            {
                "level": 1,
                "trigger": "[TEMPLATE] an observable condition (e.g. one media outlet "
                           "reports the issue)",
                "owner": "TODO: role, not name",
                "action": "[TEMPLATE] what happens at this level",
                "sla_hours": 24,
            },
            {
                "level": 2,
                "trigger": "[TEMPLATE] the crisis crosses a threshold",
                "owner": "TODO: role, not name",
                "action": "[TEMPLATE] what happens at this level",
                "sla_hours": 4,
            },
            {
                "level": 3,
                "trigger": "[TEMPLATE] regulator or board involvement",
                "owner": "TODO: role, not name",
                "action": "[TEMPLATE] what happens at this level",
                "sla_hours": 1,
            },
        ],
        "kpis": [
            {
                "id": "time_to_first_statement",
                "name": "[TEMPLATE] Time to the first public statement",
                "target": "<= 4",
                "unit": "hours",
                "window": "from T0",
                "source": "TODO: which system or report holds this number",
            },
            {
                "id": "stakeholder_alignment",
                "name": "[TEMPLATE] Stakeholders briefed before the statement",
                "target": "100",
                "unit": "%",
                "window": "before the first statement",
                "source": "TODO: attendance or sign-off record",
            },
            {
                "id": "decision_latency",
                "name": "[TEMPLATE] Median decision latency inside the ladder",
                "target": "<= 2",
                "unit": "hours",
                "source": "TODO: decision log",
            },
        ],
        "decision_log": [],
        "evidence": [],
        "provenance": {
            "author": "TODO: pack owner",
            "created": creator,
            "source": "TODO: public sources only, or state the internal source and "
                      "classification",
            "license": "TODO: e.g. CC-BY-4.0 or internal-only",
            "notes": "TEMPLATE generated by `crh pack init`. Replace every placeholder "
                     "before running a rehearsal; a template is a scaffold, not evidence.",
        },
    }


def write_pack(pack: dict, out: Path, force: bool = False) -> Path:
    """Write a pack as UTF-8 JSON; refuses to overwrite unless *force*.

    *out* may be a ``.json`` file path or a directory (existing or not); a
    non-``.json`` path is treated as a directory and the pack is written as
    ``scenario_pack.json`` inside it.
    """
    target = Path(out)
    if target.suffix.lower() != ".json":
        target = target / PACK_FILENAME
    if target.exists() and not force:
        raise PackError(f"refusing to overwrite existing pack: {target} "
                        "(use --force)")
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        text = json.dumps(pack, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
        with open(str(target), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
    except OSError as exc:
        raise PackError(f"cannot write {target}: {exc}") from exc
    return target


def read_pack(path: Path) -> Tuple[dict, Path]:
    """Read a pack from a file or a directory that contains one."""
    target = Path(path).expanduser()
    if target.is_dir():
        for name in (PACK_FILENAME, f"{target.name}.json"):
            candidate = target / name
            if candidate.is_file():
                target = candidate
                break
        else:
            candidates = sorted(target.glob("*.json"))
            if len(candidates) == 1:
                target = candidates[0]
            else:
                raise PackError(
                    f"no scenario pack found in {target}: expected "
                    f"{PACK_FILENAME} or exactly one .json file")
    if not target.is_file():
        raise PackError(f"scenario pack not found: {target}")
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise PackError(f"not valid JSON: {target}: {exc}") from exc
    except OSError as exc:
        raise PackError(f"cannot read {target}: {exc}") from exc
    if not isinstance(data, dict):
        raise PackError(f"the top level of a scenario pack must be an object: {target}")
    return data, target


def validate_file(path: Path, repo: Optional[Path] = None) -> Tuple[dict, Path, List[str], Path]:
    """Read + validate one pack. Returns (data, pack path, errors, schema path)."""
    data, resolved = read_pack(path)
    schema = load_schema(repo)
    errors = validate_pack(data, schema)
    return data, resolved, errors, schema_path(repo)


def summary_line(pack: dict) -> str:
    """One-line description of a pack, for CLI output."""
    meta = pack.get("meta") or {}
    counts = [
        f"{len(pack.get('stakeholders') or [])} stakeholders",
        f"{len(pack.get('regulatory_triggers') or [])} regulatory triggers",
        f"{len(pack.get('escalation_ladder') or [])} escalation levels",
        f"{len(pack.get('kpis') or [])} KPIs",
        f"{len(pack.get('evidence') or [])} evidence files",
    ]
    template = "TEMPLATE (not a delivered case)" if pack.get("template") else "filled pack"
    return (f"{meta.get('id', '?')} · {meta.get('name', '?')} · "
            f"{meta.get('sector', '?')} · {template} · " + ", ".join(counts))
