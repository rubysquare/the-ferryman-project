#!/usr/bin/env python3
"""
The Ferryman Project — macOS scheduler (launchd)
Speaks the Dawn Anchor and Dusk Release aloud at set hours. No screen, no network.

Usage:
    python3 schedule.py install                      # dawn 07:00, dusk 21:30
    python3 schedule.py install --dawn 06:30 --dusk 22:00
    python3 schedule.py status
    python3 schedule.py uninstall
"""

import os
import sys
import plistlib
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

FERRYMAN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "ferryman.py"))
AGENTS_DIR = os.path.expanduser("~/Library/LaunchAgents")
DEFAULTS: Dict[str, str] = {"dawn": "07:00", "dusk": "21:30"}
WINDOW_MINUTES = 90


def label(crossing: str) -> str:
    """Returns the launchd job label for a crossing."""
    return f"org.ferryman.{crossing}"


def plist_path(crossing: str) -> str:
    """Returns the absolute file path for a crossing's plist."""
    return os.path.join(AGENTS_DIR, label(crossing) + ".plist")


def build_plist(crossing: str, at: str) -> Dict[str, Any]:
    """Generates the launchd property list dictionary."""
    start = datetime.strptime(at, "%H:%M")
    end = start + timedelta(minutes=WINDOW_MINUTES)
    window = f"{start:%H:%M}-{end:%H:%M}"
    return {
        "Label": label(crossing),
        "ProgramArguments": [sys.executable, FERRYMAN, crossing, "--voice", "--window", window],
        "StartCalendarInterval": {"Hour": start.hour, "Minute": start.minute},
        "ProcessType": "Background",
    }


import shutil


def bootout(crossing: str) -> None:
    """Unloads a launchd job if currently loaded."""
    if shutil.which("launchctl") is None:
        return
    try:
        subprocess.run(
            ["launchctl", "bootout", f"gui/{os.getuid()}/{label(crossing)}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )
    except OSError:
        pass


def install(times: Dict[str, str]) -> None:
    """Installs and bootstraps launchd LaunchAgents."""
    if sys.platform != "darwin" or shutil.which("launchctl") is None:
        sys.stderr.write("Notice: launchd is specific to macOS with launchctl installed. Use systemd or cron on Linux.\n")
        return

    os.makedirs(AGENTS_DIR, exist_ok=True)
    for crossing, at in times.items():
        bootout(crossing)
        target_plist = plist_path(crossing)
        with open(target_plist, "wb") as f:
            plistlib.dump(build_plist(crossing, at), f)
        res = subprocess.run(
            ["launchctl", "bootstrap", f"gui/{os.getuid()}", target_plist],
            capture_output=True,
            text=True,
            check=False
        )
        if res.returncode == 0:
            print(f"Installed {crossing}: {at} (Window: {WINDOW_MINUTES}m)")
        else:
            sys.stderr.write(f"Warning: launchctl bootstrap returned code {res.returncode}: {res.stderr.strip()}\n")


def status() -> None:
    """Checks the status of installed Ferryman launchd jobs."""
    print("=== Ferryman launchd Status ===")
    if sys.platform != "darwin" or shutil.which("launchctl") is None:
        sys.stderr.write("Notice: launchctl command not found or not on macOS. This scheduler requires macOS.\n")
        return

    for crossing in DEFAULTS:
        path = plist_path(crossing)
        if not os.path.exists(path):
            print(f"{crossing}: Not installed")
            continue

        # Check launchctl state
        try:
            res = subprocess.run(
                ["launchctl", "print", f"gui/{os.getuid()}/{label(crossing)}"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False
            )
            state = "Active (loaded)" if res.returncode == 0 else "Plist exists (unloaded)"
        except OSError:
            state = "Plist exists (unloaded)"

        try:
            with open(path, "rb") as f:
                data = plistlib.load(f)
                cal = data.get("StartCalendarInterval", {})
                hour = cal.get("Hour", 0)
                minute = cal.get("Minute", 0)
                print(f"{crossing}: {state} at {hour:02d}:{minute:02d}")
        except Exception:
            print(f"{crossing}: {state} (Could not read plist)")


def uninstall() -> None:
    """Unloads and removes launchd LaunchAgents."""
    for crossing in DEFAULTS:
        bootout(crossing)
        path = plist_path(crossing)
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass
    print("Uninstalled all Ferryman launchd schedules.")


def main(argv: Optional[List[str]] = None) -> None:
    if argv is None:
        argv = sys.argv[1:]

    if not argv or argv[0] not in ("install", "uninstall", "status"):
        print(__doc__.strip())
        return

    cmd = argv[0]
    if cmd == "uninstall":
        uninstall()
        return
    elif cmd == "status":
        status()
        return

    times = dict(DEFAULTS)
    for crossing in DEFAULTS:
        flag = "--" + crossing
        if flag in argv:
            idx = argv.index(flag)
            if idx + 1 < len(argv):
                at = argv[idx + 1]
                try:
                    datetime.strptime(at, "%H:%M")
                    times[crossing] = at
                except ValueError:
                    sys.exit(f"{flag} requires an hour in HH:MM format, e.g. {flag} {DEFAULTS[crossing]}")

    install(times)


if __name__ == "__main__":
    main()
