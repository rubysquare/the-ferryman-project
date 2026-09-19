#!/usr/bin/env python3
"""
The Ferryman Project — Apple Shortcuts Helper
Generates ready-to-run shell commands and AppleScript triggers for Siri & Shortcuts.
"""

import os
import sys

FERRYMAN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "ferryman.py"))


def generate_recipes() -> None:
    print("=== Apple Shortcuts / Siri Recipes ===\n")
    print("1. 'Knot' (Midday Pause / SOS):")
    print(f"   Command: /usr/bin/python3 {FERRYMAN} pause --voice\n")
    print("2. 'Dawn Anchor':")
    print(f"   Command: /usr/bin/python3 {FERRYMAN} dawn --voice\n")
    print("3. 'Dusk Release':")
    print(f"   Command: /usr/bin/python3 {FERRYMAN} dusk --voice\n")
    print("Setup instructions:")
    print("1. Open macOS or iOS 'Shortcuts' app.")
    print("2. Create New Shortcut -> Add action 'Run Shell Script'.")
    print("3. Paste the desired command above.")
    print("4. Name the shortcut 'Knot', 'Dawn Anchor', or 'Dusk Release'.")
    print("5. Trigger anytime via 'Hey Siri, Knot'.\n")


if __name__ == "__main__":
    generate_recipes()
