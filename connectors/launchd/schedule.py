#!/usr/bin/env python3
"""
The Ferryman Project — macOS scheduler (launchd)
Speaks the Dawn Anchor and Dusk Release aloud at set hours. No screen, no network.

    python3 schedule.py install                      # dawn 07:00, dusk 21:30
    python3 schedule.py install --dawn 06:30 --dusk 22:00
    python3 schedule.py uninstall
"""

import os
import sys
import plistlib
import subprocess
from datetime import datetime, timedelta

FERRYMAN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "ferryman.py"))
AGENTS_DIR = os.path.expanduser("~/Library/LaunchAgents")
DEFAULTS = {"dawn": "07:00", "dusk": "21:30"}
# If the machine was asleep at the hour, launchd fires on wake. Past this, stay silent.
WINDOW_MINUTES = 90


def label(crossing):
    return f"org.ferryman.{crossing}"


def plist_path(crossing):
    return os.path.join(AGENTS_DIR, label(crossing) + ".plist")


def build_plist(crossing, at):
    start = datetime.strptime(at, "%H:%M")
    end = start + timedelta(minutes=WINDOW_MINUTES)
    window = f"{start:%H:%M}-{end:%H:%M}"
    return {
        "Label": label(crossing),
        "ProgramArguments": ["/usr/bin/python3", FERRYMAN, crossing, "--voice", "--window", window],
        "StartCalendarInterval": {"Hour": start.hour, "Minute": start.minute},
        "ProcessType": "Background",
    }


def bootout(crossing):
    subprocess.run(["launchctl", "bootout", f"gui/{os.getuid()}/{label(crossing)}"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)


def install(times):
    os.makedirs(AGENTS_DIR, exist_ok=True)
    for crossing, at in times.items():
        bootout(crossing)
        with open(plist_path(crossing), "wb") as f:
            plistlib.dump(build_plist(crossing, at), f)
        subprocess.run(["launchctl", "bootstrap", f"gui/{os.getuid()}", plist_path(crossing)], check=True)
        print(f"{crossing}: {at}")


def uninstall():
    for crossing in DEFAULTS:
        bootout(crossing)
        if os.path.exists(plist_path(crossing)):
            os.remove(plist_path(crossing))
    print("Removed.")


def main():
    args = sys.argv[1:]
    if not args or args[0] not in ("install", "uninstall"):
        print(__doc__.strip())
        return
    if args[0] == "uninstall":
        uninstall()
        return
    times = dict(DEFAULTS)
    for crossing in DEFAULTS:
        flag = "--" + crossing
        if flag in args:
            at = "".join(args[args.index(flag) + 1:][:1])
            try:
                datetime.strptime(at, "%H:%M")
            except ValueError:
                sys.exit(f"{flag} needs an hour as HH:MM, e.g. {flag} {DEFAULTS[crossing]}")
            times[crossing] = at
    install(times)


if __name__ == "__main__":
    main()
