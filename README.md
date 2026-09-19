# The Ferryman Project

<p align="center">
  <img src="https://raw.githubusercontent.com/rubysquare/the-ferryman-project/main/docs/assets/ferryman_banner.png" alt="The Ferryman Project" width="600" onerror="this.style.display='none'"/>
</p>

<p align="center">
  <em>"Wisdom is not expressible in words... One can find it, live it, be fortified by it, do wonders through it, but one cannot express and teach it."</em><br/>
  — <strong>Hermann Hesse, <em>Siddhartha</em></strong>
</p>

<p align="center">
  <a href="#the-5-immutable-guardrails"><img src="https://img.shields.io/badge/guardrails-5%20immutable-blueviolet.svg" alt="5 Guardrails"/></a>
  <a href="#the-anti-monetization-pledge"><img src="https://img.shields.io/badge/license-AGPLv3-blue.svg" alt="AGPLv3 License"/></a>
  <a href="#quickstart--installation"><img src="https://img.shields.io/badge/dependencies-0%20external-brightgreen.svg" alt="Zero External Dependencies"/></a>
  <a href="#quickstart--installation"><img src="https://img.shields.io/badge/python-3.8%2B-blue.svg" alt="Python 3.8+"/></a>
  <a href="#data-sovereignty--local-storage"><img src="https://img.shields.io/badge/telemetry-zero-success.svg" alt="Zero Telemetry"/></a>
</p>

---

**The Ferryman Project** is an open-source, non-extractive digital public good. It is an analog-first lifeline for grounded consciousness and self-mastery in a hyper-stimulated, algorithmically driven world.

It is **not** an app designed to maximize your screen time, sell you subscriptions, or trap you in your head. Like Vasudeva the ferryman in Hermann Hesse's *Siddhartha*, its sole purpose is to row you across the daily river, anchor you in your body, and get you back into the physical world as quickly as possible.

**The primary metric of success is how quickly you close the terminal.**

---

## The Modern Siddhartha Philosophy

In *Siddhartha*, the seeker discovers that no guru, dogma, or intellectual discipline can grant him peace. He must journey through four archetypes:

```
                  ┌───────────────────────────────┐
                  │ 1. The Brahmin (The Intellect) │
                  │ Theories, books, paradigms    │
                  │ Pitfall: Analysis paralysis   │
                  └───────────────┬───────────────┘
                                  │
                                  ▼
                  ┌───────────────────────────────┐
                  │ 2. The Samana (The Will)      │
                  │ Fasting, monk mode, control   │
                  │ Pitfall: Spiritual ego & guilt│
                  └───────────────┬───────────────┘
                                  │
                                  ▼
                  ┌───────────────────────────────┐
                  │ 3. The Merchant & Lover       │
                  │ Ambition, money, status       │
                  │ Pitfall: Existential nausea   │
                  └───────────────┬───────────────┘
                                  │
                                  ▼
                  ┌───────────────────────────────┐
                  │ 4. The Ferryman (Integration) │
                  │ Somatic presence, simplicity  │
                  │ Synthesis: Grounded in life   │
                  └───────────────────────────────┘
```

When asked what skills he brought to the marketplace, Siddhartha replied:

$$\text{"I can think. I can wait. I can fast."}$$

In the 21st century, these three ancient capacities are the ultimate superpowers:
1. **"I can think"** — Discerning clear signal from algorithmic noise and social conditioning.
2. **"I can wait"** — Reclaiming boredom tolerance and emotional poise without sub-second dopamine.
3. **"I can fast"** — Fasting not only from food, but from feeds, outrage, distraction, and the urge to endlessly consume information.

The Ferryman does not teach these; it creates the quiet physical space for you to practice them.

---

## The 5 Immutable Guardrails

Any modification to this codebase that violates these five tenets is considered a defect and will be rejected:

### 1. The Anti-Monetization Pledge
- **No Paywalls or Subscriptions:** Clarity will never be gatekept behind a paywall.
- **No Venture Capital Metrics:** Zero optimization for retention, conversion funnels, or "lifetime value" (LTV).
- **At-Cost / Zero-Cost Forever ($0.00):** Runs completely offline for $0.00, or via Bring-Your-Own-Key (BYOK) for raw API cents per month.
- **Copyleft Freedom:** Permanent [AGPLv3](./LICENSE) prevents closing or wrapping in proprietary wrappers.

### 2. The Anti-Engagement Principle
- **Success = Time Spent Away from the Screen:** The faster you step back into physical reality, the better the tool worked.
- **Zero Gamification:** No streaks, badges, points, XP, or levels. Streaks weaponize anxiety and guilt.
- **The Circuit Breaker:** If you try to binge-chat or ruminate, the engine terminates the session immediately.

### 3. Somatic & Embodied Primacy
- **The Body Precedes the Intellect:** Never dispense cognitive advice while the user is physically dysregulated.
- **Mandatory Anchors:** Always prompts the user to check their breath, jaw, shoulders, and feet before reflection.

### 4. Absolute Privacy & Zero Data Harvesting
- **Local-First by Default:** All reflections and check-ins are stored in `~/.ferryman_log.json` with strict POSIX permissions (`0600`).
- **Zero Telemetry:** No Google Analytics, PostHog, Mixpanel, Sentry beacons, or cloud egress.

### 5. The Ferryman Demeanor
- **Tone:** Quiet, unhurried, grounded, humble, and sparse.
- **No Gimmicks:** No cheerleading ("You've got this!"), no corporate wellness jargon, and no unsolicited lecturing.

---

## The Three Daily Crossings

The Ferryman operates across three distinct, time-capped intervals:

```
┌─────────────────────────┐   ┌─────────────────────────┐   ┌─────────────────────────┐
│       Dawn Anchor       │   │   Midday Pause (SOS)    │   │      Dusk Release       │
│        90 Seconds       │   │        30 Seconds       │   │        3 Minutes        │
│   Somatic + Intention   │   │  Sensory Grounding Loop │   │   Unburden & Let Go     │
└─────────────────────────┘   └─────────────────────────┘   └─────────────────────────┘
```

### 1. Dawn Anchor (90 Seconds)
```bash
ferryman dawn
```
- **Somatic Check:** Unclench jaw, drop shoulders, breathe into the belly.
- **Single Question:** *"What is the single essential thing you must honor today?"*
- **The Cutoff:** Records your answer, gives a grounded blessing, and closes. No endless conversation.

### 2. Midday Pause / SOS (30 Seconds)
```bash
ferryman pause
# aliases: ferryman sos, knot, midday
```
- **Sensory Grounding:** Feet planted, long exhale, name 3 physical objects in your immediate room.
- **Refusal to Analyze:** The Ferryman refuses to entertain your mental spirals. It anchors your nervous system and sends you back to work.

### 3. Dusk Release (3 Minutes)
```bash
ferryman dusk
# aliases: ferryman night, release
```
- **Unburdening:** *"What is unfinished or heavy from today that can be laid down?"*
- **The River Perspective:** Reminds you that today's mistakes and triumphs are water flowing past.
- **Night Instruction:** Step away from all screens, disconnect, and rest.

### 4. The Circuit Breaker (Anti-Binge Rule)
```bash
ferryman tips
# aliases: ferryman chat, ask, help
```
If you treat the Ferryman as an intellectual chat engine or search engine, it immediately triggers a hard stop:
> *"We are moving into the head and away from reality. You have enough information; what you need now is stillness and action. Close this window and return to your life."*

---

## Quickstart & Installation

The Ferryman has **zero external dependencies** and runs on pure Python 3.8+. Choose whichever installation method suits your workflow:

### Option 1: Standalone Install Script (Recommended)

Zero friction, no virtual environments, no `pip` or PEP 668 issues. Installs cleanly to `~/.local/bin/ferryman`:

```bash
# Direct install via curl:
curl -fsSL https://raw.githubusercontent.com/rubysquare/the-ferryman-project/main/install.sh | sh

# Or from a cloned repository:
./install.sh
```

To uninstall at any time:
```bash
./install.sh --uninstall
```

### Option 2: Python Package (pip / pipx)

```bash
# Using pipx (recommended for isolated CLI tools):
pipx install git+https://github.com/rubysquare/the-ferryman-project.git

# Or standard pip:
pip install .
```

### Option 3: Homebrew (macOS / Linux)

```bash
# From tap (recommended once published):
brew tap rubysquare/the-ferryman-project
brew install ferryman

# Or directly from the formula template (after release archive is created):
brew install --formula Formula/ferryman.rb
```

### Option 4: Direct Clone & Run

```bash
git clone https://github.com/rubysquare/the-ferryman-project.git
cd the-ferryman-project
python3 ferryman.py
```

---

## CLI Usage & Options

```
Usage:
  ferryman [command] [options]

Commands:
  dawn, morning, anchor     90s morning somatic check + single intention
  pause, sos, knot, midday  30s somatic circuit-breaker (grounding)
  dusk, night, release      3m evening unburdening of mental baggage
  tips, chat, ask, help     Anti-binge circuit-breaker test
  status, log               View your local private crossing log
  clear-log                 Wipe your local log (data sovereignty)

Options:
  --voice                   Speak aloud with offline system voice (say / spd-say / espeak)
  --window HH:MM-HH:MM      Run only if current time is within this interval (silent otherwise)
  --rate WPM                Speech rate in words per minute (default: 160)
  --fast                    Disable character-by-character typing delay
  --version                 Display version information
  -h, --help                Show this help message
```

### Zero-Screen Voice Mode

Run Ferryman with your eyes closed:

```bash
ferryman dawn --voice
```

The Ferryman leverages built-in, offline speech synthesis with zero external dependencies:
- **macOS:** Native `say`
- **Linux:** Native `spd-say` or `espeak-ng` / `espeak`
- **Windows:** Native PowerShell `System.Speech.Synthesis.SpeechSynthesizer`

In headless mode (e.g. triggered without a terminal keyboard), the voice speaks the prompt, waits in quiet contemplation, and cleanly terminates without blocking or hanging.

---

## Zero-Screen Connectors

Automate your crossings so you never even have to open a terminal:

| Connector | Platform | Description | Guide |
| :--- | :--- | :--- | :--- |
| **macOS `launchd`** | macOS | Daily spoken crossings via launchd daemon | [`connectors/launchd/`](./connectors/launchd/) |
| **Linux `systemd`** | Linux | User timer for scheduled Dawn/Dusk prompts | [`connectors/systemd/`](./connectors/systemd/) |
| **POSIX `cron`** | Universal Unix | Standard crontab integration | [`connectors/cron/`](./connectors/cron/) |
| **Siri Shortcuts** | macOS / iOS | Voice-activated SOS pause via Siri ("Hey Siri, Midday Pause") | [`connectors/shortcuts/`](./connectors/shortcuts/) |

### Time Windowing (`--window HH:MM-HH:MM`)

Connectors use time windowing to ensure your machine stays silent if you wake up late:

```bash
# Only speaks if the current time is between 06:00 and 08:30:
ferryman dawn --voice --window 06:00-08:30
```

---

## Data Sovereignty & Local Storage

Your reflections belong strictly to you.

- **Storage Location:** `~/.ferryman_log.json`
- **POSIX Permissions:** Created with mode `0600` (read/write only by owner).
- **Atomic Writes:** File updates are written to an atomic temporary file before replacing the target, preventing data corruption during power loss or abrupt exits.
- **Symlink Protection:** Resolves real filesystem paths before writing, preventing symlink attacks.
- **Data Sovereignty:** Wipe your log at any time with `ferryman clear-log`.
- **Zero Cloud Egress:** Not a single byte ever leaves your machine.

---

## Formal Architectural Proofs

The Ferryman Project is mathematically verified against its alignment guardrails. See [Formal Architectural Proofs](./docs/architectural_proofs.md) for complete specifications and proofs:

- **Theorem 1 (Anti-Engagement):** Every execution path $\pi$ is strictly acyclic and bounded ($|\pi| \le 5$).
- **Theorem 2 (Somatic Primacy):** The somatic state must precede every reflective inquiry state ($\forall \pi, \text{pos}(S_{\text{SOMATIC}}) < \text{pos}(S_{\text{INQUIRY}})$).
- **Theorem 3 (Zero Network Egress):** The transition alphabet $\Gamma$ contains strictly empty network operations ($\Sigma_{\text{net}} = \emptyset$).
- **Theorem 4 (Temporal Decidability):** Window evaluation terminates in $O(1)$ time with no indeterminate states.
- **Theorem 5 (Headless Liveness):** When run without a terminal, the engine guarantees non-blocking termination without deadlock.

---

## Contributing & Governance

We welcome contributions that preserve the sanctuary of human attention.

- Read [AGENTS.md](./AGENTS.md) for our AI and contributor constitution.
- Read [CONTRIBUTING.md](./CONTRIBUTING.md) for our **Anti-Feature Charter** and **Rejection-by-Design Checklist**.
- All bug reports and feature proposals are managed through GitHub issue templates (`.github/ISSUE_TEMPLATE/`).

---

## License

[AGPLv3](./LICENSE) — GNU Affero General Public License v3 or later.

This software is free as in freedom. It cannot be privatized, closed-sourced, or wrapped in proprietary paywalls. If you share or modify this code, your changes must remain open under the same license.
