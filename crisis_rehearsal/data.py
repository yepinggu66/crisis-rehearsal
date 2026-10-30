# -*- coding: utf-8 -*-
"""Read-only access to the shipped evidence pack.

Every number the CLI prints comes from one of these files:

    data/events.csv                 30 public crises, sources and real outcomes
    data/seeds/{id}.md              T-72h information pack per event
    data/repeat_v02/scores.jsonl    90 judge records (30 events x 3 runs)
    data/repeat_v02/scores_v01.jsonl  v0.1 single-run baseline
    data/repeat_v02/item_clusters.json  LLM item merge used by STA
    docs/reports/{id}.md, data/reports/{id}.md  the four shipped reports

Nothing in this module writes. Mutating the evidence pack is what
``crh verify`` exists to detect.
"""
from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from .paths import EVENTS_CSV, SCORES_JSONL


class DataError(RuntimeError):
    """Raised when a required evidence file is missing or unreadable."""


@dataclass(frozen=True)
class Event:
    id: str
    event_name_en: str
    event_name_zh: str
    entity: str
    year: str
    date: str
    crisis_type: str
    trigger: str
    outcome: str
    penalty: str
    source_url: str
    predictability: str

    @property
    def title(self) -> str:
        """Chinese title when available, else the English one."""
        return self.event_name_zh or self.event_name_en

    def sources(self) -> List[str]:
        """Split the source column on the separators used in the CSV."""
        raw = self.source_url or ""
        parts = re.split(r"[；;]\s*", raw)
        return [p.strip() for p in parts if p.strip()]


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise DataError(f"cannot read {path}: {exc}") from exc


def load_events(repo: Path) -> Dict[str, Event]:
    """Parse data/events.csv. The file carries a UTF-8 BOM, hence utf-8-sig."""
    path = Path(repo) / EVENTS_CSV
    if not path.is_file():
        raise DataError(f"missing evidence file: {path}")
    events: Dict[str, Event] = {}
    try:
        with open(str(path), encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                clean = {(k or "").strip(): (v or "").strip() for k, v in row.items()}
                if not clean.get("id"):
                    continue
                event = Event(
                    id=clean["id"],
                    event_name_en=clean.get("event_name_en", ""),
                    event_name_zh=clean.get("event_name_zh", ""),
                    entity=clean.get("entity", ""),
                    year=clean.get("year", ""),
                    date=clean.get("date", ""),
                    crisis_type=clean.get("crisis_type", ""),
                    trigger=clean.get("trigger", ""),
                    outcome=clean.get("outcome", ""),
                    penalty=clean.get("penalty", ""),
                    source_url=clean.get("source_url", ""),
                    predictability=clean.get("predictability", ""),
                )
                events[event.id] = event
    except csv.Error as exc:
        raise DataError(f"cannot parse {path}: {exc}") from exc
    if not events:
        raise DataError(f"no events in {path}")
    return events


def event_ids(repo: Path) -> List[str]:
    """Sorted event ids as strings (numeric order when possible)."""
    return sorted(load_events(repo), key=_id_key)


def _id_key(value: str):
    try:
        return (0, int(value))
    except (TypeError, ValueError):
        return (1, str(value))


def seed_path(repo: Path, eid: str) -> Path:
    return Path(repo) / "data" / "seeds" / f"{eid}.md"


def load_seed(repo: Path, eid: str) -> Optional[str]:
    """The T-72h information pack for one event, or None when absent."""
    path = seed_path(repo, eid)
    if not path.is_file():
        return None
    return _read_text(path)


def load_scores(repo: Path) -> List[dict]:
    """All judge records (90 for the shipped pack), in file order."""
    path = Path(repo) / SCORES_JSONL
    if not path.is_file():
        raise DataError(f"missing evidence file: {path}")
    rows: List[dict] = []
    for line in _read_text(path).splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    if not rows:
        raise DataError(f"no judge records in {path}")
    return rows


def load_baseline_scores(repo: Path) -> List[dict]:
    """The v0.1 single-run baseline (30 records), or [] when not shipped."""
    path = Path(repo) / "data" / "repeat_v02" / "scores_v01.jsonl"
    if not path.is_file():
        return []
    rows: List[dict] = []
    for line in _read_text(path).splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def load_clusters(repo: Path) -> dict:
    """The LLM item merge that the STA metric depends on, or {} if absent."""
    path = Path(repo) / "data" / "repeat_v02" / "item_clusters.json"
    if not path.is_file():
        return {}
    try:
        return json.loads(_read_text(path))
    except json.JSONDecodeError as exc:
        raise DataError(f"cannot parse {path}: {exc}") from exc


def scores_for_event(rows: List[dict], eid: str) -> List[dict]:
    """Judge records of one event, sorted by run label."""
    def order(record):
        try:
            return (0, int(record.get("run")))
        except (TypeError, ValueError):
            return (1, str(record.get("run")))

    return sorted((r for r in rows if str(r.get("id")) == str(eid)), key=order)


def shipped_report_path(repo: Path, eid: str) -> Optional[Path]:
    """The verbatim rehearsal report shipped for this event, if any.

    Only events 1, 6, 25 and 28 ship a full report body (the v0.1 grid samples).
    The filter is written as a path probe on purpose: adding a report file is
    enough to make it appear, and no event can accidentally claim a body.
    """
    for candidate in (Path(repo) / "docs" / "reports" / f"{eid}.md",
                      Path(repo) / "data" / "reports" / f"{eid}.md"):
        if candidate.is_file():
            return candidate
    return None


_FAILURE_HEADING = re.compile(r"^##\s*#(\d+)\b")


def load_failure_note(repo: Path, eid: str) -> Optional[str]:
    """Post-mortem section for one event from data/failures.md, if published."""
    path = Path(repo) / "data" / "failures.md"
    if not path.is_file():
        return None
    lines = _read_text(path).splitlines()
    start = None
    for index, line in enumerate(lines):
        match = _FAILURE_HEADING.match(line)
        if match and match.group(1) == str(eid):
            start = index
            break
    if start is None:
        return None
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "\n".join(lines[start:end]).strip()
