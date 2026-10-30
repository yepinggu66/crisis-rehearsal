# -*- coding: utf-8 -*-
"""Load the v0.1/v0.2 reproduction scripts as modules (import, never modify).

``scripts/ci_stats.py`` and ``scripts/sta_stats.py`` are the published
reproduction path for every number in the README. Instead of copying their
formulas — a copy would silently drift — the CLI imports them from the checkout
and calls their functions. The files are opened read-only.

If the scripts are missing (for example a wheel installed without the sdist
payload) the CLI says so and points at ``--repo``; it never invents statistics.
"""
from __future__ import annotations

import importlib.util
import re
import sys
from functools import lru_cache
from pathlib import Path


class ScriptUnavailable(RuntimeError):
    """Raised when the v0.2 statistics scripts cannot be imported."""


def _load(name: str, path: Path):
    if not path.is_file():
        raise ScriptUnavailable(
            f"statistics script not found: {path}\n"
            "The evidence workstation imports scripts/ci_stats.py and "
            "scripts/sta_stats.py from the repository instead of duplicating "
            "their formulas. Use --repo to point at a full checkout."
        )
    module_name = "crh_scripts_" + re.sub(r"\W", "_", name)
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        raise ScriptUnavailable(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    # Register before exec so intra-script references behave like a normal import.
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=None)
def _ci_stats_cached(path_str: str):
    return _load("ci_stats", Path(path_str))


@lru_cache(maxsize=None)
def _sta_stats_cached(path_str: str):
    return _load("sta_stats", Path(path_str))


def ci_stats(repo: Path):
    """The imported scripts/ci_stats.py module of *repo*."""
    return _ci_stats_cached(str(Path(repo) / "scripts" / "ci_stats.py"))


def sta_stats(repo: Path):
    """The imported scripts/sta_stats.py module of *repo*."""
    return _sta_stats_cached(str(Path(repo) / "scripts" / "sta_stats.py"))
