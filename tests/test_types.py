"""
Unit tests for ferryman/types.py
"""

import unittest
from ferryman.types import LogEntry, WindowSpec, SpeechConfig


class TestTypes(unittest.TestCase):

    def test_log_entry_structure(self) -> None:
        entry: LogEntry = {
            "timestamp": "2026-09-19T12:00:00",
            "type": "dawn",
            "content": "Deep stillness"
        }
        self.assertEqual(entry["type"], "dawn")
        self.assertEqual(entry["content"], "Deep stillness")
        self.assertIn("timestamp", entry)

    def test_window_spec(self) -> None:
        spec = WindowSpec(
            start_hour=7,
            start_minute=0,
            end_hour=8,
            end_minute=30,
            wraps_midnight=False
        )
        self.assertEqual(spec.start_hour, 7)
        self.assertEqual(spec.end_minute, 30)
        self.assertFalse(spec.wraps_midnight)

    def test_speech_config_defaults(self) -> None:
        config = SpeechConfig(rate=160)
        self.assertEqual(config.rate, 160)
        self.assertIsNone(config.voice_name)
        self.assertFalse(config.enabled)


if __name__ == "__main__":
    unittest.main()
