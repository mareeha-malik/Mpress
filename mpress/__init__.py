"""Compatibility shim: make `import mpress` work when the project
is nested under the `MPress/` directory (case mismatch between dev and
deploy environments).

This module imports the real package at `MPress.mpress` and re-exports
its attributes so `mpress.*` imports work regardless of filesystem layout.
"""
from importlib import import_module
import sys

try:
    _real = import_module('MPress.mpress')
except Exception:
    # Fall back to trying to import a top-level mpress package if present
    _real = import_module('mpress') if 'mpress' in sys.modules else None

if _real is not None:
    for _name in dir(_real):
        if _name.startswith('__'):
            continue
        globals()[_name] = getattr(_real, _name)

# Ensure this module is registered as 'mpress'
sys.modules['mpress'] = sys.modules.get('mpress', sys.modules[__name__])
# Compatibility shim so imports for both `MPress` and `mpress` work
# This file intentionally left minimal.
