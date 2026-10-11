"""
Global Geopolitical War Room - Configuration Module
Handles system mode (mock vs live) and environment settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
dotenv_path = ROOT_DIR / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)
else:
    load_dotenv()


def get_war_room_mode() -> str:
    """
    Returns the active War Room operation mode ('mock' or 'live').
    Defaults to 'mock' if WAR_ROOM_MODE is unset or invalid.
    """
    mode = os.getenv("WAR_ROOM_MODE", "mock").strip().lower()
    if mode not in ("mock", "live"):
        return "mock"
    return mode


def is_mock_mode() -> bool:
    """
    Returns True if the application is running in Mock Mode.
    """
    return get_war_room_mode() == "mock"
