import unittest
from unittest.mock import patch

import policy


class LanguagePolicyTests(unittest.TestCase):
    def setUp(self):
        self.answer = "Abre My courses para ver tus cursos. [KB-CATALOG-03 · Courses]"
        self.source = [{"article": "KB-CATALOG-03", "section": "Courses"}]

    @patch("policy.router.detect_language", return_value=("fr", 0.51))
    @patch("policy.router.confirm_language", return_value=True)
    def test_confirmed_language_allows_cited_answer(self, _confirm, _detect):
        self.assertEqual(policy.check(self.answer, "es", self.source)[0], "pass")

    @patch("policy.router.detect_language", return_value=("fr", 0.51))
    @patch("policy.router.confirm_language", return_value=False)
    def test_unconfirmed_mismatch_is_blocked(self, _confirm, _detect):
        self.assertEqual(policy.check(self.answer, "es", self.source)[0], "block")

    @patch("policy.router.confirm_language", return_value=True)
    def test_confirmation_does_not_bypass_citation(self, _confirm):
        self.assertEqual(policy.check("Abre My courses.", "es", self.source)[0], "block")


if __name__ == "__main__":
    unittest.main()
