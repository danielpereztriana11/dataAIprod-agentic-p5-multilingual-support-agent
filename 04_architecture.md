# 04 · Architecture — P5 team · Multilingual LMS support agent

> Session 4 deliverable. Due **6 November** in your repo as `04_architecture.md`, with `spec.md` v2 and `evals/tickets_v0.csv` (50 rows).
> Describe the prototype you actually built, not the one you plan. Every line must match something in `/prototype`.

## 1. One-line description
*What the system does, for whom, with what output.*
A support workflow for an ed-tech LMS that answers learners', instructors' and admins' routine "how do I" tickets in their language (en, fr, es, pt, pl, ar) with a reply that cites the English help article — and sends every sensitive, security, unsupported-language or unsure ticket to a native-speaking person.

## 2. The diagram
Draw the flow with boxes and arrows (image, Mermaid, or ASCII). Mark every human checkpoint with **⊘** and the override switch with **⏻**.

```
                         ⏻ switch.json (per language: L3 / L2 / off)
                                  │
ticket ──▶ [1 router] ──▶ [2 routing rule] ──▶ [3 retrieve + draft] ──▶ [4 policy check] ──┬─▶ L3 language: sent with "AI answer" label
           language +       │                    │ no passage → no draft                    │      + "talk to a person"  ⊘ weekly sample
           category +       │                    │                                          └─▶ L2 language: ⊘ native speaker approves ──▶ sent
           confidence       │ language not covered · switch off · security ·               │ block (no citation, promise,
                            │ sensitive (grades, certificates, accessibility,               │        secret, language mismatch)
                            │ personal data) · confidence < 0.50                            │
                            └──────────────────────▶ ⊘ native-speaking person ◀─────────────┘
                                                     (hand-off note: language, category, reason, sources)
⏻ switch: the Head of Support edits prototype/switch.json — one language at a time, to L3, L2 or off; no deployment.
```

## 3. Component table
| # | Component | Rung (1 rules · 2 classical ML · 3 pretrained model · 4 custom) | Pattern (chaining · routing · parallelization · orchestrator-workers · evaluator-optimizer · agent) | Trust level (L1–L4) | Checkpoint ⊘ (approval · abstention · sampling · none) | Metric observed |
|---|---|---|---|---|---|---|
| 1 | Router — `router.py` (language + category, TF-IDF characters + logistic regression) | 2 | routing | L4 above 0.50 confidence | abstention (below threshold → person) | language accuracy **94 %**; 8 of 27 automatable tickets below the category threshold |
| 2 | Routing rule — `route_rule.py` (language, switch, security, sensitive, confidence) | 1 | routing | L4 in one direction only (it can only send to a person) | abstention (person only for sensitive) | hand-over recall **100 %** (24 / 24); drafts on hand-over tickets **0** |
| 3 | Retrieve + draft — `retrieve.py`, `draft.py`, `kb/` (TF-IDF top-3 over the English KB; template drafter, LLM if a key is set) | 1 for the template drafter in v0 · 3 with an LLM key | chaining | L3 for en / fr / es · L2 for pt / pl / ar (`switch.json`) | approval (L2) · sampling (L3) | retrieval hit@3 **75 %** (8 cases with sources); 0 / 27 automatable tickets drafted |
| 4 | Policy check — `policy.py` (citation, promises, secrets, language match) | 1 | chaining (gate) | L4 (block → person) | abstention (block → person with the reason) | policy blocks on automatable tickets: **8**, all "language mismatch" |

## 4. Workflow or agent?
*One paragraph.* Can you draw the path in advance (workflow), or does the model decide its own steps and tools (agent)? Why is that the right choice for your risk level? What would have to be true to move one step up?

A **workflow**: the path is drawn in advance (router → rule → retrieve + draft → check), with a gate between each step, no loop and no tool the model can choose. Our risk sits in the routing, not in the writing: a grade, an accommodation or a personal-data request answered by a model is a GDPR and EU AI Act Annex III problem, so the decision to answer must stay in rules a DPO can read, and the only model output is a draft that a rule checks. To move one step up (an evaluator-optimizer that rewrites a blocked draft, or an agent that can open the user's course settings), we would need: the success criterion met per language on 200 cases, 100 % hand-over recall held on adversarial cases in all six languages, and the switch tested in production for that language.

## 5. Fallbacks
What happens when… (one line each)
- retrieval finds nothing: no passage above 0.10 → no draft → escalate to a native-speaking person, reason "no source found" (`pipeline.py`).
- the model's confidence is below the threshold: language confidence or category confidence below 0.50 → escalate, reason "language not covered or unsure" / "low confidence" (`route_rule.py`).
- the policy checker blocks the draft: the draft is never sent; escalate with the block reason in the hand-off note (`pipeline.py`).
- the API is down: `draft.py` catches the error and falls back to the template drafter; the policy check still runs (a non-English template draft is blocked → person).

## 6. The override switch ⏻
- Who can switch it off: the Head of Support, by editing `prototype/switch.json` (no deployment); if the file cannot be read, every language is treated as **off** (fail safe).
- Scope (one ticket · one user · everyone): **one language, for everyone** — L3 (the agent sends), L2 (a native speaker approves) or off (person only).
- Tested on (date, by whom): [date], by [name] — French set to `off`, `python prototype/app.py "Comment changer ma photo de profil ?"` returned "escalate · language switched off"; set back to `L3`.

## 7. Data
- Training / demo data (`data/`): `prototype/data/tickets_synthetic.csv` — 156 synthetic tickets (144 in the 6 languages — 24 per language — and 12 in Italian, German, Dutch, Korean for "other") written by the team for the router; `prototype/data/demo_tickets.csv` — 12 demo tickets; `prototype/kb/` — 35 fictional English help articles. All invented, no real data.
- Evaluation data (`evals/eval_set_v0.csv`): 51 cases (7 languages · 24 hand-over · 27 automatable, 12 of them in the core languages), labelled by the team before the run, origin in every row; **never used for tuning**.
- Personal data present? None: all tickets are invented. In production, ticket text is personal data (we are processor); logs and storage rules are in `governance.md` (Sessions 3 and 4).

## 8. Eval result v0
Copy the headline from `evals/report_v0.md`: *"<N> % of 'how do I' tickets got a draft two graders would send without editing — criterion was <X> %."*

"**0 %** (0 / 12) of automatable core-language tickets got a draft two graders would send without editing — criterion was **57 %**. Hand-over recall 100 %, 0 drafts on hand-over tickets."

## 9. What you would build next (3 lines max)
1. A drafter that writes in the ticket's language (LLM from the passages only), so non-English drafts stop failing the language check.
2. A router trained on more synthetic tickets, with the threshold calibrated on held-out synthetic data, not on the eval-set.
3. Sensitive rules that fire on decisions ("change my grade"), not on topics ("export the grades"), and refusals with a cited article for isolation traps.
