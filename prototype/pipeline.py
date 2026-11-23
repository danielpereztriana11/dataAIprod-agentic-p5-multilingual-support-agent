"""The workflow: router -> routing rule -> retrieve + draft -> policy check. No loop, no tools."""
import router, route_rule, retrieve, draft as drafter, policy


def run_one(text):
    r = router.predict(text)
    decision, reason = route_rule.decide(r, text)
    passages, out = [], "NO_DRAFT"
    if decision == "draft":
        passages = retrieve.top_k(text)
        out = drafter.draft(text, passages, r["language"])
        if out == "NO_DRAFT":
            decision, reason = "escalate", "no source found"
    status, why = policy.check(out, r["language"], passages)
    if decision == "draft" and status == "block":
        decision, reason = "escalate", "policy block: " + why
    send = route_rule.switch_state(r["language"]) if decision == "draft" else "person"
    # L3: the agent sends with an "AI answer" label · L2: ⊘ a native speaker approves before sending
    return dict(r, decision=decision, send=send, reason=reason, draft=out, policy=status,
                citations=[f"{p['article']} · {p['section']} ({p['score']:.2f})" for p in passages])
