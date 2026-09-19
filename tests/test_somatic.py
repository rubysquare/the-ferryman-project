"""
Unit tests for ferryman/somatic.py
"""

import unittest
from ferryman.somatic import (
    get_dawn_somatic_prompt,
    get_midday_grounding_steps,
    get_dusk_closing_prompt
)


class TestSomatic(unittest.TestCase):

    def test_dawn_somatic_prompt(self) -> None:
        prompts = get_dawn_somatic_prompt()
        self.assertIsInstance(prompts, list)
        self.assertGreaterEqual(len(prompts), 2)
        full_text = " ".join(prompts)
        self.assertIn("shoulders", full_text)
        self.assertIn("jaw", full_text)
        self.assertIn("breath", full_text)

    def test_midday_grounding_steps(self) -> None:
        steps = get_midday_grounding_steps()
        self.assertIsInstance(steps, list)
        self.assertGreaterEqual(len(steps), 3)
        full_text = " ".join(steps)
        self.assertIn("Stop reading", full_text)
        self.assertIn("feet", full_text)
        self.assertIn("Exhale", full_text)
        self.assertIn("3 physical objects", full_text)

    def test_dusk_closing_prompt(self) -> None:
        prompts = get_dusk_closing_prompt()
        self.assertIsInstance(prompts, list)
        self.assertGreaterEqual(len(prompts), 3)
        full_text = " ".join(prompts)
        self.assertIn("river keeps flowing", full_text)
        self.assertIn("Turn off your devices", full_text)


if __name__ == "__main__":
    unittest.main()
