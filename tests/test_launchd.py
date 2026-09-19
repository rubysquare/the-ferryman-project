"""
Unit tests for connectors/launchd/schedule.py
"""

import io
import unittest
from unittest.mock import patch, MagicMock

from connectors.launchd.schedule import (
    label,
    plist_path,
    build_plist,
    install,
    status,
    uninstall,
    bootout,
    WINDOW_MINUTES
)


class TestLaunchd(unittest.TestCase):

    def test_label(self) -> None:
        self.assertEqual(label("dawn"), "org.ferryman.dawn")
        self.assertEqual(label("dusk"), "org.ferryman.dusk")

    def test_plist_path(self) -> None:
        path = plist_path("dawn")
        self.assertTrue(path.endswith("org.ferryman.dawn.plist"))

    def test_build_plist(self) -> None:
        plist = build_plist("dawn", "07:00")
        self.assertEqual(plist["Label"], "org.ferryman.dawn")
        self.assertEqual(plist["ProcessType"], "Background")
        self.assertEqual(plist["StartCalendarInterval"], {"Hour": 7, "Minute": 0})
        args = plist["ProgramArguments"]
        self.assertIn("dawn", args)
        self.assertIn("--voice", args)
        self.assertIn("--window", args)
        idx = args.index("--window")
        self.assertEqual(args[idx + 1], "07:00-08:30")

    @patch("shutil.which", return_value=None)
    def test_install_no_launchctl(self, mock_which: MagicMock) -> None:
        err_buf = io.StringIO()
        with patch("sys.stderr", err_buf):
            install({"dawn": "07:00"})
        self.assertIn("launchd is specific to macOS", err_buf.getvalue())

    @patch("shutil.which", return_value=None)
    def test_status_no_launchctl(self, mock_which: MagicMock) -> None:
        err_buf = io.StringIO()
        with patch("sys.stderr", err_buf):
            status()
        self.assertIn("launchctl command not found", err_buf.getvalue())

    @patch("shutil.which", return_value=None)
    def test_bootout_no_launchctl(self, mock_which: MagicMock) -> None:
        # Should return safely without raising
        bootout("dawn")


if __name__ == "__main__":
    unittest.main()
