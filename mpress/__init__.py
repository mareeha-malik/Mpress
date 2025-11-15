"""Compatibility shim: make `import mpress` work when the project
is nested under the `MPress/` directory (case mismatch between dev and
deploy environments).

This shim makes the top-level `mpress` package point to the actual
package directory at `MPress/mpress` when present. This ensures
`import mpress.settings` and `mpress.wsgi` resolve correctly inside
containers where the repository layout may differ.
"""
from pathlib import Path
import sys
import os

# If the nested package exists at <repo root>/MPress/mpress, point
# this package's __path__ there so submodule imports work normally.
_root = Path(__file__).resolve().parent
_candidate = _root.parent / 'MPress' / 'mpress'
if _candidate.exists():
    __path__ = [str(_candidate)]

# Register module name in sys.modules (no-op if already present)
sys.modules.setdefault('mpress', sys.modules.get(__name__))
# Compatibility shim so imports for both `MPress` and `mpress` work
# This file intentionally left minimal.
