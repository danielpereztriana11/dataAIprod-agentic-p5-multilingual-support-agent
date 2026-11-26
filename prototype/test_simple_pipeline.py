import unittest
from unittest.mock import patch
import simple_pipeline as simple

PASSAGES = [{"article": "KB-TEST-01", "section": "Steps", "text": "Open the menu.", "score": 0.8}]
ROUTINE = {"language": "en", "lang_conf": 0.9, "category": "how_do_i", "cat_conf": 0.9}

class SimpleWorkflowTests(unittest.TestCase):
    @patch("simple_pipeline.policy.check", return_value=("pass", ""))
    @patch("simple_pipeline.draft.draft", return_value="Open the menu. [KB-TEST-01 · Steps]")
    @patch("simple_pipeline.retrieve.top_k", return_value=PASSAGES)
    @patch("simple_pipeline.router.predict", return_value=ROUTINE)
    def test_routine_request_is_answered(self, *_mocks):
        out = simple.run_one("How do I open the menu?")
        self.assertEqual(out["decision"], "draft")
        self.assertEqual(out["send"], "L3")

    @patch("simple_pipeline.router.predict", side_effect=AssertionError("must not call model"))
    def test_sensitive_and_certificate_are_handed_off(self, _model):
        for question in ("Please change my grade", "Where is my certificate?"):
            self.assertEqual(simple.run_one(question)["decision"], "escalate")

    @patch("simple_pipeline.router.predict", return_value={"language": "pl", "lang_conf": 0.9, "category": "how_do_i", "cat_conf": 0.9})
    def test_polish_is_off(self, _model):
        self.assertEqual(simple.run_one("test")["decision"], "escalate")

    @patch("simple_pipeline.router.predict", return_value=ROUTINE)
    @patch("simple_pipeline.retrieve.top_k", return_value=[])
    def test_no_source_hands_off(self, *_mocks):
        self.assertEqual(simple.run_one("test")["decision"], "escalate")

    @patch("simple_pipeline.router.predict", side_effect=ValueError("invalid"))
    def test_router_failure_hands_off(self, _model):
        self.assertEqual(simple.run_one("test")["decision"], "escalate")


if __name__ == "__main__":
    unittest.main()
