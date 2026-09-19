"""
Unit tests for ferryman/cli.py
"""

import io
import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock

from ferryman.cli import parse_args, main, VERSION, setup_signal_handlers
from ferryman.storage import save_entry, load_log


class TestCLI(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_log = os.path.join(self.temp_dir.name, "log.json")
        os.environ["FERRYMAN_DATA_FILE"] = self.test_log

    def tearDown(self) -> None:
        if "FERRYMAN_DATA_FILE" in os.environ:
            del os.environ["FERRYMAN_DATA_FILE"]
        self.temp_dir.cleanup()

    def test_parse_args(self) -> None:
        argv = ["dawn", "--voice", "--rate", "180", "--fast", "--window", "07:00-08:30"]
        args, voice, rate, fast, window = parse_args(argv)
        self.assertEqual(args, ["dawn"])
        self.assertTrue(voice)
        self.assertEqual(rate, 180)
        self.assertTrue(fast)
        self.assertEqual(window, "07:00-08:30")

    def test_parse_args_invalid_rate(self) -> None:
        argv = ["dawn", "--rate", "not-a-number"]
        args, voice, rate, fast, window = parse_args(argv)
        self.assertEqual(rate, 160)  # default preserved

    def test_parse_args_no_delay(self) -> None:
        argv = ["--no-delay"]
        args, voice, rate, fast, window = parse_args(argv)
        self.assertTrue(fast)

    def test_version_flag(self) -> None:
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            code = main(["--version"])
        self.assertEqual(code, 0)
        self.assertIn(f"The Ferryman Project v{VERSION}", buf.getvalue())

    def test_help_flag(self) -> None:
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            code = main(["--help"])
        self.assertEqual(code, 0)
        self.assertIn("The Ferryman Project", buf.getvalue())
        self.assertIn("Usage:", buf.getvalue())

    def test_window_out_of_range_exits_silently(self) -> None:
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            code = main(["--window", "03:00-03:01", "dawn", "--fast"])
        self.assertEqual(code, 0)
        self.assertEqual(buf.getvalue(), "")

    def test_status_command(self) -> None:
        save_entry("dawn", "Presence test")
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            code = main(["status"])
        self.assertEqual(code, 0)
        self.assertIn("Total Crossings Recorded: 1", buf.getvalue())
        self.assertIn("Presence test", buf.getvalue())

    def test_clear_log_command(self) -> None:
        save_entry("pause", "Somatic reset")
        self.assertEqual(len(load_log()), 1)
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            code = main(["clear-log"])
        self.assertEqual(code, 0)
        self.assertEqual(len(load_log()), 0)
        self.assertIn("wiped clean", buf.getvalue())

    def test_command_aliases(self) -> None:
        aliases = [
            (["morning", "--fast"], "THE DAWN ANCHOR"),
            (["anchor", "--fast"], "THE DAWN ANCHOR"),
            (["pause", "--fast"], "THE MIDDAY PAUSE"),
            (["sos", "--fast"], "THE MIDDAY PAUSE"),
            (["knot", "--fast"], "THE MIDDAY PAUSE"),
            (["midday", "--fast"], "THE MIDDAY PAUSE"),
            (["dusk", "--fast"], "THE DUSK RELEASE"),
            (["night", "--fast"], "THE DUSK RELEASE"),
            (["release", "--fast"], "THE DUSK RELEASE"),
            (["evening", "--fast"], "THE DUSK RELEASE"),
            (["tips", "--fast"], "THE FERRYMAN'S BOUNDARY"),
            (["chat", "--fast"], "THE FERRYMAN'S BOUNDARY"),
            (["ask", "--fast"], "THE FERRYMAN'S BOUNDARY"),
            (["help", "--fast"], "THE FERRYMAN'S BOUNDARY"),
            (["breaker", "--fast"], "THE FERRYMAN'S BOUNDARY"),
        ]
        for cmd_args, expected_output in aliases:
            with self.subTest(cmd=cmd_args):
                buf = io.StringIO()
                with patch("sys.stdout", buf):
                    with patch("builtins.input", return_value="test input"):
                        code = main(cmd_args)
                self.assertEqual(code, 0)
                self.assertIn(expected_output, buf.getvalue())

    def test_interactive_menu_choices(self) -> None:
        choices = [
            ("1", "THE DAWN ANCHOR"),
            ("2", "THE MIDDAY PAUSE"),
            ("3", "THE DUSK RELEASE"),
            ("4", "THE FERRYMAN'S BOUNDARY"),
            ("q", "Step away and breathe"),
            ("invalid", "Step away and breathe"),
        ]
        for choice, expected_output in choices:
            with self.subTest(choice=choice):
                buf = io.StringIO()
                with patch("sys.stdout", buf):
                    with patch("sys.stdin.isatty", return_value=True):
                        with patch("builtins.input", side_effect=[choice, "test"]):
                            code = main(["--fast"])
                self.assertEqual(code, 0)
                self.assertIn(expected_output, buf.getvalue())

    def test_non_tty_menu_graceful_exit(self) -> None:
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            with patch("sys.stdin.isatty", return_value=False):
                code = main([])
        self.assertEqual(code, 0)
        self.assertIn("The river awaits", buf.getvalue())

    def test_parse_args_duplicates_and_trailing(self) -> None:
        # Duplicate flags
        args, voice, rate, fast, window = parse_args(["--voice", "--voice", "--fast", "--fast", "dawn"])
        self.assertEqual(args, ["dawn"])
        self.assertTrue(voice)
        self.assertTrue(fast)

        # Trailing flags without arguments
        args, voice, rate, fast, window = parse_args(["--rate"])
        self.assertEqual(args, [])

        args, voice, rate, fast, window = parse_args(["--window"])
        self.assertEqual(args, [])

        # Negative or out of bounds rates ignored
        args, voice, rate, fast, window = parse_args(["--rate", "-50", "dawn"])
        self.assertEqual(rate, 160)

        args, voice, rate, fast, window = parse_args(["--rate", "9999", "dawn"])
        self.assertEqual(rate, 160)

    def test_unrecognized_command(self) -> None:
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            code = main(["unknown_crossing"])
        self.assertEqual(code, 1)
        self.assertIn("Unknown crossing 'unknown_crossing'", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
