"""
Global Geopolitical War Room - Vercel Serverless Entrypoint
This module serves as the ASGI entrypoint for Vercel's Python runtime.
Vercel expects the FastAPI/ASGI app at api/index.py exported as `app`.
"""

import sys
import os
from pathlib import Path

# ─── Path bootstrap: ensure project root is on sys.path ──────────────────────
# Vercel places api/index.py in /var/task/api/ — we need /var/task on the path
# so that `from backend.xxx import yyy` works correctly.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ─── Re-export the FastAPI application ───────────────────────────────────────
from backend.main import app  # noqa: F401, E402 — must come after sys.path fix

__all__ = ["app"]
