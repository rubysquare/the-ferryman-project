"""
Unit tests for connectors/shortcuts/generate_shortcut.py
"""

import io
import unittest
from unittest.mock import patch

from connectors.shortcuts.generate_shortcut import generate_recipes


class TestShortcuts(unittest.TestCase):

    def test_generate_recipes_output(self) -> None:
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            generate_recipes()
        out = buf.getvalue()
        self.assertIn("=== Apple Shortcuts / Siri Recipes ===", out)
        self.assertIn("1. 'Knot' (Midday Pause / SOS):", out)
        self.assertIn("pause --voice", out)
        self.assertIn("2. 'Dawn Anchor':", out)
        self.assertIn("dawn --voice", out)
        self.assertIn("3. 'Dusk Release':", out)
        self.assertIn("dusk --voice", out)
        self.assertIn("Hey Siri, Knot", out)


if __name__ == "__main__":
    unittest.main()
