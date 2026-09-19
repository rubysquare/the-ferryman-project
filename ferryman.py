#!/usr/bin/env python3
"""
The Ferryman Project — Core Engine
An open-source, anti-engagement lifeline for grounded consciousness.
"""

import sys
import os

# Ensure the repository root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ferryman.cli import main, VERSION
from ferryman.storage import (
    load_log,
    save_entry,
    clear_log,
    get_log_path,
    DEFAULT_LOG_PATH
)
from ferryman.window import is_in_window
from ferryman.crossings import (
    CrossingContext,
    run_dawn_anchor,
    run_midday_pause,
    run_dusk_release,
    run_circuit_breaker
)
from ferryman.voice import get_voice_engine

# Backwards-compatibility aliases
DATA_FILE = DEFAULT_LOG_PATH


def in_window(window: str) -> bool:
    """Backwards compatibility for time window check."""
    return is_in_window(window)


def dawn_anchor() -> None:
    """Backwards compatibility runner for Dawn Anchor."""
    ctx = CrossingContext(fast_mode=False)
    run_dawn_anchor(ctx)


def midday_pause() -> None:
    """Backwards compatibility runner for Midday Pause."""
    ctx = CrossingContext(fast_mode=False)
    run_midday_pause(ctx)


def dusk_release() -> None:
    """Backwards compatibility runner for Dusk Release."""
    ctx = CrossingContext(fast_mode=False)
    run_dusk_release(ctx)


def circuit_breaker() -> None:
    """Backwards compatibility runner for Circuit Breaker."""
    ctx = CrossingContext(fast_mode=False)
    run_circuit_breaker(ctx)


if __name__ == "__main__":
    sys.exit(main())
