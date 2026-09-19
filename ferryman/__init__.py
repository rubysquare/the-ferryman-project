"""
The Ferryman Project
An open-source, anti-engagement lifeline for grounded consciousness.
"""

from ferryman.types import LogEntry, CrossingType, WindowSpec, SpeechConfig
from ferryman.storage import load_log, save_entry, clear_log, get_log_path
from ferryman.window import parse_window, is_in_window
from ferryman.voice import get_voice_engine, clean_spoken_text
from ferryman.crossings import (
    CrossingContext,
    run_dawn_anchor,
    run_midday_pause,
    run_dusk_release,
    run_circuit_breaker
)
from ferryman.cli import main, VERSION

__version__ = VERSION

__all__ = [
    "LogEntry",
    "CrossingType",
    "WindowSpec",
    "SpeechConfig",
    "load_log",
    "save_entry",
    "clear_log",
    "get_log_path",
    "parse_window",
    "is_in_window",
    "get_voice_engine",
    "clean_spoken_text",
    "CrossingContext",
    "run_dawn_anchor",
    "run_midday_pause",
    "run_dusk_release",
    "run_circuit_breaker",
    "main",
    "__version__",
]
