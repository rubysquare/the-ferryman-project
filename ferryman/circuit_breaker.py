"""
The Ferryman Project — Anti-Binge Circuit Breaker
Protects the user from treating the Ferryman as an intellectual dopamine dispenser,
search engine, or chat companion. Enforces the Anti-Engagement Principle (AGENTS.md).
"""

import re
from typing import List, Tuple

# Patterns indicating intellectual rumination, advice-seeking, or treating Ferryman as an LLM/chatbot
ADVICE_SEEKING_PATTERNS = [
    r"\b(?:need|want|give me|tell me|show me|seeking|looking for|got any|any)\b.*\b(?:tips|advice|steps|recommendations|hacks|guidance|suggestions)\b",
    r"\b(?:tips|advice|guidance|recommendations)\s+(?:on|for|about|with)\b",
    r"\bwhat (?:are|is) (?:some |the |any )?(?:tips|advice|ways|steps|recommendations)\b",
    r"\b(?:how (?:do|can|should) i|what should i|what can i do)\b",
    r"\b(?:best way to|how to)\s+(?:deal with|handle|cope with|fix|solve|stop|overcome|manage|live|breathe|sleep|relax|calm)\b",
    r"\b(?:tell me|guide me on)\s+(?:what to do|how to)\b",
    r"\bhelp me (?:with|to|figure out|solve)\b",
    r"\b(?:teach me|write (?:me )?(?:an essay|a poem|a story|a summary|code))\b",
    r"\b(?:can you|could you|please)\s+(?:explain|analyze|summarize|help|guide|teach|tell|recommend|suggest)\b",
    r"\b(?:explain|analyze|summarize)\s+(?:to me|for me|the meaning|why|how|what|the concept|hesse|siddhartha)\b",
    r"\b(?:what do you think|solve this for me|coach me)\b",
    r"\b(?:what is the meaning of|who (?:is|was) (?:vasudeva|siddhartha|hesse))\b",
    r"\b(?:10 tips|5 tips|best way to|life advice)\b",
]

CIRCUIT_BREAKER_MESSAGE = """
=== THE FERRYMAN'S BOUNDARY ===
You are seeking more words, more tips, and more answers.
Knowledge can be spoken, but wisdom must be lived.
The ferryman does not lecture; he rows.

We are moving into the head and away from reality.
You have enough information; what you need now is stillness and action.
Step away from the screen. Your answers are out there in your direct experience.
"""


def is_advice_seeking(text: str) -> bool:
    """
    Analyzes input text to determine if the user is seeking advice,
    philosophical debate, or treating the tool as a chatbot.
    """
    if not text:
        return False

    cleaned = text.strip().lower()

    # Direct keyword matches
    direct_triggers = {"tips", "advice", "help", "chat", "ask", "guide", "explain"}
    if cleaned in direct_triggers:
        return True

    # Regex pattern checks
    for pattern in ADVICE_SEEKING_PATTERNS:
        if re.search(pattern, cleaned):
            return True

    return False


def get_boundary_message() -> str:
    """Returns the standardized circuit breaker boundary text."""
    return CIRCUIT_BREAKER_MESSAGE.strip()
