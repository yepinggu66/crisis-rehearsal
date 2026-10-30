# -*- coding: utf-8 -*-
"""Repository discovery and small path / hashing helpers.

The CLI can be used three ways:

* from a checkout: ``crh stats`` inside the repository works out of the box;
* from anywhere: ``crh stats --repo /path/to/crisis-rehearsal``;
* from a checkout mounted read-only in a container, with ``CR_ROOT`` set.

Discovery never writes anything. A directory qualifies as the repository when
``data/events.csv`` and ``data/repeat_v02/scores.jsonl`` are both present, so a
half-copied directory fails loudly instead of producing wrong numbers.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

EVENTS_CSV = Path("data") / "events.csv"
SCORES_JSONL = Path("data") / "repeat_v02" / "scores.jsonl"
MANIFEST_REL = Path("data") / "evidence.sha256"

_HINT = (
    "Point the CLI at the repository with --repo PATH, run it from the repository "
    "root, or set CR_ROOT."
)


class RepoNotFound(RuntimeError):
    """Raised when no usable crisis-rehearsal checkout can be located."""


def looks_like_repo(path: Path) -> bool:
    """True when *path* is a crisis-rehearsal checkout (evidence pack present)."""
    try:
        return (path / EVENTS_CSV).is_file() and (path / SCORES_JSONL).is_file()
    except OSError:
        return False


def find_repo(explicit: object = None) -> Path:
    """Locate the repository root.

    Search order: explicit ``--repo`` argument, ``$CR_ROOT``, current directory
    and its parents, then the package location and its parents (this is what
    makes an editable install work from any directory).
    """
    tried = []
    if explicit is not None and str(explicit).strip():
        base = Path(str(explicit)).expanduser().resolve()
        tried.append(base)
        if looks_like_repo(base):
            return base
        raise RepoNotFound(f"not a crisis-rehearsal repository: {base}\n{_HINT}")

    env = os.environ.get("CR_ROOT")
    if env:
        base = Path(env).expanduser().resolve()
        tried.append(base)
        if looks_like_repo(base):
            return base

    for start in (Path.cwd().resolve(), Path(__file__).resolve().parent):
        for base in (start, *start.parents):
            if base in tried:
                continue
            tried.append(base)
            if looks_like_repo(base):
                return base

    raise RepoNotFound(
        "could not find a crisis-rehearsal repository (looked for "
        f"{EVENTS_CSV.as_posix()} and {SCORES_JSONL.as_posix()}).\n{_HINT}"
    )


def rel(repo: Path, path: object) -> str:
    """Path as a repo-relative POSIX string when possible, else as given."""
    p = Path(str(path))
    try:
        return p.resolve().relative_to(Path(repo).resolve()).as_posix()
    except (ValueError, OSError):
        return p.as_posix()


def sha256_bytes(data: bytes) -> str:
    """Full sha256 hex digest (lower case)."""
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: object) -> str:
    """Full sha256 hex digest of a file.

    Returns ``"n/a"`` only for unreadable paths; callers display that string
    instead of pretending the file was verified.
    """
    try:
        h = hashlib.sha256()
        with open(str(path), "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return "n/a"


def sha256_prefix(path: object, length: int = 16) -> str:
    """Short digest, same convention as scripts/ci_stats.py (16 hex chars)."""
    digest = sha256_file(path)
    return digest if digest == "n/a" else digest[:length]


def write_text(path: object, text: str) -> Path:
    """Write UTF-8 text with LF endings, creating parent directories."""
    target = Path(str(path))
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(str(target), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return target


def iter_files(root: object) -> list:
    """All regular files under *root*, sorted by POSIX relative path."""
    base = Path(str(root))
    if not base.exists():
        return []
    out = []
    for path in base.rglob("*"):
        if path.is_file():
            out.append(path)
    return sorted(out, key=lambda p: p.relative_to(base).as_posix())
