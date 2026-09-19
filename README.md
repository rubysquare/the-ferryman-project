# The Ferryman Project

> *"Wisdom is not expressible in words... One can find it, live it, be fortified by it, do wonders through it, but one cannot express and teach it."*  
> — Hermann Hesse, *Siddhartha*

**The Ferryman Project** is an open-source, non-extractive digital public good. It is designed to be an analog-first lifeline for grounded consciousness and self-mastery in a hyper-stimulated, algorithmically driven world.

It is **not** an app designed to maximize your screen time, sell you subscriptions, or trap you in your head. Like Vasudeva the ferryman, its sole purpose is to row you across the daily river, anchor you in your body, and get you back into the real world as quickly as possible.

---

## The Ferryman Social Contract (Anti-Monetization Pledge)

To prevent this project from falling into the predatory playbook of commercial "wellness tech":

1. **Anti-Engagement by Design:** The Ferryman measures success not by time spent in the system, but by how quickly you close it. 
2. **Zero Gamification:** No streaks, no points, no badges, no guilt. Life is not a game to optimize; it is a river to navigate.
3. **Zero Data Monetization:** All logs, reflections, and somatic check-ins are stored locally or in your private encrypted database. No central server harvests your emotional state.
4. **Permanent Copyleft (AGPLv3):** This software will remain free and open forever. It cannot be privatized, closed-sourced, or wrapped in a predatory paywall.
5. **At-Cost / Bring Your Own Key (BYOK):** Users run it locally for $0.00, or connect their own low-cost API keys (spending pennies a month instead of $100/year subscriptions).

---

## The Three Daily Crossings

The Ferryman interacts with you in three distinct, time-capped intervals:

```
[Dawn Anchor]          [Midday Pause / SOS]           [Dusk Release]
 90 Seconds              30 Seconds                     3 Minutes
 Somatic + Intention     Break the mental loop          Unburden & Sleep
```

### 1. The Dawn Anchor (90 Seconds)
- **Somatic Check:** Unclench jaw, drop shoulders, breathe into the belly.
- **Single Question:** *"What is the single essential thing you must honor today?"*
- **The Cutoff:** Acknowledges your answer and closes. No lingering conversation.

### 2. The Midday Pause (SOS on Demand)
- Triggered by typing or speaking `PAUSE` or `KNOT`.
- The Ferryman **refuses to analyze your thoughts**. Instead, it forces an immediate physical somatic reset: feet on the ground, extended exhale, sensory grounding (5-4-3-2-1).

### 3. The Dusk Release (3 Minutes)
- **Unburdening:** *"What is unfinished or heavy from today that can be laid down?"*
- **The River Perspective:** Mirrors back that your mistakes, triumphs, and struggles were simply water flowing past.
- **Night Instruction:** Disconnect, step away from screens, and rest.

---

## The Circuit Breaker (Anti-Binge Rule)

If you attempt to treat the Ferryman like a search engine or chat companion—asking for 10 tips, intellectual theories, or endlessly ruminating—the system triggers a hard stop:

> *"We are moving into the head and away from reality. You have enough information; what you need now is stillness and action. Close this window and return to your life."*

---

## Project Structure

```
the-ferryman-project/
├── README.md             # Manifesto, architecture, and pledge
├── AGENTS.md             # Guardrails every contributor (human or AI) must follow
├── LICENSE               # AGPLv3
├── ferryman.py           # Self-contained CLI prototype
├── connectors/           # Zero-screen entry points (launchd schedule, Siri Shortcut)
└── docs/                 # The Modern Siddhartha guide
```

---

## Getting Started with the Prototype

Run the local prototype right from your terminal:

```bash
python3 ferryman.py
```

### Without a screen

```bash
python3 ferryman.py dawn --voice
```

Each line is spoken by the offline system voice (macOS `say`). To have Dawn and Dusk spoken at set hours, or to call the Midday Pause through Siri, see [`connectors/`](./connectors/README.md).

---

## License

[AGPLv3](./LICENSE). Free to use, study, change, and share; any version offered to others, including over a network, must stay open under the same terms.
