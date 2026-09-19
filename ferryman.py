#!/usr/bin/env python3
"""
The Ferryman Project — Core Prototype
An open-source, anti-engagement lifeline for grounded consciousness.
"""

import sys
import time
import json
import os
import shutil
import subprocess
from datetime import datetime

DATA_FILE = os.path.expanduser("~/.ferryman_log.json")

# Zero-screen mode: lines are spoken with the system's offline voice (macOS `say`).
VOICE = False
VOICE_RATE = "160"  # words per minute; unhurried


def load_log():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_entry(session_type, text):
    log = load_log()
    log.append({
        "timestamp": datetime.now().isoformat(),
        "type": session_type,
        "content": text
    })
    with open(DATA_FILE, "w") as f:
        json.dump(log, f, indent=2)
    # Reflections belong to the human alone
    os.chmod(DATA_FILE, 0o600)


def slow_print(text, delay=0.02):
    if VOICE:
        print(text)
        spoken = text.replace("=", "").strip()
        if spoken:
            subprocess.run(["say", "-r", VOICE_RATE, spoken], check=False)
        return
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def clear_screen():
    # Keep terminal minimal and distraction-free
    if sys.stdout.isatty():
        print("\033c", end="")


def headless():
    # Spoken with no keyboard attached (scheduler, Siri): the answer stays with the human
    return VOICE and not sys.stdin.isatty()


def in_window(window):
    # "07:00-08:30"; may wrap past midnight
    start, end = window.split("-")
    now = datetime.now().strftime("%H:%M")
    if start <= end:
        return start <= now <= end
    return now >= start or now <= end


def dawn_anchor():
    clear_screen()
    slow_print("\n=== THE DAWN ANCHOR ===")
    slow_print("Before we begin: drop your shoulders, unclench your jaw, and let your belly soften.")
    time.sleep(1.5)
    slow_print("Take one slow, deep breath in... and release it all the way down.\n")
    time.sleep(1.5)

    slow_print("What is the single most essential thing you must honor today?")
    if headless():
        time.sleep(20)
        slow_print("Carry it lightly as you cross the river today.")
        slow_print("\nNow step away from screens, and enter your morning.\n")
        return
    try:
        intention = input("\n> ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nTake care.")
        return

    if intention:
        save_entry("dawn", intention)
        print()
        slow_print(f"Understood. Carry '{intention}' lightly as you cross the river today.")
    else:
        slow_print("Silence is also an answer. Walk gently today.")

    time.sleep(1)
    slow_print("\nNow close your terminal, step away from screens, and enter your morning.\n")


def midday_pause():
    clear_screen()
    slow_print("\n=== THE MIDDAY PAUSE (SOS) ===")
    slow_print("Stop reading. We will not analyze your thoughts right now.\n")
    time.sleep(1.0)

    slow_print("1. Place both feet firmly flat on the floor.")
    time.sleep(1.2)
    slow_print("2. Exhale completely until your lungs are empty. Hold for 3 seconds.")
    time.sleep(1.5)
    slow_print("3. Notice 3 physical objects in the room right now (not on a screen).")
    time.sleep(1.5)

    if headless():
        time.sleep(5)
        slow_print("\nYou are back on solid ground. Return to your task one breath at a time.\n")
        return
    try:
        feeling = input("\nIn one word or phrase, what sensation is present in your body right now?\n> ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nBreathe.")
        return

    if feeling:
        save_entry("pause", feeling)
        print()
        slow_print(f"Acknowledge the '{feeling}'. It is just a current passing through.")

    slow_print("\nYou are back on solid ground. Return to your task one breath at a time.\n")


def dusk_release():
    clear_screen()
    slow_print("\n=== THE DUSK RELEASE ===")
    slow_print("The day's market is closed. The river keeps flowing.\n")
    time.sleep(1.0)

    slow_print("What is unfinished, heavy, or lingering from today that you can lay down tonight?")
    if headless():
        time.sleep(30)
        slow_print("Notice: thinking about it now will not solve it tonight.")
        slow_print("You did what you could. What remains belongs to tomorrow.")
        slow_print("\nTurn off your devices. Let your mind settle like still water. Rest.\n")
        return
    try:
        burden = input("\n> ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nRest well.")
        return

    if burden:
        save_entry("dusk", burden)
        print()
        slow_print("Notice: thinking about it now will not solve it tonight.")
        slow_print("You did what you could. What remains belongs to tomorrow.")
    else:
        slow_print("Nothing to carry. A peaceful night.")

    time.sleep(1.0)
    slow_print("\nTurn off this device. Let your mind settle like still water. Rest.\n")


def circuit_breaker():
    clear_screen()
    slow_print("\n=== THE FERRYMAN'S BOUNDARY ===")
    slow_print("You are seeking more words, more tips, and more answers.")
    slow_print("Knowledge can be spoken, but wisdom must be lived.")
    slow_print("The ferryman does not lecture; he rows.")
    slow_print("\nStep away from the screen. Your answers are out there in your direct experience.\n")


def main():
    global VOICE
    args = sys.argv[1:]
    if "--window" in args:
        # Scheduled crossings stay silent if the machine wakes long after the hour
        i = args.index("--window")
        window = args[i + 1] if i + 1 < len(args) else ""
        del args[i:i + 2]
        try:
            if not in_window(window):
                return
        except ValueError:
            pass
    if "--voice" in args or os.environ.get("FERRYMAN_VOICE") == "1":
        args = [a for a in args if a != "--voice"]
        VOICE = shutil.which("say") is not None

    if args:
        cmd = args[0].lower()
        if cmd in ("dawn", "morning", "anchor"):
            dawn_anchor()
            return
        elif cmd in ("pause", "sos", "knot", "midday"):
            midday_pause()
            return
        elif cmd in ("dusk", "night", "release", "evening"):
            dusk_release()
            return
        elif cmd in ("chat", "ask", "help", "tips"):
            circuit_breaker()
            return

    clear_screen()
    print("THE FERRYMAN PROJECT")
    print("An open-source lifeline for grounded presence.")
    print("=" * 45)
    print("1. Dawn Anchor   (90s morning orientation)")
    print("2. Midday Pause  (30s somatic circuit-breaker)")
    print("3. Dusk Release  (3m evening unburdening)")
    print("4. Ask for Tips  (Test the anti-binge rule)")
    print("q. Walk Away")
    print("=" * 45)

    try:
        choice = input("\nChoose your crossing [1-4, q]: ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nWalk in peace.")
        return

    if choice == "1":
        dawn_anchor()
    elif choice == "2":
        midday_pause()
    elif choice == "3":
        dusk_release()
    elif choice == "4":
        circuit_breaker()
    else:
        print("\nStep away and breathe. The river awaits.")


if __name__ == "__main__":
    main()
