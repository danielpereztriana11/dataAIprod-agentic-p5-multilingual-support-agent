"""Presentation workflow: route, apply rules, find a source, draft and check."""
import re

import draft
import policy
import retrieve
import route_rule
import router


def run_one(text):
    result = {"language": "other", "decision": "escalate", "send": "person", "reason": "", "draft": "NO_DRAFT", "citations": [], "policy": "not checked"}
    # Treat certificates as human-only, including the gap found in the earlier eval.
    if route_rule.SECURITY.search(text):
        result["reason"] = "security queue"
        return result
    if route_rule.SENSITIVE.search(text) or re.search(r"certificat|certificad|certificate|świadczen|شهادة", text, re.I):
        result["reason"] = "sensitive - person only"
        return result
    try:
        routing = router.predict(text)
        language = routing["language"]
        result["language"] = language
        decision, reason = route_rule.decide(routing, text)
        if decision != "draft":
            result["reason"] = reason
            return result
        passages = retrieve.top_k(text, rerank=False)
        if not passages:
            result["reason"] = "no clear source"
            return result
        answer = draft.draft(text, passages, language)
        if answer == "NO_DRAFT":
            result["reason"] = "no reliable draft"
            return result
        status, why = policy.check(answer, language, passages)
        result["policy"] = status
        if status != "pass":
            result["reason"] = "policy block: " + why
            return result
        result.update(decision="draft", send=route_rule.switch_state(language), draft=answer,
                      citations=[f"{p['article']} · {p['section']} ({p['score']:.2f})" for p in passages])
        return result
    except (OSError, ValueError, TypeError, KeyError):
        result["reason"] = "local model or retrieval unavailable"
        return result
