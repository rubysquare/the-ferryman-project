# The Ferryman Project: AI Handoff & Continuity Brief

> **Context for Incoming AI Agents:**  
> This project was initialized to create an open-source, anti-monetization, anti-engagement lifeline for grounded consciousness, inspired by Hermann Hesse’s *Siddhartha*. Read [`AGENTS.md`](./AGENTS.md) before writing any code.

---

## 1. Project Status & Current State

- **Repository Root:** `the-ferryman-project`
- **Core Philosophy Guide:** Written and approved at [`docs/modern_siddhartha_guide.md`](./docs/modern_siddhartha_guide.md).
- **Core Engine Prototype:** [`ferryman.py`](./ferryman.py) is a working, dependency-free Python 3 CLI implementing:
  - **Dawn Anchor:** 90-second morning somatic check + single intention prompt.
  - **Midday Pause (SOS):** 30-second sensory grounding (feet, breath, 3 physical objects).
  - **Dusk Release:** 3-minute evening unburdening of unfinished mental baggage.
  - **Circuit Breaker:** Hard stop triggered when users attempt to treat the AI as an endless chat/advice machine.
  - **Local Storage:** Logs stored in `~/.ferryman_log.json` (mode 0600) with zero network calls.
  - **Voice Mode (2026-09-19):** `--voice` speaks every line through macOS `say`. With no keyboard attached it asks, leaves a silence, and closes without logging.
- **Connectors (2026-09-19):** [`connectors/launchd/schedule.py`](./connectors/launchd/schedule.py) installs spoken Dawn/Dusk LaunchAgents; [`connectors/README.md`](./connectors/README.md) has the Siri Shortcut recipe. `--window HH:MM-HH:MM` keeps a late-waking machine silent.

---

## 2. Immediate Next Steps / Roadmap

Incoming agents can assist with any of the following tasks while strictly adhering to [`AGENTS.md`](./AGENTS.md):

### Task A: Voice & Audio Interfaces (Zero-Screen Priority)
- **Done:** spoken output via native OS engines: macOS `say`, Linux `spd-say` & `espeak-ng`/`espeak`, and Windows PowerShell `System.Speech` (zero dependencies across all platforms).
- **Done:** extensive ANSI escape cleaning and markdown parsing for synthesized speech.
- **Open:** spoken *input*. Offline speech-to-text (`whisper.cpp` / `faster-whisper`) and a warmer voice (`piper-tts`) would break the "dependency-free" rule in `CLAUDE.md`, so they must be strictly optional add-ons, never required. Decide first whether a spoken answer needs capturing at all; the headless crossings work without it.

### Task B: Low-Friction Connectors
- **Done:** Siri / Apple Shortcuts recipes (`connectors/shortcuts/`).
- **Open (needs the founder's decision):** Telegram / Signal bot. It adds a network dependency and lives on the phone; weigh it against Guardrail 2 before building.

### Task C: Daily Scheduling Automations
- **Done:** macOS `launchd` (`connectors/launchd/schedule.py`).
- **Done:** Linux `systemd` user timer (`connectors/systemd/schedule.py`).
- **Done:** Universal POSIX `crontab` (`connectors/cron/schedule.py`).
- **Done:** Comprehensive unit test suite covering all connectors (`tests/test_launchd.py`, `tests/test_systemd.py`, `tests/test_cron.py`, `tests/test_shortcuts.py`).

### Verification & Proofs
- **Done:** Formal architectural proofs written in [`docs/architectural_proofs.md`](./docs/architectural_proofs.md) proving bounded execution, somatic primacy, zero network egress, temporal decidability, and non-blocking headless liveness.
- **Done:** 97 unit tests verifying type safety, boundary values, circuit breaker false-positive & false-negative avoidance, atomic & concurrent storage with symlink preservation, cross-platform voice engines, and connector generation.

### Housekeeping
- **Done (2026-09-19):** AGPLv3 `LICENSE` added; local git repository initialised (no remote).
- **Open (needs the founder's decision):** where, and whether, to publish the repository.

---

## 3. How to Verify Any Work You Do

Before completing any task, run:
```bash
# Verify the CLI prototype executes cleanly without errors:
python3 ferryman.py
python3 ferryman.py dawn
python3 ferryman.py pause
python3 ferryman.py dusk
python3 ferryman.py tips

# Headless pass (no keyboard, as launchd and Siri run it). Must not hang:
for c in "" dawn pause dusk tips; do python3 ferryman.py $c </dev/null; done
```

Check:
1. Did you add unnecessary cloud dependencies or telemetry? (If yes, remove them).
2. Did you create any feature that encourages the user to stay on the screen longer? (If yes, remove it).
