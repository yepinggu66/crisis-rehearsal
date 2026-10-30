# Crisis Rehearsal Engine — developer entry points.
#
# The CLI itself is standard library only. These targets are conveniences:
# they assume `python -m pip install -e ".[dev]"` has been run once (or that
# `crh` is on PATH from an editable install).

PYTHON ?= python
CRH ?= crh
OUT ?= demo_out

.PHONY: help install dev test verify stats demo report site check clean sdist pack-example

help:
	@echo "install       pip install -e .            (CLI, zero runtime dependencies)"
	@echo "dev           pip install -e \".[dev]\"    (adds pytest for the test suite)"
	@echo "test          pytest -q"
	@echo "verify        crh verify                  (sha256 integrity of data/)"
	@echo "stats         crh stats                   (recompute the published numbers)"
	@echo "demo          crh demo --out $(OUT)       (offline, <10 s, no API key)"
	@echo "report        crh report --event $(EVENT)  (EVENT=6 by default)"
	@echo "site          crh site                    (30-event static dossier site)"
	@echo "check         verify + stats + test"
	@echo "sdist         build a source distribution into dist/"
	@echo "clean         remove build, test and demo artifacts"

install:
	$(PYTHON) -m pip install -e .

dev:
	$(PYTHON) -m pip install -e ".[dev]"

test:
	$(PYTHON) -m pytest -q

verify:
	$(CRH) verify

stats:
	$(CRH) stats

EVENT ?= 6
report:
	$(CRH) report --event $(EVENT)

demo:
	$(CRH) demo --out $(OUT)

site:
	$(CRH) site --out site

check: verify stats test
	@echo "check: evidence OK, published numbers reproduce, tests green"

sdist:
	$(PYTHON) -m pip install --quiet build
	$(PYTHON) -m build --sdist

pack-example:
	$(CRH) pack validate schema/examples/example_enterprise_pack.json

clean:
	rm -rf build dist *.egg-info .pytest_cache htmlcov .coverage
	rm -rf demo_out reports site scenario_packs
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
