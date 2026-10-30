# -*- coding: utf-8 -*-
"""Shared fixtures for the crisis-rehearsal test suite.

The suite runs against the real repository (the shipped evidence pack is part of
the package's contract) and against temporary throw-away repositories for the
tamper / scaffold tests. Nothing here writes into the checkout.
"""
import shutil
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from crisis_rehearsal.evidence import write_manifest  # noqa: E402


@pytest.fixture(scope="session")
def repo() -> Path:
    return REPO


@pytest.fixture(scope="session")
def stats_result(repo):
    from crisis_rehearsal.stats import compute

    return compute(repo)


@pytest.fixture(scope="session")
def context(repo, stats_result):
    from crisis_rehearsal.report import build_context

    return build_context(repo, stats_result=stats_result)


@pytest.fixture()
def mini_repo(tmp_path, repo) -> Path:
    """A throw-away copy of data/ with a freshly generated manifest."""
    target = tmp_path / "repo"
    shutil.copytree(repo / "data", target / "data")
    write_manifest(target)
    return target
