# -*- coding: utf-8 -*-
"""Allow ``python -m crisis_rehearsal`` as an equivalent of the ``crh`` command."""
from __future__ import annotations

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
