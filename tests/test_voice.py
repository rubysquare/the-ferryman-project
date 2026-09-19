"""
Unit tests for ferryman/voice.py
"""

import sys
import unittest
from unittest.mock import patch, MagicMock

from ferryman.voice import (
    clean_spoken_text,
    NullVoiceEngine,
    MacOSSayEngine,
    LinuxSpdSayEngine,
    LinuxEspeakEngine,
    WindowsVoiceEngine,
    get_voice_engine
)


class TestVoice(unittest.TestCase):

    def test_clean_spoken_text_ansi_and_markdown(self) -> None:
        raw = "\033c\n=== THE DAWN ANCHOR ===\nChoose [1-4, q]: *breathe* deeply `now`"
        cleaned = clean_spoken_text(raw)
        self.assertNotIn("===", cleaned)
        self.assertNotIn("[1-4, q]", cleaned)
        self.assertNotIn("*", cleaned)
        self.assertNotIn("`", cleaned)
        self.assertNotIn("\033", cleaned)
        self.assertIn("THE DAWN ANCHOR", cleaned)
        self.assertIn("breathe deeply now", cleaned)

    def test_clean_spoken_text_extended_ansi(self) -> None:
        raw = "\x1b[2J\x1b[H\x1b[32mGreen text\x1b[0m and \x1b(Bcharset reset"
        cleaned = clean_spoken_text(raw)
        self.assertNotIn("\x1b", cleaned)
        self.assertIn("Green text and charset reset", cleaned)

    def test_clean_spoken_text_markdown_links(self) -> None:
        raw = "Inspired by [Vasudeva](https://en.wikipedia.org/wiki/Vasudeva) the ferryman."
        cleaned = clean_spoken_text(raw)
        self.assertNotIn("https://", cleaned)
        self.assertNotIn("[", cleaned)
        self.assertNotIn("]", cleaned)
        self.assertIn("Inspired by Vasudeva the ferryman.", cleaned)

    def test_clean_spoken_text_osc_sequences(self) -> None:
        raw = "\x1b]0;Terminal Title\x07Hello peaceful river \x1b\\Next line"
        cleaned = clean_spoken_text(raw)
        self.assertNotIn("\x1b", cleaned)
        self.assertNotIn("Terminal Title", cleaned)
        self.assertIn("Hello peaceful river Next line", cleaned)

    def test_null_voice_engine(self) -> None:
        engine = NullVoiceEngine()
        self.assertTrue(engine.is_available())
        self.assertFalse(engine.speak("Hello", 160))

    def test_empty_text_returns_true(self) -> None:
        say_engine = MacOSSayEngine()
        self.assertTrue(say_engine.speak("", 160))

        spd_engine = LinuxSpdSayEngine()
        self.assertTrue(spd_engine.speak("", 160))

        espeak_engine = LinuxEspeakEngine()
        self.assertTrue(espeak_engine.speak("", 160))

        win_engine = WindowsVoiceEngine()
        self.assertTrue(win_engine.speak("", 160))

    @patch("shutil.which", return_value="/usr/bin/say")
    @patch("subprocess.run")
    def test_macos_say_engine_speak(self, mock_run: MagicMock, mock_which: MagicMock) -> None:
        engine = MacOSSayEngine()
        self.assertTrue(engine.is_available())
        mock_run.return_value = MagicMock(returncode=0)
        self.assertTrue(engine.speak("Breathe", 160))
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        self.assertEqual(cmd, ["say", "-r", "160", "Breathe"])

    @patch("shutil.which", return_value="/usr/bin/spd-say")
    @patch("subprocess.run")
    def test_linux_spd_say_engine_speak(self, mock_run: MagicMock, mock_which: MagicMock) -> None:
        engine = LinuxSpdSayEngine()
        self.assertTrue(engine.is_available())
        mock_run.return_value = MagicMock(returncode=0)
        self.assertTrue(engine.speak("Breathe", 160))
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        self.assertEqual(cmd, ["spd-say", "-r", "0", "-w", "Breathe"])

    @patch("shutil.which", return_value="/usr/bin/espeak-ng")
    @patch("subprocess.run")
    def test_linux_espeak_engine_speak(self, mock_run: MagicMock, mock_which: MagicMock) -> None:
        engine = LinuxEspeakEngine("espeak-ng")
        self.assertTrue(engine.is_available())
        mock_run.return_value = MagicMock(returncode=0)
        self.assertTrue(engine.speak("Breathe", 160))
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        self.assertEqual(cmd, ["espeak-ng", "-s", "160", "Breathe"])

    @patch("sys.platform", "win32")
    @patch("shutil.which", return_value=r"C:\Windows\System32\powershell.exe")
    @patch("subprocess.run")
    def test_windows_voice_engine_speak(self, mock_run: MagicMock, mock_which: MagicMock) -> None:
        engine = WindowsVoiceEngine()
        self.assertTrue(engine.is_available())
        mock_run.return_value = MagicMock(returncode=0)
        self.assertTrue(engine.speak("Breathe", 160))
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        self.assertEqual(cmd[0], "powershell")
        self.assertIn("System.Speech.Synthesis.SpeechSynthesizer", cmd[-1])
        self.assertIn("Breathe", cmd[-1])

    def test_get_voice_engine_returns_valid_instance(self) -> None:
        engine = get_voice_engine()
        self.assertIsNotNone(engine)
        self.assertTrue(hasattr(engine, "speak"))
        self.assertTrue(hasattr(engine, "is_available"))


if __name__ == "__main__":
    unittest.main()
