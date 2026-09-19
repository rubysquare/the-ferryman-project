"""
Unit tests for connectors/systemd/schedule.py
"""

import os
import unittest
from unittest.mock import patch, MagicMock

from connectors.systemd.schedule import (
    service_name,
    timer_name,
    service_path,
    timer_path,
    generate_service_content,
    generate_timer_content,
    install,
    status,
    uninstall,
    main,
    DEFAULTS,
    WINDOW_MINUTES,
)


class TestSystemd(unittest.TestCase):

    def test_unit_names(self) -> None:
        self.assertEqual(service_name("dawn"), "ferryman-dawn.service")
        self.assertEqual(service_name("dusk"), "ferryman-dusk.service")
        self.assertEqual(timer_name("dawn"), "ferryman-dawn.timer")
        self.assertEqual(timer_name("dusk"), "ferryman-dusk.timer")

    def test_unit_paths(self) -> None:
        spath = service_path("dawn")
        tpath = timer_path("dawn")
        self.assertTrue(spath.endswith("ferryman-dawn.service"))
        self.assertTrue(tpath.endswith("ferryman-dawn.timer"))
        self.assertIn(".config/systemd/user", spath)

    def test_generate_service_content(self) -> None:
        content = generate_service_content("dawn", "07:00")
        self.assertIn("[Unit]", content)
        self.assertIn("Description=The Ferryman Project — Dawn Crossing", content)
        self.assertIn("[Service]", content)
        self.assertIn("Type=oneshot", content)
        self.assertIn("ExecStart=", content)
        self.assertIn("dawn --voice --window 07:00-08:30", content)

    def test_generate_timer_content(self) -> None:
        content = generate_timer_content("dusk", "21:30")
        self.assertIn("[Unit]", content)
        self.assertIn("Description=The Ferryman Project — Dusk Timer", content)
        self.assertIn("[Timer]", content)
        self.assertIn("OnCalendar=*-*-* 21:30:00", content)
        self.assertIn("Persistent=false", content)
        self.assertIn("[Install]", content)
        self.assertIn("WantedBy=timers.target", content)

    @patch("shutil.which", return_value=None)
    @patch("sys.stderr.write")
    def test_systemctl_not_found_graceful(self, mock_stderr: MagicMock, mock_which: MagicMock) -> None:
        install(dict(DEFAULTS))
        mock_stderr.assert_called()
        self.assertIn("systemctl command not found", mock_stderr.call_args[0][0])

    @patch("shutil.which", return_value="/usr/bin/systemctl")
    @patch("os.makedirs")
    @patch("builtins.open", unittest.mock.mock_open())
    @patch("subprocess.run")
    def test_install_success(self, mock_run: MagicMock, mock_dirs: MagicMock, mock_which: MagicMock) -> None:
        times = {"dawn": "06:30", "dusk": "22:00"}
        install(times)
        mock_dirs.assert_called_once()
        # Verify daemon-reload and enable calls
        self.assertTrue(mock_run.called)
        calls = [c[0][0] for c in mock_run.call_args_list]
        self.assertIn(["systemctl", "--user", "daemon-reload"], calls)
        self.assertIn(["systemctl", "--user", "enable", "--now", "ferryman-dawn.timer"], calls)
        self.assertIn(["systemctl", "--user", "enable", "--now", "ferryman-dusk.timer"], calls)

    @patch("shutil.which", return_value="/usr/bin/systemctl")
    @patch("subprocess.run")
    def test_status_active(self, mock_run: MagicMock, mock_which: MagicMock) -> None:
        mock_run.return_value = MagicMock(stdout="ferryman-dawn.timer\nferryman-dusk.timer\n", returncode=0)
        with patch("sys.stdout.write"):
            status()
        mock_run.assert_called_once()

    @patch("shutil.which", return_value="/usr/bin/systemctl")
    @patch("os.path.exists", return_value=True)
    @patch("os.remove")
    @patch("subprocess.run")
    def test_uninstall(self, mock_run: MagicMock, mock_remove: MagicMock, mock_exists: MagicMock, mock_which: MagicMock) -> None:
        uninstall()
        self.assertTrue(mock_run.called)
        self.assertTrue(mock_remove.called)


if __name__ == "__main__":
    unittest.main()
