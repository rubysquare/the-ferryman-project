#!/usr/bin/env python3
"""
The Ferryman Project — Universal POSIX crontab Scheduler
Schedules Dawn Anchor and Dusk Release via the user's crontab.

Usage:
    python3 schedule.py install                      # dawn 07:00, dusk 21:30
    python3 schedule.py install --dawn 06:30 --dusk 22:00
    python3 schedule.py status
    python3 schedule.py uninstall
"""

import os
import sys
import shutil
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional

FERRYMAN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "ferryman.py"))
DEFAULTS: Dict[str, str] = {"dawn": "07:00", "dusk": "21:30"}
WINDOW_MINUTES = 90
CRON_START_TAG = "# BEGIN FERRYMAN"
CRON_END_TAG = "# END FERRYMAN"


def get_existing_crontab() -> str:
    """Retrieves current user crontab or empty string if none exists."""
    if shutil.which("crontab") is None:
        return ""
    res = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=False)
    if res.returncode == 0:
        return res.stdout
    return ""


def set_crontab(content: str) -> bool:
    """Updates user crontab with new content."""
    if shutil.which("crontab") is None:
        sys.stderr.write("Notice: crontab command not found.\n")
        return False
    res = subprocess.run(["crontab", "-"], input=content, text=True, capture_output=True, check=False)
    return res.returncode == 0


def generate_cron_lines(times: Dict[str, str]) -> List[str]:
    """Generates cron entries for the configured crossing times."""
    lines = [CRON_START_TAG]
    for crossing, at in times.items():
        dt = datetime.strptime(at, "%H:%M")
        end_dt = dt + timedelta(minutes=WINDOW_MINUTES)
        window = f"{dt:%H:%M}-{end_dt:%H:%M}"
        cmd = f"{sys.executable} {FERRYMAN} {crossing} --voice --window {window}"
        # Format: minute hour * * * command
        lines.append(f"{dt.minute} {dt.hour} * * * {cmd}")
    lines.append(CRON_END_TAG)
    return lines


def strip_ferryman_block(crontab_text: str) -> str:
    """Removes the Ferryman block from crontab content without deleting unrelated user jobs."""
    lines = crontab_text.splitlines()
    has_start = any(line.strip() == CRON_START_TAG for line in lines)
    has_end = any(line.strip() == CRON_END_TAG for line in lines)

    cleaned: List[str] = []
    if has_start and has_end:
        # Standard balanced block removal
        in_block = False
        for line in lines:
            if line.strip() == CRON_START_TAG:
                in_block = True
                continue
            if line.strip() == CRON_END_TAG:
                in_block = False
                continue
            if not in_block:
                cleaned.append(line)
    elif has_start:
        # Unclosed block: only strip CRON_START_TAG and lines that reference ferryman
        for line in lines:
            if line.strip() == CRON_START_TAG or "ferryman" in line.lower():
                continue
            cleaned.append(line)
    else:
        # No start tag: preserve all lines except any lingering end tag
        for line in lines:
            if line.strip() == CRON_END_TAG:
                continue
            cleaned.append(line)

    return "\n".join(cleaned).strip() + "\n" if cleaned else ""


def install(times: Dict[str, str]) -> None:
    current = get_existing_crontab()
    stripped = strip_ferryman_block(current)
    new_block = "\n".join(generate_cron_lines(times))
    updated = (stripped + "\n" + new_block + "\n").strip() + "\n"

    if set_crontab(updated):
        for crossing, at in times.items():
            print(f"Installed {crossing}: {at} in crontab")
    else:
        sys.stderr.write("Failed to install crontab entries.\n")


def status() -> None:
    print("=== Ferryman crontab Status ===")
    if shutil.which("crontab") is None:
        sys.stderr.write("Notice: crontab command not found. This scheduler requires crontab.\n")
        return

    current = get_existing_crontab()
    lines = current.splitlines()
    in_block = False
    found = False
    for line in lines:
        if line.strip() == CRON_START_TAG:
            in_block = True
            continue
        if line.strip() == CRON_END_TAG:
            in_block = False
            continue
        if in_block:
            found = True
            print(line)

    if not found:
        print("No Ferryman crontab entries found.")


def uninstall() -> None:
    current = get_existing_crontab()
    stripped = strip_ferryman_block(current)
    if set_crontab(stripped):
        print("Removed all Ferryman crontab entries.")
    else:
        sys.stderr.write("Failed to remove crontab entries.\n")


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
