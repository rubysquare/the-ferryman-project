# The Ferryman Project: Launch & Outreach Kit

This document contains publication-ready copy for launching **The Ferryman Project** across Hacker News, digital minimalism communities, Unix/command-line forums, and long-form essay platforms.

---

## 1. Hacker News ("Show HN")

### Post Details
- **Title:** `Show HN: The Ferryman – An anti-engagement, zero-dependency CLI for grounded presence`
- **URL (leave blank if text post, or submit direct link):** `https://github.com/rubysquare/the-ferryman-project`

### Text Body (First Comment / Post Body)

```text
Hi HN,

I built The Ferryman (https://github.com/rubysquare/the-ferryman-project) out of frustration with commercial "wellness" software. 

Almost every mindfulness app today uses the exact mechanics that drive digital addiction: push notifications, streaks, points, gamified XP, and subscriptions designed to keep you looking at glass. When you're dysregulated or burned out, the last thing you need is another app trying to optimize your retention metrics.

The Ferryman is an open-source, non-extractive digital public good inspired by Vasudeva the ferryman in Hermann Hesse's *Siddhartha*. In the book, the ferryman doesn't lecture, sell dogmas, or keep people on his boat. He listens to the river, rows people across, and lets them go.

Our primary metric of success is how quickly you close the terminal.

### The 3 Daily Crossings

1. Dawn Anchor (90 seconds): A somatic check (unclench jaw, drop shoulders, deep belly breath) followed by a single question: "What is the single essential thing you must honor today?" Records your answer locally, gives a quiet blessing, and terminates.
2. Midday Pause / SOS (30 seconds): When you're spiraling or overwhelmed, `ferryman pause` refuses to engage with your thoughts. It enforces physical grounding: feet flat on the floor, complete exhale with a 3-second hold, and naming 3 physical objects in the room.
3. Dusk Release (3 minutes): Evening unburdening: "What is unfinished or heavy that you can lay down tonight?" Reminds you that the day's market is closed, and to shut down your screens.

### The Circuit Breaker (Anti-Binge Rule)
If you try to treat Ferryman like an AI chatbot or ask for productivity advice (`ferryman tips`), it triggers a hard stop:
"We are moving into the head and away from reality. You have enough information; what you need now is stillness and action. Close this window and return to your life."

### Technical Architecture
- 100% Zero Runtime Dependencies: Pure Python 3.8+ standard library only. No requests, no bloated frameworks, no third-party package trees.
- Zero-Screen Offline Voice: Supports `--voice` out of the box using built-in OS speech synthesis (macOS `say`, Linux `spd-say`/`espeak`, Windows PowerShell `System.Speech`). You can run it with your eyes closed.
- Native Schedulers: Includes zero-dependency scripts for macOS `launchd`, Linux `systemd` user timers, POSIX `cron`, and Apple Shortcuts (Siri: "Hey Siri, Knot").
- Data Sovereignty: All reflections are stored locally in `~/.ferryman_log.json` with strict POSIX `0600` permissions. Writes use atomic temporary files with `fcntl.flock` concurrency locking and symlink preservation.
- Zero Telemetry: No analytics, no tracking pixels, no network egress.
- Formally Verified: We wrote formal proofs (docs/architectural_proofs.md) modeling the system as a bounded DAG (max path length <= 5), proving non-blocking headless liveness, zero network calls, and somatic primacy.
- 107 automated unit tests with 100% pass rate.
- License: AGPLv3.

### Quickstart
```bash
curl -fsSL https://raw.githubusercontent.com/rubysquare/the-ferryman-project/main/install.sh | sh
ferryman dawn
```

Code, documentation, and formal proofs are all on GitHub:
https://github.com/rubysquare/the-ferryman-project

I’d love to hear your thoughts, especially from anyone else trying to design software that deliberately minimizes screen time.
```

---

## 2. Reddit Community Copy

### A. For `r/digitalminimalism` & `r/nosurf`

- **Post Title:** `I built a zero-dependency CLI lifeline to help me step away from screens (The Ferryman)`
- **Body:**

```text
Hi everyone,

Like many here, I’ve tried countless mindfulness, journaling, and habit apps. Almost all of them eventually made my screen addiction worse:
- They use streaks that make you feel guilty if you miss a day.
- They send notifications begging you to come back.
- They encourage endless "intellectualizing" about self-improvement rather than living.

I decided to build the exact opposite: **The Ferryman Project** (https://github.com/rubysquare/the-ferryman-project).

It’s an open-source, non-extractive terminal tool inspired by Hermann Hesse’s *Siddhartha*. Its core design principle is that **success is measured by how quickly you close the terminal.**

### What it does:
1. **Dawn Anchor (90s)**: Drops shoulders, unclimbs jaw, takes one deep breath, asks for one single intention, and immediately closes.
2. **Midday Pause / SOS (30s)**: For when you're overwhelmed or doomscrolling. It refuses to analyze your thoughts. It forces you to put feet on the floor, exhale completely, and name 3 physical objects in the room.
3. **Dusk Release (3m)**: Unburdens whatever mental baggage is lingering from the workday, reminds you that today's mistakes are water under the bridge, and tells you to turn off your devices.
4. **The Circuit Breaker**: If you try to use it to binge-chat or search for advice, it cuts you off with a hard boundary: *"You have enough information; what you need now is stillness and action."*

### Why it’s different:
- **Zero streaks, points, or badges:** Life is not a video game to be optimized.
- **Runs with your eyes closed:** Has a `--voice` mode that speaks prompts aloud using your computer's built-in offline voice (macOS `say`, Linux `spd-say`, Windows `System.Speech`).
- **100% Offline & Private:** Zero external dependencies, zero network requests, zero telemetry. Everything stays in `~/.ferryman_log.json` on your machine.
- **Free as in freedom:** AGPLv3, $0.00 forever.

If you're on Mac or Linux, you can try it with:
```bash
curl -fsSL https://raw.githubusercontent.com/rubysquare/the-ferryman-project/main/install.sh | sh
ferryman dawn
```

The repository and philosophy guide are here:
https://github.com/rubysquare/the-ferryman-project

I hope this helps anyone else looking for a quiet, grounded bridge back to the physical world.
```

---

### B. For `r/commandline` & `r/unixporn`

- **Post Title:** `The Ferryman: An anti-engagement CLI lifeline in pure Python stdlib (0 dependencies, offline voice, launchd/systemd connectors)`
- **Body:**

```text
Hey r/commandline,

I built **The Ferryman** (https://github.com/rubysquare/the-ferryman-project), an open-source CLI designed to anchor presence and deliberately push you *away* from the screen.

Key engineering details:
- **Zero Dependencies**: Pure Python 3.8+ standard library only.
- **Cross-Platform Offline Voice**: `--voice` uses native OS synthesis (macOS `say`, Linux `spd-say` / `espeak-ng`, Windows `System.Speech` via PowerShell). It cleans ANSI escape sequences and extracts markdown links before speaking.
- **Automations**: Native, dependency-free connectors for macOS `launchd` (LaunchAgents), Linux `systemd` user timers, and POSIX `crontab`.
- **Time Windowing (`--window HH:MM-HH:MM`)**: Scheduled daemons stay completely silent if you wake up after your morning window or sleep past night cutoff.
- **Data Sovereignty**: Atomic write replace with POSIX `0600` permissions and `fcntl.flock` concurrency locking; preserves symlinks to cloud-synced folders.
- **Formal Invariants**: Mathematically modeled in `docs/architectural_proofs.md` as an acyclic DAG with bounded execution ($|\pi| \le 5$) and proven headless non-blocking liveness.
- **Test Suite**: 107 automated unit tests.

Install via standalone POSIX script:
```bash
curl -fsSL https://raw.githubusercontent.com/rubysquare/the-ferryman-project/main/install.sh | sh
ferryman --help
```

GitHub: https://github.com/rubysquare/the-ferryman-project
License: AGPLv3
```

---

## 3. Standalone Essay: Substack / Medium / Blog

### Title:
**The Modern Siddhartha: Thinking, Waiting, and Fasting in the Algorithmic Age**

### Subtitle:
*Why the ancient capacities of Hermann Hesse's seeker are the ultimate superpowers against digital capture—and how to build software that lets you walk away.*

### Essay Text:

In Hermann Hesse’s 1922 masterpiece *Siddhartha*, the seeker leaves behind the rigid intellectualism of the Brahmins, the ascetic mortification of the forest Samanas, and the commercial triumphs of the merchant city.

When the wealthy merchant Kamaswami asks Siddhartha what skills he brings to the marketplace, Siddhartha gives an answer that confounds the merchant:

> *"I can think. I can wait. I can fast."*
>
> *"And that is all?"* asked the merchant.
>
> *"I think that is all."*
>
> *"And of what use is that? For example, fasting—what good is it?"*
>
> *"It is of great value, sir. When a person has nothing to eat, fasting is the wisest thing he can do. If Siddhartha had not learned to fast, he would have had to accept any work today, either with you or wherever else, because hunger would have forced him to. But as it is, Siddhartha can wait calmly; he is not impatient, he is not in need, he can let hunger stave off for a long time and laugh at it."*

In the twenty-first century, we live in a marketplace infinitely more predatory than Kamaswami’s bazaar. We are surrounded by algorithms optimized to harvest the scarcest resource on earth: unbroken human attention.

If Siddhartha walked among us today, his three ancient skills would not merely be philosophical curiosities. They would be the ultimate survival kit.

---

### 1. "I Can Think" (Discerning Signal from Conditioning)

To think in the modern era does not mean accumulating more opinions, reading more threads, or absorbing more hot takes. The modern intellectual lives like the Brahmin of Hesse’s first chapter: suffocating under an avalanche of theories, frameworks, and intellectual noise, yet perpetually anxious and disconnected.

Real thinking is subtractive. It is the capacity to sit in quiet contemplation until the conditioned noise of the timeline settles like sediment in a glass of water, leaving only direct, unclouded perception.

If your "thinking" requires constant input from an algorithm, you are not thinking; you are being thought.

---

### 2. "I Can Wait" (Reclaiming Boredom Tolerance)

The modern digital economy is an engine designed to eradicate waiting. A microsecond of boredom at a red light, in an elevator, or between compile runs triggers a Pavlovian reach for the phone.

When you lose the ability to wait, you lose emotional poise. You become reactive, irritable, and easily swayed by the outrage cycle. 

To say *"I can wait"* means reclaiming the dignity of the unoccupied moment. It means being capable of standing in an empty room, feeling your feet on the earth, and breathing without needing a screen to distract you from your own existence.

---

### 3. "I Can Fast" (Abstinence in an Age of Gluttony)

Fasting is not merely abstaining from food. In our world, the most dangerous gluttony is information gluttony.

We binge on notifications, podcasts at 2x speed, endless tabs, and the compulsive urge to consume "just one more tip" that will finally unlock productivity. But knowledge can be spoken; wisdom must be lived.

To fast today means practicing voluntary cognitive deprivation:
- Fasting from feeds.
- Fasting from outrage.
- Fasting from the illusion that more information will solve a problem that requires courage and action.

---

### The River and the Ferryman

At the end of his journey, Siddhartha does not find enlightenment in books, in ascetic starvation, or in worldly wealth. He finds it by the river, working alongside Vasudeva the ferryman.

Vasudeva is not a guru. He has no dogmas, no seminars, and no retention strategies. His work is remarkably simple: he listens to the river, rows travelers across, and lets them go on their way.

When we designed **The Ferryman Project**, we asked ourselves: *What would software look like if it were built in the spirit of Vasudeva?*

1. **It would measure success by how quickly you close it.** Every second you spend looking at our tool instead of living your life is a failure of our design.
2. **It would have zero streaks, badges, or gamification.** Streaks weaponize guilt and loss aversion. Life is a river, not an optimization dashboard.
3. **It would place the body before the mind.** We do not entertain cognitive spirals when your nervous system is dysregulated. We check the jaw, the shoulders, the breath, and the feet first.
4. **It would enforce a circuit breaker.** When you compulsively seek "more tips," it tells you to stop reading and step outside.
5. **It would be free forever.** No paywalls, no venture capital metrics, no telemetry, and zero network calls.

The river is flowing. Step away from your screens, take a breath, and cross.

---

*The Ferryman Project is an open-source, zero-dependency digital public good under AGPLv3.*  
*Repository & Documentation: https://github.com/rubysquare/the-ferryman-project*
