"""
The Ferryman Project — Type Definitions
Strict type contracts for all internal and external boundaries.
"""

from typing import Optional, List, Dict, Tuple, Any, Union, NamedTuple, Callable
import sys

if sys.version_info >= (3, 8):
    from typing import Literal, TypedDict
else:
    from typing_extensions import Literal, TypedDict  # type: ignore


CrossingType = Literal["dawn", "pause", "dusk", "breaker"]


class LogEntry(TypedDict):
    """Immutable record of a somatic or intentional crossing entry."""
    timestamp: str  # ISO 8601 UTC or local format
    type: str       # "dawn", "pause", "dusk"
    content: str    # Raw reflection or body sensation


class WindowSpec(NamedTuple):
    """Specification of an allowed execution time window."""
    start_hour: int
    start_minute: int
    end_hour: int
    end_minute: int
    wraps_midnight: bool


class SpeechConfig(NamedTuple):
    """Configuration for local voice synthesis."""
    rate: int           # Words per minute (e.g. 160 unhurried)
    voice_name: Optional[str] = None
    enabled: bool = False
