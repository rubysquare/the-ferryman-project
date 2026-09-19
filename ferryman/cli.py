"""
The Ferryman Project — Command Line Interface
Provides the terminal interface and parses flags for voice, windowing,
and crossing dispatch.
"""

import sys
import os
import signal
from typing import List, Optional, Tuple
from datetime import datetime

from ferryman.types import SpeechConfig
from ferryman.window import is_in_window
from ferryman.storage import load_log, clear_log, get_log_path
from ferryman.crossings import (
    CrossingContext,
    run_dawn_anchor,
    run_midday_pause,
    run_dusk_release,
    run_circuit_breaker
)
from ferryman.voice import get_voice_engine

VERSION = "0.2.0"


def get_prog_name() -> str:
    """Returns the appropriate command name based on invocation."""
    if not sys.argv or not sys.argv[0]:
        return "ferryman"
    base = os.path.basename(sys.argv[0])
    if base.endswith(".py"):
        if base == "__main__.py":
            return "python3 -m ferryman"
        return f"python3 {base}"
    return base


def get_help_text(prog: Optional[str] = None) -> str:
    """Constructs help text using the appropriate invocation name."""
    if prog is None:
        prog = get_prog_name()
    return f"""The Ferryman Project v{VERSION}
An open-source, anti-engagement lifeline for grounded consciousness.

Usage:
  {prog} [command] [options]

Commands:
  dawn, morning, anchor     90s morning somatic check + single intention
  pause, sos, knot, midday  30s somatic circuit-breaker (grounding)
  dusk, night, release      3m evening unburdening of mental baggage
  tips, chat, ask, help     Anti-binge circuit-breaker test
  status, log               View your local private crossing log
  clear-log                 Wipe your local log (data sovereignty)

Options:
  --voice                   Speak aloud with offline system voice (say / spd-say / espeak)
  --window HH:MM-HH:MM      Run only if current time is within this interval (silent otherwise)
  --rate WPM                Speech rate in words per minute (default: 160)
  --fast                    Disable character-by-character typing delay
  --version                 Display version information
  -h, --help                Show this help message
"""


HELP_TEXT = get_help_text("ferryman")


def setup_signal_handlers() -> None:
    """Configures graceful exit on interrupt signals (Ctrl+C)."""
    def sigint_handler(signum: int, frame: object) -> None:
        try:
            sys.stdout.write("\nWalk in peace.\n")
            sys.stdout.flush()
        except (AttributeError, ValueError):
            pass
        sys.exit(0)

    try:
        signal.signal(signal.SIGINT, sigint_handler)
    except (ValueError, AttributeError):
        pass


def show_log_status() -> None:
    """Displays stored reflection entries without gamification or streaks."""
    entries = load_log()
    path = get_log_path()
    print(f"\n[Ferryman Private Log: {path}]")
    print(f"Total Crossings Recorded: {len(entries)} (No streaks, no points, no guilt)\n")
    if not entries:
        print("Your log is empty. Every day is a fresh river.")
        return

    # Show up to last 10 entries
    recent = entries[-10:]
    for e in recent:
        ts = e.get("timestamp", "")
        # Format timestamp nicely if possible
        try:
            dt = datetime.fromisoformat(ts)
            formatted_ts = dt.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            formatted_ts = ts
        c_type = e.get("type", "").upper()
        content = e.get("content", "")
        print(f"[{formatted_ts}] {c_type}: {content}")
    print()


def handle_clear_log() -> None:
    """Wipes the local log file."""
    count = clear_log()
    print(f"\nLocal log wiped clean ({count} entries removed). Your reflections belong only to you.\n")


def parse_args(argv: List[str]) -> Tuple[List[str], bool, int, bool, Optional[str]]:
    """Parses command line arguments and flags."""
    raw_args = list(argv)
    voice = False
    rate = 160
    fast = False
    window: Optional[str] = None
    args: List[str] = []

    i = 0
    while i < len(raw_args):
        arg = raw_args[i]
        if arg in ("--fast", "--no-delay"):
            fast = True
        elif arg == "--voice":
            voice = True
        elif arg == "--rate":
            if i + 1 < len(raw_args):
                i += 1
                try:
                    parsed_rate = int(raw_args[i])
                    if 20 <= parsed_rate <= 600:
                        rate = parsed_rate
                except ValueError:
                    pass
        elif arg.startswith("--rate="):
            try:
                parsed_rate = int(arg.split("=", 1)[1])
                if 20 <= parsed_rate <= 600:
                    rate = parsed_rate
            except ValueError:
                pass
        elif arg == "--window":
            if i + 1 < len(raw_args):
                i += 1
                window = raw_args[i]
        elif arg.startswith("--window="):
            window = arg.split("=", 1)[1]
        else:
            args.append(arg)
        i += 1

    if os.environ.get("FERRYMAN_VOICE") == "1":
        voice = True

    return args, voice, rate, fast, window



def main(argv: Optional[List[str]] = None) -> int:
    """Main CLI entrypoint."""
    setup_signal_handlers()

    if argv is None:
        argv = sys.argv[1:]

    args, voice_flag, rate, fast_flag, window = parse_args(argv)

    # Check window restriction if specified (e.g. from launchd or cron)
    if window:
        if not is_in_window(window):
            # Outside window: exit silently as intended
            return 0

    # Help and version flags
    if "-h" in args or "--help" in args:
        print(get_help_text())
        return 0

    if "--version" in args:
        print(f"The Ferryman Project v{VERSION}")
        return 0

    if "--status" in args or "status" in args or "--log" in args or "log" in args:
        show_log_status()
        return 0

    if "--clear-log" in args or "clear-log" in args:
        handle_clear_log()
        return 0

    # Initialize Crossing Context
    engine = get_voice_engine() if voice_flag else None
    ctx = CrossingContext(
        voice_enabled=voice_flag,
        voice_rate=rate,
        fast_mode=fast_flag,
        engine=engine
    )

    if args:
        cmd = args[0].lower()
        if cmd in ("dawn", "morning", "anchor"):
            run_dawn_anchor(ctx)
            return 0
        elif cmd in ("pause", "sos", "knot", "midday"):
            run_midday_pause(ctx)
            return 0
        elif cmd in ("dusk", "night", "release", "evening"):
            run_dusk_release(ctx)
            return 0
        elif cmd in ("chat", "ask", "help", "tips", "breaker"):
            run_circuit_breaker(ctx)
            return 0
        else:
            print(f"Unknown crossing '{cmd}'. Type '{get_prog_name()} --help' for available commands.")
            return 1

    # No command supplied: display interactive menu
    ctx.clear_screen()
    print("THE FERRYMAN PROJECT")
    print("An open-source lifeline for grounded presence.")
    print("=" * 45)
    print("1. Dawn Anchor   (90s morning orientation)")
    print("2. Midday Pause  (30s somatic circuit-breaker)")
    print("3. Dusk Release  (3m evening unburdening)")
    print("4. Ask for Tips  (Test the anti-binge rule)")
    print("q. Walk Away")
    print("=" * 45)

    try:
        if not sys.stdin.isatty():
            # If non-interactive stdin, don't block or crash
            print("\nStep away and breathe. The river awaits.")
            return 0
        choice = input("\nChoose your crossing [1-4, q]: ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nWalk in peace.")
        return 0

    if choice == "1":
        run_dawn_anchor(ctx)
    elif choice == "2":
        run_midday_pause(ctx)
    elif choice == "3":
        run_dusk_release(ctx)
    elif choice == "4":
        run_circuit_breaker(ctx)
    else:
        print("\nStep away and breathe. The river awaits.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
