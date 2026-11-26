import unittest

import route_rule


class UncertainLanguageTests(unittest.TestCase):
    def test_unconfirmed_language_is_handed_off(self):
        r = {"language": "es", "lang_conf": 0.41, "cat_conf": 0.8, "category": "how_do_i"}
        self.assertEqual(route_rule.decide(r, "question")[0], "escalate")

    def test_agreement_allows_normal_routing(self):
        r = {"language": "es", "lang_conf": 0.41, "language_confirmed": True, "cat_conf": 0.8, "category": "how_do_i"}
        self.assertEqual(route_rule.decide(r, "question")[0], "draft")

    def test_polish_remains_off(self):
        r = {"language": "pl", "lang_conf": 0.41, "language_confirmed": True, "cat_conf": 0.8, "category": "how_do_i"}
        self.assertEqual(route_rule.decide(r, "question")[0], "escalate")


if __name__ == "__main__":
    unittest.main()

class UncertainCategoryTests(unittest.TestCase):
    def test_confirmed_routine_can_continue(self):
        r = {"language": "en", "lang_conf": 0.9, "cat_conf": 0.4, "category": "how_do_i", "routine_confirmed": True}
        self.assertEqual(route_rule.decide(r, "how can I open a lesson")[0], "draft")

    def test_sensitive_rule_overrides_routine_confirmation(self):
        r = {"language": "en", "lang_conf": 0.9, "cat_conf": 0.4, "category": "how_do_i", "routine_confirmed": True}
        self.assertEqual(route_rule.decide(r, "please change my grade")[0], "escalate")

    def test_unconfirmed_low_confidence_hands_off(self):
        r = {"language": "en", "lang_conf": 0.9, "cat_conf": 0.4, "category": "how_do_i", "routine_confirmed": False}
        self.assertEqual(route_rule.decide(r, "question")[0], "escalate")
