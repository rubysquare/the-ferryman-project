# Contributing to The Ferryman Project

Thank you for your interest in contributing to **The Ferryman Project**.

Before proposing or writing any code, please understand that this repository is not conventional software. It is an open-source, non-extractive digital public good designed to protect **human sovereignty, somatic presence, and freedom from algorithmic capture**.

In Herman Hesse's *Siddhartha*, Vasudeva the ferryman does not lecture, sell dogmas, or keep people trapped on his boat. He listens to the river, rows people across, and lets them go.

Every line of code in this project must honor that same spirit.

---

## 1. The Anti-Feature Charter (What Will Never Be Accepted)

Commercial "wellness" software frequently turns mindfulness into another addiction through gamification, retention funnels, and data harvesting. To protect the integrity of this project, the following features are **strictly prohibited by design**:

| Prohibited Anti-Feature | Rationale |
| :--- | :--- |
| **Streaks, Badges, Points, XP, Leaderboards** | Streaks weaponize anxiety, loss aversion, and neurotic guilt. Life is not an optimization game. |
| **Engagement Re-Notification Loops** | We will never send reminders urging you to "come back" or "keep your streak alive." Automations run only at explicit user-chosen times (Dawn/Dusk). |
| **Conversational Binging / Open Chatbots** | The Ferryman refuses to be an endless advice dispenser. The Circuit Breaker is non-negotiable: intellectual rumination must be stopped and redirected to physical reality. |
| **Centralized Telemetry & Analytics** | No Google Analytics, PostHog, Mixpanel, Sentry beacons, or tracking pixels. Zero telemetry. Logs remain strictly on the user's local machine (`~/.ferryman_log.json`, mode 0600). |
| **Monetization Hooks & Paywalls** | No "pro" versions, no subscriptions, no locked features. The software is AGPLv3 and runs locally for $0.00. |
| **Runtime External Dependencies** | The core engine and CLI must remain 100% zero-dependency Python standard library. No `requests`, no heavy frameworks, no bloated package trees. |

If a proposal or pull request introduces any of the above, it will be politely and immediately closed.

---

## 2. The Rejection-by-Design Checklist

Every issue proposal and pull request is systematically evaluated against these five non-negotiable questions:

1. [ ] **Does this pull the human toward a screen or push them back to physical reality?**  
   *If it increases time spent looking at glass, it is a regression.*
2. [ ] **Does this create user dependency or foster user sovereignty?**  
   *The goal of the Ferryman is to become unnecessary.*
3. [ ] **Could this feature be used to exploit, track, or monetize the user?**  
   *All data must remain strictly local, private, and user-owned.*
4. [ ] **Is the code minimal, readable, and 100% dependency-free?**  
   *Core functionality must rely solely on the Python standard library.*
5. [ ] **Does the body precede the intellect?**  
   *Somatic grounding (breath, jaw, shoulders, feet) must never be bypassed for intellectual analysis.*

---

## 3. How to Propose Changes

### Reporting Bugs
If you find a bug:
1. Check existing GitHub issues to make sure it hasn't already been reported.
2. Open a new issue using the **Bug Report** template.
3. Include your OS, Python version, steps to reproduce, and the observed vs expected behavior.

### Proposing Features or Connectors
Before opening a pull request for a new feature or connector:
1. Open a **Feature Proposal** issue.
2. Complete the mandatory Guardrail Defense section in the issue template.
3. Wait for consensus before investing significant time in implementation.

---

## 4. Development & Coding Standards

- **Python Version:** Compatible with Python 3.8+ (tested on 3.8, 3.9, 3.10, 3.11, 3.12, 3.13).
- **Zero Runtime Dependencies:** Use only the Python standard library for the core package and CLI.
- **Type Annotations:** All new functions and methods must include standard type annotations (`typing`).
- **Quiet Tone:** Adhere to the Ferryman demeanor: sparse, calm, unhurried, without cheerleading, corporate wellness jargon, or lecturing.
- **Security & Privacy:** Local storage must respect POSIX file permissions (`0600`). Never log sensitive user data to world-readable paths.
- **Testing:**
  - Every bug fix or feature must include unit tests in `tests/`.
  - Run the full test suite before submitting:
    ```bash
    python3 -m unittest discover tests
    ```
  - Verify headless execution (stdin redirected from `/dev/null`) does not hang or crash:
    ```bash
    for c in "" dawn pause dusk tips; do python3 ferryman.py $c </dev/null; done
    ```

---

## 5. Community Code of Conduct

We treat each other with the same calm dignity that the Ferryman shows travelers by the river. Be patient, humble, concise, and kind.
