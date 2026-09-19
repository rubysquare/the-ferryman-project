"""
The Ferryman Project — The Three Daily Crossings
Implements Dawn Anchor, Midday Pause (SOS), Dusk Release, and Circuit Breaker.
Supports interactive terminal mode and zero-screen headless voice mode.
"""

import sys
import time
from typing import Optional, Callable
from ferryman.types import SpeechConfig
from ferryman.storage import save_entry
from ferryman.voice import VoiceEngine, get_voice_engine
from ferryman.circuit_breaker import is_advice_seeking, get_boundary_message
from ferryman.somatic import (
    get_dawn_somatic_prompt,
    get_midday_grounding_steps,
    get_dusk_closing_prompt
)


class CrossingContext:
    """Encapsulates I/O and runtime configuration for a crossing."""

    def __init__(
        self,
        voice_enabled: bool = False,
        voice_rate: int = 160,
        fast_mode: bool = False,
        engine: Optional[VoiceEngine] = None,
        input_func: Optional[Callable[[str], str]] = None,
        print_func: Optional[Callable[[str], None]] = None,
        sleep_func: Optional[Callable[[float], None]] = None,
    ) -> None:
        self.voice_enabled = voice_enabled
        self.voice_rate = voice_rate
        self.fast_mode = fast_mode
        self.engine = engine or (get_voice_engine() if voice_enabled else None)
        self.input_func = input_func or input
        self.print_func = print_func or sys.stdout.write
        self.sleep_func = sleep_func or time.sleep

    def is_headless(self) -> bool:
        """Determines if the session is running headless (e.g. piped, launchd, Siri)."""
        # If stdin is not a TTY, or if voice is on without a TTY
        try:
            return not sys.stdin.isatty()
        except (AttributeError, ValueError):
            return True

    def clear_screen(self) -> None:
        """Clears terminal screen if connected to a valid TTY."""
        try:
            if sys.stdout.isatty():
                self.print_func("\033c")
        except (AttributeError, ValueError):
            pass

    def slow_print(self, text: str, delay: float = 0.02) -> None:
        """Prints text with an unhurried cadence and speaks if voice is enabled."""
        if self.voice_enabled and self.engine:
            self.print_func(text + "\n")
            self.engine.speak(text, self.voice_rate)
            return

        if self.fast_mode or delay <= 0:
            self.print_func(text + "\n")
            return

        for char in text:
            self.print_func(char)
            try:
                sys.stdout.flush()
            except (AttributeError, ValueError):
                pass
            self.sleep_func(delay)
        self.print_func("\n")

    def sleep(self, seconds: float) -> None:
        """Sleeps unless in fast mode."""
        if not self.fast_mode:
            self.sleep_func(seconds)


def run_dawn_anchor(ctx: CrossingContext) -> None:
    """Dawn Anchor: 90-second morning somatic check + single intention."""
    ctx.clear_screen()
    ctx.slow_print("\n=== THE DAWN ANCHOR ===")
    for prompt in get_dawn_somatic_prompt():
        ctx.slow_print(prompt)
        ctx.sleep(1.2)

    ctx.slow_print("\nWhat is the single most essential thing you must honor today?")

    if ctx.is_headless():
        ctx.sleep(20.0 if not ctx.fast_mode else 0.0)
        ctx.slow_print("Carry it lightly as you cross the river today.")
        ctx.slow_print("\nNow step away from screens, and enter your morning.\n")
        return

    try:
        ctx.print_func("\n> ")
        sys.stdout.flush()
        raw = ctx.input_func("").strip()
    except (KeyboardInterrupt, EOFError):
        ctx.print_func("\nTake care.\n")
        return

    if is_advice_seeking(raw):
        run_circuit_breaker(ctx)
        return

    if raw:
        save_entry("dawn", raw)
        ctx.print_func("\n")
        ctx.slow_print(f"Understood. Carry '{raw}' lightly as you cross the river today.")
    else:
        ctx.slow_print("Silence is also an answer. Walk gently today.")

    ctx.sleep(1.0)
    ctx.slow_print("\nNow close your terminal, step away from screens, and enter your morning.\n")


def run_midday_pause(ctx: CrossingContext) -> None:
    """Midday Pause / SOS: 30-second somatic reset to break the mental loop."""
    ctx.clear_screen()
    ctx.slow_print("\n=== THE MIDDAY PAUSE (SOS) ===")
    steps = get_midday_grounding_steps()
    for step in steps:
        ctx.slow_print(step)
        ctx.sleep(1.2)

    if ctx.is_headless():
        ctx.sleep(5.0 if not ctx.fast_mode else 0.0)
        ctx.slow_print("\nYou are back on solid ground. Return to your task one breath at a time.\n")
        return

    try:
        ctx.print_func("\nIn one word or phrase, what sensation is present in your body right now?\n> ")
        sys.stdout.flush()
        raw = ctx.input_func("").strip()
    except (KeyboardInterrupt, EOFError):
        ctx.print_func("\nBreathe.\n")
        return

    if is_advice_seeking(raw):
        run_circuit_breaker(ctx)
        return

    if raw:
        save_entry("pause", raw)
        ctx.print_func("\n")
        ctx.slow_print(f"Acknowledge the '{raw}'. It is just a current passing through.")

    ctx.slow_print("\nYou are back on solid ground. Return to your task one breath at a time.\n")


def run_dusk_release(ctx: CrossingContext) -> None:
    """Dusk Release: 3-minute evening unburdening of mental baggage."""
    ctx.clear_screen()
    ctx.slow_print("\n=== THE DUSK RELEASE ===")
    ctx.slow_print("The day's market is closed. The river keeps flowing.\n")
    ctx.sleep(1.0)

    ctx.slow_print("What is unfinished, heavy, or lingering from today that you can lay down tonight?")

    if ctx.is_headless():
        ctx.sleep(30.0 if not ctx.fast_mode else 0.0)
        for line in get_dusk_closing_prompt()[1:]:
            ctx.slow_print(line)
        return

    try:
        ctx.print_func("\n> ")
        sys.stdout.flush()
        raw = ctx.input_func("").strip()
    except (KeyboardInterrupt, EOFError):
        ctx.print_func("\nRest well.\n")
        return

    if is_advice_seeking(raw):
        run_circuit_breaker(ctx)
        return

    if raw:
        save_entry("dusk", raw)
        ctx.print_func("\n")
        ctx.slow_print("Notice: thinking about it now will not solve it tonight.")
        ctx.slow_print("You did what you could. What remains belongs to tomorrow.")
    else:
        ctx.slow_print("Nothing to carry. A peaceful night.")

    ctx.sleep(1.0)
    ctx.slow_print("\nTurn off this device. Let your mind settle like still water. Rest.\n")


def run_circuit_breaker(ctx: CrossingContext) -> None:
    """Anti-binge circuit breaker: enforces screen-free boundary."""
    ctx.clear_screen()
    ctx.slow_print(get_boundary_message())
