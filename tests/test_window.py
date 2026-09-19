"""
Unit tests for ferryman/window.py
"""

import unittest
from datetime import datetime
from ferryman.window import parse_window, is_in_window


class TestWindow(unittest.TestCase):

    def test_parse_valid_same_day_window(self) -> None:
        spec = parse_window("07:00-08:30")
        self.assertEqual(spec.start_hour, 7)
        self.assertEqual(spec.start_minute, 0)
        self.assertEqual(spec.end_hour, 8)
        self.assertEqual(spec.end_minute, 30)
        self.assertFalse(spec.wraps_midnight)

    def test_parse_valid_overnight_window(self) -> None:
        spec = parse_window("23:30-01:15")
        self.assertEqual(spec.start_hour, 23)
        self.assertEqual(spec.start_minute, 30)
        self.assertEqual(spec.end_hour, 1)
        self.assertEqual(spec.end_minute, 15)
        self.assertTrue(spec.wraps_midnight)

    def test_parse_midnight_boundaries(self) -> None:
        spec = parse_window("23:59-00:01")
        self.assertEqual(spec.start_hour, 23)
        self.assertEqual(spec.start_minute, 59)
        self.assertEqual(spec.end_hour, 0)
        self.assertEqual(spec.end_minute, 1)
        self.assertTrue(spec.wraps_midnight)

    def test_parse_invalid_windows(self) -> None:
        invalid_cases = [
            "",
            "   ",
            "07:00",
            "07:00-08:00-09:00",
            "25:00-08:00",
            "07:00-24:00",
            "07:60-08:00",
            "abc-def",
            "07:00 - 08:30:00",
            "-",
            "07:00-",
            "-08:00"
        ]
        for case in invalid_cases:
            with self.subTest(case=case):
                with self.assertRaises(ValueError):
                    parse_window(case)

    def test_is_in_window_same_day(self) -> None:
        window = "07:00-08:30"
        # Inside
        dt_in = datetime(2026, 9, 19, 7, 30)
        self.assertTrue(is_in_window(window, now=dt_in))
        # Exact start
        self.assertTrue(is_in_window(window, now=datetime(2026, 9, 19, 7, 0)))
        # Exact end
        self.assertTrue(is_in_window(window, now=datetime(2026, 9, 19, 8, 30)))
        # Before
        self.assertFalse(is_in_window(window, now=datetime(2026, 9, 19, 6, 59)))
        # After
        self.assertFalse(is_in_window(window, now=datetime(2026, 9, 19, 8, 31)))

    def test_is_in_window_overnight(self) -> None:
        window = "22:00-02:00"
        # Late night inside
        self.assertTrue(is_in_window(window, now=datetime(2026, 9, 19, 23, 0)))
        # Early morning inside
        self.assertTrue(is_in_window(window, now=datetime(2026, 9, 20, 1, 30)))
        # Exact boundaries
        self.assertTrue(is_in_window(window, now=datetime(2026, 9, 19, 22, 0)))
        self.assertTrue(is_in_window(window, now=datetime(2026, 9, 20, 2, 0)))
        # Outside (daytime)
        self.assertFalse(is_in_window(window, now=datetime(2026, 9, 19, 12, 0)))
        self.assertFalse(is_in_window(window, now=datetime(2026, 9, 19, 21, 59)))
        self.assertFalse(is_in_window(window, now=datetime(2026, 9, 20, 2, 1)))

    def test_is_in_window_invalid_returns_false(self) -> None:
        self.assertFalse(is_in_window("invalid-window"))
        self.assertFalse(is_in_window(""))


if __name__ == "__main__":
    unittest.main()
