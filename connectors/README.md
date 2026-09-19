# Connectors

Ways to reach the Ferryman without opening a terminal or looking at a screen.
All connectors execute `ferryman.py --voice`, which speaks each line with the system's offline voice (`say` on macOS, `spd-say` or `espeak-ng` on Linux).

When a crossing is spoken with no keyboard attached (headless), it does not prompt you to type. It asks the question, leaves a silence for internal reflection, and closes cleanly. The answer stays with you; nothing is logged.

---

## 1. launchd (macOS Scheduling)

Schedules the Dawn Anchor and Dusk Release as native macOS LaunchAgents.

```bash
# Install with defaults (dawn 07:00, dusk 21:30)
python3 connectors/launchd/schedule.py install

# Custom times
python3 connectors/launchd/schedule.py install --dawn 06:30 --dusk 22:00

# Check status
python3 connectors/launchd/schedule.py status

# Uninstall
python3 connectors/launchd/schedule.py uninstall
```

If the Mac was asleep at the hour, launchd fires the job on wake. A crossing more than 90 minutes late stays silent rather than speaking into an unintended setting.

---

## 2. systemd (Linux User Timers)

Schedules crossings via user-level systemd timers (`~/.config/systemd/user/`).

```bash
python3 connectors/systemd/schedule.py install
python3 connectors/systemd/schedule.py install --dawn 06:30 --dusk 22:00
python3 connectors/systemd/schedule.py status
python3 connectors/systemd/schedule.py uninstall
```

---

## 3. crontab (Universal POSIX Scheduling)

Schedules crossings using standard Unix `crontab`.

```bash
python3 connectors/cron/schedule.py install
python3 connectors/cron/schedule.py install --dawn 06:30 --dusk 22:00
python3 connectors/cron/schedule.py status
python3 connectors/cron/schedule.py uninstall
```

---

## 4. Siri / Apple Shortcuts (On-Demand Voice Lifeline)

Enables invoking the 30-second Midday Pause via voice ("Hey Siri, Knot").
See [`connectors/shortcuts/README.md`](./shortcuts/README.md) for full setup instructions.

```bash
# Test the spoken output manually
python3 ferryman.py pause --voice

# Test the scheduled headless experience (no keyboard)
python3 ferryman.py pause --voice </dev/null
```
