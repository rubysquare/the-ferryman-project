"""
The Ferryman Project — Time Window Verification
Determines if the current moment falls within a specified crossing window.
Supports single-day intervals and overnight intervals wrapping past midnight.
"""

from datetime import datetime, time
from typing import Optional, Tuple
from ferryman.types import WindowSpec


def parse_window(window_str: str) -> WindowSpec:
    """
    Parses a window string formatted as 'HH:MM-HH:MM' into a WindowSpec.
    Raises ValueError if format or hours/minutes are invalid.
    """
    if not window_str or "-" not in window_str:
        raise ValueError(f"Window must be in 'HH:MM-HH:MM' format, got: '{window_str}'")

    parts = window_str.strip().split("-")
    if len(parts) != 2:
        raise ValueError(f"Window must have exactly one '-' separator, got: '{window_str}'")

    start_str, end_str = parts[0].strip(), parts[1].strip()

    try:
        start_t = datetime.strptime(start_str, "%H:%M").time()
        end_t = datetime.strptime(end_str, "%H:%M").time()
    except ValueError as e:
        raise ValueError(f"Invalid time format in window '{window_str}': {e}") from e

    start_minutes = start_t.hour * 60 + start_t.minute
    end_minutes = end_t.hour * 60 + end_t.minute
    wraps = start_minutes > end_minutes

    return WindowSpec(
        start_hour=start_t.hour,
        start_minute=start_t.minute,
        end_hour=end_t.hour,
        end_minute=end_t.minute,
        wraps_midnight=wraps
    )


def is_in_window(window_str: str, now: Optional[datetime] = None) -> bool:
    """
    Checks if `now` (or current local time if None) is within `window_str`.
    Returns False if window_str is invalid.
    """
    try:
        spec = parse_window(window_str)
    except ValueError:
        return False

    current_dt = now or datetime.now()
    cur_minutes = current_dt.hour * 60 + current_dt.minute

    start_minutes = spec.start_hour * 60 + spec.start_minute
    end_minutes = spec.end_hour * 60 + spec.end_minute

    if not spec.wraps_midnight:
        return start_minutes <= cur_minutes <= end_minutes
    else:
        # Wraps across midnight (e.g. 23:00 to 02:00)
        return cur_minutes >= start_minutes or cur_minutes <= end_minutes
