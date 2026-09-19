"""
Unit tests for ferryman/crossings.py
"""

import os
import tempfile
import unittest
from typing import List

from ferryman.crossings import (
    CrossingContext,
    run_dawn_anchor,
    run_midday_pause,
    run_dusk_release,
    run_circuit_breaker
)
from ferryman.storage import load_log


class DummyVoiceEngine:
    def __init__(self) -> None:
        self.spoken: List[str] = []

    def is_available(self) -> bool:
        return True

    def speak(self, text: str, rate: int) -> bool:
        self.spoken.append(text)
        return True


class TestCrossings(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_log = os.path.join(self.temp_dir.name, "log.json")
        os.environ["FERRYMAN_DATA_FILE"] = self.test_log
        self.output: List[str] = []

    def tearDown(self) -> None:
        if "FERRYMAN_DATA_FILE" in os.environ:
            del os.environ["FERRYMAN_DATA_FILE"]
        self.temp_dir.cleanup()

    def make_context(
        self,
        user_input: str = "",
        headless: bool = False,
        voice: bool = False,
        raise_interrupt: bool = False
    ) -> CrossingContext:
        self.output = []
        engine = DummyVoiceEngine() if voice else None

        def mock_input(_: str) -> str:
            if raise_interrupt:
                raise KeyboardInterrupt
            return user_input

        ctx = CrossingContext(
            voice_enabled=voice,
            fast_mode=True,
            engine=engine,
            input_func=mock_input,
            print_func=lambda s: self.output.append(s),
            sleep_func=lambda _: None
        )
        if headless:
            ctx.is_headless = lambda: True  # type: ignore
        else:
            ctx.is_headless = lambda: False  # type: ignore
        return ctx

    def test_dawn_anchor_interactive(self) -> None:
        ctx = self.make_context(user_input="Ship the release with calm focus")
        run_dawn_anchor(ctx)
        entries = load_log()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["type"], "dawn")
        self.assertEqual(entries[0]["content"], "Ship the release with calm focus")
        full_text = "".join(self.output)
        self.assertIn("THE DAWN ANCHOR", full_text)
        self.assertIn("Understood. Carry 'Ship the release with calm focus' lightly", full_text)

    def test_dawn_anchor_empty_input(self) -> None:
        ctx = self.make_context(user_input="")
        run_dawn_anchor(ctx)
        self.assertEqual(len(load_log()), 0)
        full_text = "".join(self.output)
        self.assertIn("Silence is also an answer.", full_text)

    def test_dawn_anchor_headless(self) -> None:
        ctx = self.make_context(headless=True)
        run_dawn_anchor(ctx)
        self.assertEqual(len(load_log()), 0)
        full_text = "".join(self.output)
        self.assertIn("Carry it lightly as you cross the river today.", full_text)

    def test_dawn_anchor_circuit_breaker_trigger(self) -> None:
        ctx = self.make_context(user_input="Give me 5 tips to fix my focus")
        run_dawn_anchor(ctx)
        self.assertEqual(len(load_log()), 0)
        full_text = "".join(self.output)
        self.assertIn("THE FERRYMAN'S BOUNDARY", full_text)

    def test_dawn_anchor_interrupt(self) -> None:
        ctx = self.make_context(raise_interrupt=True)
        run_dawn_anchor(ctx)
        self.assertEqual(len(load_log()), 0)
        full_text = "".join(self.output)
        self.assertIn("Take care", full_text)

    def test_midday_pause_interactive(self) -> None:
        ctx = self.make_context(user_input="tightness in chest")
        run_midday_pause(ctx)
        entries = load_log()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["type"], "pause")
        self.assertEqual(entries[0]["content"], "tightness in chest")
        full_text = "".join(self.output)
        self.assertIn("THE MIDDAY PAUSE (SOS)", full_text)
        self.assertIn("Acknowledge the 'tightness in chest'.", full_text)

    def test_midday_pause_headless(self) -> None:
        ctx = self.make_context(headless=True)
        run_midday_pause(ctx)
        self.assertEqual(len(load_log()), 0)
        full_text = "".join(self.output)
        self.assertIn("You are back on solid ground.", full_text)

    def test_midday_pause_circuit_breaker(self) -> None:
        ctx = self.make_context(user_input="how do I fix my stress right now?")
        run_midday_pause(ctx)
        self.assertEqual(len(load_log()), 0)
        full_text = "".join(self.output)
        self.assertIn("THE FERRYMAN'S BOUNDARY", full_text)

    def test_midday_pause_interrupt(self) -> None:
        ctx = self.make_context(raise_interrupt=True)
        run_midday_pause(ctx)
        self.assertEqual(len(load_log()), 0)
        full_text = "".join(self.output)
        self.assertIn("Breathe", full_text)

    def test_dusk_release_interactive(self) -> None:
        ctx = self.make_context(user_input="unresolved email disagreement")
        run_dusk_release(ctx)
        entries = load_log()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["type"], "dusk")
        self.assertEqual(entries[0]["content"], "unresolved email disagreement")
        full_text = "".join(self.output)
        self.assertIn("THE DUSK RELEASE", full_text)
        self.assertIn("What remains belongs to tomorrow.", full_text)

    def test_dusk_release_headless(self) -> None:
        ctx = self.make_context(headless=True)
        run_dusk_release(ctx)
        self.assertEqual(len(load_log()), 0)
        full_text = "".join(self.output)
        self.assertIn("Turn off your devices. Let your mind settle like still water. Rest.", full_text)

    def test_dusk_release_circuit_breaker(self) -> None:
        ctx = self.make_context(user_input="teach me how to sleep")
        run_dusk_release(ctx)
        self.assertEqual(len(load_log()), 0)
        full_text = "".join(self.output)
        self.assertIn("THE FERRYMAN'S BOUNDARY", full_text)

    def test_dusk_release_interrupt(self) -> None:
        ctx = self.make_context(raise_interrupt=True)
        run_dusk_release(ctx)
        self.assertEqual(len(load_log()), 0)
        full_text = "".join(self.output)
        self.assertIn("Rest well", full_text)

    def test_circuit_breaker_direct(self) -> None:
        ctx = self.make_context()
        run_circuit_breaker(ctx)
        full_text = "".join(self.output)
        self.assertIn("THE FERRYMAN'S BOUNDARY", full_text)

    def test_voice_speaking_in_crossings(self) -> None:
        ctx = self.make_context(voice=True, headless=True)
        run_dawn_anchor(ctx)
        self.assertTrue(len(ctx.engine.spoken) > 0)  # type: ignore


if __name__ == "__main__":
    unittest.main()
