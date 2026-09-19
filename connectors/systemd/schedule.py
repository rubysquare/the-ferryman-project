#!/usr/bin/env python3
"""
The Ferryman Project — Linux systemd User Timer Scheduler
Speaks the Dawn Anchor and Dusk Release aloud at set hours via user-level systemd.

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
SYSTEMD_USER_DIR = os.path.expanduser("~/.config/systemd/user")
DEFAULTS: Dict[str, str] = {"dawn": "07:00", "dusk": "21:30"}
WINDOW_MINUTES = 90


def service_name(crossing: str) -> str:
    return f"ferryman-{crossing}.service"


def timer_name(crossing: str) -> str:
    return f"ferryman-{crossing}.timer"


def service_path(crossing: str) -> str:
    return os.path.join(SYSTEMD_USER_DIR, service_name(crossing))


def timer_path(crossing: str) -> str:
    return os.path.join(SYSTEMD_USER_DIR, timer_name(crossing))


def generate_service_content(crossing: str, at: str) -> str:
    start = datetime.strptime(at, "%H:%M")
    end = start + timedelta(minutes=WINDOW_MINUTES)
    window = f"{start:%H:%M}-{end:%H:%M}"
    return f"""[Unit]
Description=The Ferryman Project — {crossing.capitalize()} Crossing
Documentation=https://github.com/the-ferryman-project

[Service]
Type=oneshot
ExecStart={sys.executable} {FERRYMAN} {crossing} --voice --window {window}
"""


def generate_timer_content(crossing: str, at: str) -> str:
    return f"""[Unit]
Description=The Ferryman Project — {crossing.capitalize()} Timer

[Timer]
OnCalendar=*-*-* {at}:00
Persistent=false

[Install]
WantedBy=timers.target
"""


def install(times: Dict[str, str]) -> None:
    if shutil.which("systemctl") is None:
        sys.stderr.write("Notice: systemctl command not found. This scheduler requires a Linux system with systemd.\n")
        return

    os.makedirs(SYSTEMD_USER_DIR, exist_ok=True)
    for crossing, at in times.items():
        # Write .service
        with open(service_path(crossing), "w", encoding="utf-8") as f:
            f.write(generate_service_content(crossing, at))

        # Write .timer
        with open(timer_path(crossing), "w", encoding="utf-8") as f:
            f.write(generate_timer_content(crossing, at))

    # Reload and enable
    subprocess.run(["systemctl", "--user", "daemon-reload"], check=False)
    for crossing in times:
        subprocess.run(["systemctl", "--user", "enable", "--now", timer_name(crossing)], check=False)
        print(f"Installed {crossing}: {times[crossing]} (systemd timer)")


def status() -> None:
    print("=== Ferryman systemd Status ===")
    if shutil.which("systemctl") is None:
        sys.stderr.write("Notice: systemctl command not found. This scheduler requires a Linux system with systemd.\n")
        return

    res = subprocess.run(
        ["systemctl", "--user", "list-timers", "--all"],
        capture_output=True,
        text=True,
        check=False
    )
    for crossing in DEFAULTS:
        t_name = timer_name(crossing)
        if t_name in res.stdout:
            print(f"{crossing}: Active in systemd timers")
        elif os.path.exists(timer_path(crossing)):
            print(f"{crossing}: Unit file exists but timer is not active")
        else:
            print(f"{crossing}: Not installed")


def uninstall() -> None:
    has_systemctl = shutil.which("systemctl") is not None
    for crossing in DEFAULTS:
        if has_systemctl:
            subprocess.run(["systemctl", "--user", "disable", "--now", timer_name(crossing)], check=False)
        for path in (service_path(crossing), timer_path(crossing)):
            if os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass
    if has_systemctl:
        subprocess.run(["systemctl", "--user", "daemon-reload"], check=False)
    print("Uninstalled all Ferryman systemd units.")


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
