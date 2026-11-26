import os
import unittest
from unittest.mock import patch

import draft

PASSAGES = [{"article": "KB-DEMO-01", "section": "Steps", "text": "Open Settings."}]


class OllamaDraftTests(unittest.TestCase):
    @patch.dict(os.environ, {"OLLAMA_MODEL": "qwen2.5:1.5b"})
    @patch("draft._ollama", side_effect=["Abra Ajustes. [KB-DEMO-01 · Steps]", "YES"])
    def test_local_model_drafts_in_requested_language(self, local_model):
        output = draft.draft("¿Cómo abro ajustes?", PASSAGES, "es")
        self.assertIn("Abra Ajustes", output)
        self.assertIn("Spanish", local_model.call_args_list[0].args[0])

    @patch.dict(os.environ, {"OLLAMA_MODEL": "qwen2.5:1.5b"})
    @patch("draft._ollama", side_effect=OSError("offline"))
    def test_local_model_failure_escalates(self, _local_model):
        self.assertEqual(draft.draft("Question", PASSAGES, "fr"), "NO_DRAFT")

    @patch.dict(os.environ, {"OLLAMA_MODEL": "qwen2.5:1.5b"})
    @patch("draft._ollama", return_value="Je suis désolé, je ne peux pas répondre.")
    def test_refusal_is_handed_off(self, _local_model):
        self.assertEqual(draft.draft("Question", PASSAGES, "fr"), "NO_DRAFT")

    @patch.dict(os.environ, {"OLLAMA_MODEL": "qwen2.5:1.5b"})
    @patch("draft._ollama", side_effect=["Unsupported claim.", "NO"])
    def test_failed_source_check_is_handed_off(self, _local_model):
        self.assertEqual(draft.draft("Question", PASSAGES, "en"), "NO_DRAFT")

    def test_no_source_does_not_generate(self):
        self.assertEqual(draft.draft("Question", [], "en"), "NO_DRAFT")


if __name__ == "__main__":
    unittest.main()
