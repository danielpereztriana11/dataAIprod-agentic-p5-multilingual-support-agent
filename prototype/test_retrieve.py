import unittest
from unittest.mock import patch

import retrieve


class SemanticRetrievalTests(unittest.TestCase):
    def setUp(self):
        self.chunks = [
            {"article": "A", "section": "One", "text": "first"},
            {"article": "B", "section": "Two", "text": "second"},
        ]
        self.state = patch.multiple(retrieve, _CHUNKS=self.chunks, _VEC=object(), _EMBED_CACHE=([[1, 0], [0, 1]], [0, 1]))
        self.state.start()
        self.addCleanup(self.state.stop)

    @patch("retrieve._embed", return_value=[[1, 0]])
    def test_clear_match(self, _embed):
        self.assertEqual(retrieve.semantic_top_k("query")[0]["article"], "A")

    @patch("retrieve._embed", return_value=[[1, 1]])
    def test_ambiguous_match_is_not_returned(self, _embed):
        self.assertEqual(retrieve.semantic_top_k("query"), [])

    @patch("retrieve._embed", side_effect=OSError("offline"))
    def test_model_unavailable_fails_closed(self, _embed):
        self.assertEqual(retrieve.semantic_top_k("query"), [])


if __name__ == "__main__":
    unittest.main()

class RerankTests(unittest.TestCase):
    @patch.dict('os.environ', {'OLLAMA_MODEL': 'test'})
    @patch('draft._ollama', return_value='KB-OTHER-99')
    def test_unknown_model_choice_is_rejected(self, _model):
        candidates = [{'article': 'KB-ONE-01', 'section': 'Steps', 'text': 'A'}]
        self.assertIsNone(retrieve._rerank_uncertain('question', candidates))

    @patch.dict('os.environ', {'OLLAMA_MODEL': 'test'})
    @patch('draft._ollama', return_value='KB-ONE-01')
    def test_valid_model_choice_is_returned(self, _model):
        candidates = [{'article': 'KB-ONE-01', 'section': 'Steps', 'text': 'A'}]
        self.assertEqual(retrieve._rerank_uncertain('question', candidates), candidates[0])
