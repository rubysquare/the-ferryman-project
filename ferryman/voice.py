"""
The Ferryman Project — Cross-Platform Voice Engine
Zero-dependency speech synthesis utilizing native OS utilities.
Supports macOS (say), Linux (spd-say, espeak-ng, espeak), and silent fallback.
"""

import os
import re
import sys
import base64
import shutil
import subprocess
from abc import ABC, abstractmethod
from typing import Optional, List
from ferryman.types import SpeechConfig


def clean_spoken_text(text: str) -> str:
    """
    Cleanses visual terminal artifacts, markdown, and punctuation
    before passing text to speech synthesis.
    """
    # Replace markdown links [label](url) with just label
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    # Remove ANSI OSC sequences (\x1b] ... \x07 or \x1b\\)
    text = re.sub(r"\x1b\].*?(?:\x07|\x1b\\)", "", text)
    # Remove ANSI CSI escape sequences (\x1b[ ...)
    text = re.sub(r"\x1b\[[0-9;?]*[ -/]*[@-~]", "", text)
    # Remove 2-character escape codes and charset selectors
    text = re.sub(r"\x1b(?:[@-Z\\-_]|[\(\)][A-Z0-2]|[A-Za-z0-9])", "", text)
    # Remove terminal header bars and dividers
    text = text.replace("=", "").replace("---", "").replace("___", "")
    # Remove menu selectors like [1-4, q]
    text = re.sub(r"\[.*?\]", "", text)
    # Remove markdown bold/italics/backticks/headers
    text = re.sub(r"[\*`_#]", "", text)
    # Normalize extra whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _run_speech_command(cmd: List[str], timeout: int = 30) -> bool:
    """Helper to execute TTS subprocess with timeout handling while propagating KeyboardInterrupt."""
    try:
        res = subprocess.run(
            cmd,
            check=False,
            timeout=timeout
        )
        return res.returncode == 0
    except (subprocess.TimeoutExpired, OSError, ValueError):
        return False


class VoiceEngine(ABC):
    """Abstract interface for local zero-dependency TTS engines."""

    @abstractmethod
    def speak(self, text: str, rate: int) -> bool:
        """Speaks the text aloud. Returns True if speech succeeded, False otherwise."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Checks if the engine's executable is present on the system."""
        pass


class MacOSSayEngine(VoiceEngine):
    """Voice engine using macOS native `say` binary."""

    def is_available(self) -> bool:
        return shutil.which("say") is not None

    def speak(self, text: str, rate: int) -> bool:
        cleaned = clean_spoken_text(text)
        if not cleaned:
            return True
        cmd = ["say", "-r", str(rate), cleaned]
        return _run_speech_command(cmd, timeout=30)


class LinuxSpdSayEngine(VoiceEngine):
    """Voice engine using Linux `spd-say` (Speech Dispatcher)."""

    def is_available(self) -> bool:
        return shutil.which("spd-say") is not None

    def speak(self, text: str, rate: int) -> bool:
        cleaned = clean_spoken_text(text)
        if not cleaned:
            return True
        # spd-say rate is typically -100 to 100; map 160 wpm to ~0
        spd_rate = max(-100, min(100, int((rate - 160) / 2)))
        cmd = ["spd-say", "-r", str(spd_rate), "-w", cleaned]
        return _run_speech_command(cmd, timeout=30)


class LinuxEspeakEngine(VoiceEngine):
    """Voice engine using Linux `espeak-ng` or `espeak`."""

    def __init__(self, binary_name: str = "espeak-ng") -> None:
        self.binary_name = binary_name

    def is_available(self) -> bool:
        return shutil.which(self.binary_name) is not None

    def speak(self, text: str, rate: int) -> bool:
        cleaned = clean_spoken_text(text)
        if not cleaned:
            return True
        cmd = [self.binary_name, "-s", str(rate), cleaned]
        return _run_speech_command(cmd, timeout=30)


class WindowsVoiceEngine(VoiceEngine):
    """Voice engine using Windows PowerShell System.Speech synthesis."""

    def is_available(self) -> bool:
        return sys.platform == "win32" and (
            shutil.which("powershell") is not None or shutil.which("powershell.exe") is not None
        )

    def speak(self, text: str, rate: int) -> bool:
        cleaned = clean_spoken_text(text)
        if not cleaned:
            return True
        # Rate in System.Speech is -10 to 10; default rate 160 wpm maps to 0
        win_rate = max(-10, min(10, int((rate - 160) / 8)))
        ps_text = cleaned.replace("'", "''").replace('"', '`"').replace("\n", " ")
        ps_script = (
            f"Add-Type -AssemblyName System.Speech; "
            f"$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
            f"$synth.Rate = {win_rate}; "
            f"$synth.Speak('{ps_text}')"
        )
        cmd = ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_script]
        return _run_speech_command(cmd, timeout=30)


class NullVoiceEngine(VoiceEngine):
    """Silent fallback engine when no speech synthesizer is available."""

    def is_available(self) -> bool:
        return True

    def speak(self, text: str, rate: int) -> bool:
        return False


def get_voice_engine() -> VoiceEngine:
    """Detects and returns the appropriate voice engine for the current platform."""
    # 1. Check macOS say
    say_engine = MacOSSayEngine()
    if say_engine.is_available():
        return say_engine

    # 2. Check Linux spd-say
    spd_engine = LinuxSpdSayEngine()
    if spd_engine.is_available():
        return spd_engine

    # 3. Check Linux espeak-ng / espeak
    for espeak_bin in ("espeak-ng", "espeak"):
        engine = LinuxEspeakEngine(espeak_bin)
        if engine.is_available():
            return engine

    # 4. Check Windows PowerShell
    win_engine = WindowsVoiceEngine()
    if win_engine.is_available():
        return win_engine

    # 5. Fallback
    return NullVoiceEngine()
