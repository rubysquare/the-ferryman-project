"""
Unit tests for connectors/cron/schedule.py
"""

import io
import unittest
from unittest.mock import patch, MagicMock

from connectors.cron.schedule import (
    generate_cron_lines,
    strip_ferryman_block,
    get_existing_crontab,
    set_crontab,
    install,
    status,
    uninstall,
    main,
    CRON_START_TAG,
    CRON_END_TAG,
    DEFAULTS,
)


class TestCron(unittest.TestCase):

    def test_generate_cron_lines(self) -> None:
        times = {"dawn": "07:00", "dusk": "21:30"}
        lines = generate_cron_lines(times)
        self.assertEqual(lines[0], CRON_START_TAG)
        self.assertEqual(lines[-1], CRON_END_TAG)

        # Dawn line: 0 7 * * * ... dawn ... --window 07:00-08:30
        dawn_line = [l for l in lines if "dawn" in l][0]
        self.assertTrue(dawn_line.startswith("0 7 * * * "))
        self.assertIn("dawn --voice --window 07:00-08:30", dawn_line)

        # Dusk line: 30 21 * * * ... dusk ... --window 21:30-23:00
        dusk_line = [l for l in lines if "dusk" in l][0]
        self.assertTrue(dusk_line.startswith("30 21 * * * "))
        self.assertIn("dusk --voice --window 21:30-23:00", dusk_line)

    def test_strip_ferryman_block_when_present(self) -> None:
        crontab = (
            "# Existing user cron job\n"
            "0 0 * * * /usr/bin/backup.sh\n"
            f"{CRON_START_TAG}\n"
            "0 7 * * * /usr/bin/python3 ferryman.py dawn --voice\n"
            f"{CRON_END_TAG}\n"
            "# Another job\n"
            "*/5 * * * * /usr/bin/check.sh\n"
        )
        stripped = strip_ferryman_block(crontab)
        self.assertNotIn(CRON_START_TAG, stripped)
        self.assertNotIn("ferryman.py", stripped)
        self.assertIn("backup.sh", stripped)
        self.assertIn("check.sh", stripped)

    def test_strip_ferryman_block_when_absent(self) -> None:
        crontab = "0 0 * * * /usr/bin/backup.sh\n"
        stripped = strip_ferryman_block(crontab)
        self.assertEqual(stripped, "0 0 * * * /usr/bin/backup.sh\n")

    def test_strip_ferryman_block_empty(self) -> None:
        self.assertEqual(strip_ferryman_block(""), "")

    @patch("shutil.which", return_value="/usr/bin/crontab")
    @patch("subprocess.run")
    def test_get_existing_crontab(self, mock_run: MagicMock, mock_which: MagicMock) -> None:
        mock_run.return_value = MagicMock(stdout="0 1 * * * /foo\n", returncode=0)
        out = get_existing_crontab()
        self.assertEqual(out, "0 1 * * * /foo\n")

    @patch("shutil.which", return_value=None)
    def test_get_existing_crontab_no_binary(self, mock_which: MagicMock) -> None:
        out = get_existing_crontab()
        self.assertEqual(out, "")

    @patch("shutil.which", return_value="/usr/bin/crontab")
    @patch("subprocess.run")
    def test_set_crontab(self, mock_run: MagicMock, mock_which: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=0)
        success = set_crontab("0 1 * * * /foo\n")
        self.assertTrue(success)

    @patch("connectors.cron.schedule.get_existing_crontab", return_value="")
    @patch("connectors.cron.schedule.set_crontab", return_value=True)
    def test_install(self, mock_set: MagicMock, mock_get: MagicMock) -> None:
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            install({"dawn": "07:00", "dusk": "21:30"})
        mock_set.assert_called_once()
        self.assertIn("Installed dawn: 07:00 in crontab", buf.getvalue())

    def test_strip_ferryman_block_truncated(self) -> None:
        crontab = (
            "0 0 * * * /usr/bin/backup.sh\n"
            f"{CRON_START_TAG}\n"
            "0 7 * * * /usr/bin/python3 ferryman.py dawn --voice\n"
            "# user job below without end tag\n"
            "*/10 * * * * /usr/bin/sync.sh\n"
        )
        stripped = strip_ferryman_block(crontab)
        self.assertIn("backup.sh", stripped)
        self.assertIn("sync.sh", stripped)
        self.assertNotIn(CRON_START_TAG, stripped)
        self.assertNotIn("ferryman.py", stripped)

    @patch("shutil.which", return_value=None)
    def test_status_no_crontab_binary(self, mock_which: MagicMock) -> None:
        err_buf = io.StringIO()
        with patch("sys.stderr", err_buf):
            status()
        self.assertIn("crontab command not found", err_buf.getvalue())

    @patch("shutil.which", return_value="/usr/bin/crontab")
    @patch("connectors.cron.schedule.get_existing_crontab", return_value=f"{CRON_START_TAG}\n0 7 * * * python3 ferryman.py dawn\n{CRON_END_TAG}\n")
    def test_status_with_entries(self, mock_get: MagicMock, mock_which: MagicMock) -> None:
        out_buf = io.StringIO()
        with patch("sys.stdout", out_buf):
            status()
        self.assertIn("0 7 * * * python3 ferryman.py dawn", out_buf.getvalue())


if __name__ == "__main__":
    unittest.main()
