# -*- coding: utf-8 -*-
"""Crisis Rehearsal Engine — offline evidence workstation (``crh``).

This package is the v0.3.0 product surface around the public 30-event crisis
backtest that ships in this repository. It is **standard library only** and
works with Python >= 3.9, so it can run on an air-gapped workstation:

    crh verify      # sha256 integrity of the shipped evidence pack
    crh stats       # recompute the published numbers (82.2%, STA 58, ...)
    crh report      # self-contained HTML rehearsal dossier for one event
    crh demo        # one command: verify + stats + 4 dossiers + index, < 10 s
    crh pack        # scenario-pack scaffolding + validation
    crh site        # static dossier site for all 30 events

What this package does **not** do: it does not simulate a crisis and it does not
judge a report. That is the MiroFish + LLM pipeline described in
``docs/methodology.md``, which needs a running engine and an API key. Everything
here reads the artifacts that pipeline already produced.
"""

__version__ = "0.3.0"
__all__ = ["__version__"]
