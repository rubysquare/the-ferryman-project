"""
Unit tests for ferryman/circuit_breaker.py
"""

import unittest
from ferryman.circuit_breaker import is_advice_seeking, get_boundary_message


class TestCircuitBreaker(unittest.TestCase):

    def test_direct_triggers(self) -> None:
        triggers = ["tips", "advice", "help", "chat", "ask", "guide", "explain"]
        for word in triggers:
            with self.subTest(word=word):
                self.assertTrue(is_advice_seeking(word))
                self.assertTrue(is_advice_seeking(f"  {word.upper()}  "))

    def test_advice_seeking_patterns(self) -> None:
        queries = [
            "give me 5 tips to fix my focus",
            "tell me advice on life",
            "show me recommendations for meditation",
            "what should I do right now?",
            "how do I overcome anxiety?",
            "how can I meditate better?",
            "explain the meaning of the river",
            "summarize Hesse's Siddhartha",
            "teach me how to breathe",
            "write an essay about presence",
            "write me a poem about water",
            "can you explain the concept of non-attachment?",
            "what do you think about my problem?",
            "best way to stop overthinking",
            "10 tips for better sleep",
            "can you help me with this decision?"
        ]
        for query in queries:
            with self.subTest(query=query):
                self.assertTrue(is_advice_seeking(query))

    def test_valid_reflections_not_flagged(self) -> None:
        valid_inputs = [
            "finish the report with presence",
            "tightness in my jaw",
            "chest feels constricted",
            "silence",
            "be gentle with colleagues today",
            "unfinished code review",
            "",
            "Explain the project to my team",
            "Analyze customer data for quarterly review",
            "Summarize client feedback for the meeting",
            "Help Sarah with onboarding tomorrow",
            "Finish explaining the architecture"
        ]
        for val in valid_inputs:
            with self.subTest(val=val):
                self.assertFalse(is_advice_seeking(val))

    def test_adversarial_and_nuanced_patterns(self) -> None:
        advice_queries = [
            "My jaw is tight and also what are tips for anxiety?",
            "I need advice on handling anxiety",
            "Any tips for sleep?",
            "What are some tips for staying calm?",
            "How to stop overthinking?",
            "What should I focus on?",
            "Tell me what to do",
            "What is the meaning of life?",
            "Who was Siddhartha?",
            "Got any tips for meditation?",
            "Help me solve this conflict",
            "What do you think",
        ]
        for query in advice_queries:
            with self.subTest(query=query):
                self.assertTrue(is_advice_seeking(query))

        personal_intentions = [
            "Teach my daughter how to ride a bike",
            "Write an email to Sarah about the contract",
            "Guide the new hire through their first day",
            "Help my coworker with the migration",
        ]
        for intention in personal_intentions:
            with self.subTest(intention=intention):
                self.assertFalse(is_advice_seeking(intention))

    def test_boundary_message(self) -> None:
        msg = get_boundary_message()
        self.assertIn("THE FERRYMAN'S BOUNDARY", msg)
        self.assertIn("The ferryman does not lecture; he rows.", msg)
        self.assertIn("Step away from the screen", msg)


if __name__ == "__main__":
    unittest.main()
