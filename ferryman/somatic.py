"""
The Ferryman Project — Somatic & Embodied Primacy
Implements physical grounding routines anchored in physiology (AGENTS.md Guardrail 3).
The body precedes the intellect: physical regulation before cognitive reflection.
"""

from typing import List, Tuple


def get_dawn_somatic_prompt() -> List[str]:
    """Returns the morning somatic orientation prompts."""
    return [
        "Before we begin: drop your shoulders, unclench your jaw, and let your belly soften.",
        "Take one slow, deep breath in... and release it all the way down."
    ]


def get_midday_grounding_steps() -> List[str]:
    """Returns the SOS midday sensory grounding protocol."""
    return [
        "Stop reading. We will not analyze your thoughts right now.",
        "1. Place both feet firmly flat on the floor.",
        "2. Exhale completely until your lungs are empty. Hold for 3 seconds.",
        "3. Notice 3 physical objects in the room right now (not on a screen)."
    ]


def get_dusk_closing_prompt() -> List[str]:
    """Returns the evening unburdening somatic prompts."""
    return [
        "The day's market is closed. The river keeps flowing.",
        "Notice: thinking about it now will not solve it tonight.",
        "You did what you could. What remains belongs to tomorrow.",
        "Turn off your devices. Let your mind settle like still water. Rest."
    ]
