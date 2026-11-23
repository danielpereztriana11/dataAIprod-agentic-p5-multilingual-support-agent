# spec.md — executable spec · P5 Multilingual LMS support agent · v2

> Session 3 skeleton, completed in Session 4. This is what Claude Code (or Cursor) reads to build the prototype.
> Same content as 03_product_brief.md, but nothing can stay vague: inputs, outputs, edge cases, fallbacks, done.
>
> **v2 (Session 4, after `evals/report_v0.md`):** lines marked **[v2]** are new or changed since the skeleton; each one comes from an eval miss or from what the prototype actually does.

## problem
Learners, instructors and admins of an ed-tech LMS in 14 countries ask support questions in 6 languages, but the knowledge base exists only in English. Tickets in Portuguese, Polish and Arabic wait 2–3× longer, and agents spend ≈ 9 of 14 minutes per routine non-English ticket searching the English KB and translating. The agent answers routine "how do I…" tickets in the customer's language from cited English KB articles, and routes every sensitive request (grades, assessments, certificates, accessibility, personal-data requests) to a native-speaking person. It must beat do-nothing: ≈ 57 % of automatable core-language tickets resolved (`02_sizing_P05.xlsx`).

## user_workflow
Steps with inputs and outputs, and the trust level of each step.
```
- detect    : ticket text                          -> language, confidence                         (L4 above threshold, else human queue)
                                                                                                    [v2] router.py: TF-IDF characters + logistic regression, threshold 0.50
- route     : ticket text + language               -> sensitive yes|no, category, reason           (L4 escalate-only; sensitive = person only)
- retrieve  : text + language + tenant_id          -> top-3 English KB passages (global + own tenant) (L3)
- draft     : passages + text + language           -> answer in the ticket language, with citations (L3 core languages that passed · L2 PT, PL, AR)
                                                                                                    [v2] never an English answer to a non-English ticket (miss 2)
- check     : answer                               -> policy pass | block + reason                  (L4 — block always goes to a person)
- send      : answer                               -> customer, "AI answer" label + "talk to a person" (L3: agent sends · L2: native speaker sends)
- log       : everything above                     -> log row                                        (L4)
```

## io_contracts
```
ticket    : {id, text, language_pref?, tenant_id, user_role: learner|instructor|admin, channel}
detection : {language: en|fr|es|pt|pl|ar|other, confidence}
routing   : {sensitive: true|false, category, reason?}
draft     : {text, language, citations[{kb_id, version, span}], confidence, policy: pass|block, block_reason?}
handoff   : {ticket_id, language, category, reason, sources[kb_id], confidence, draft?}
switch    : {language -> L3|L2|off}            # held by the Head of Support, changed without a deployment
log       : {ticket_id, language, category, sources, model_version, decision: answer|escalate, latency_ms}
```

## edge_cases
- **[v2] miss 1 — router unsure on routine tickets:** the category model is trained on ≥ 600 synthetic tickets (≥ 25 per category per language, never eval rows); its threshold is calibrated on held-out synthetic data; a ticket below the threshold goes to a person with the two most likely categories in the hand-off note
- **[v2] miss 2 — answer not in the ticket's language:** the drafter writes in the ticket language from the passages only (LLM, rung 3); with no LLM available, the ticket goes to an L2 native speaker with the English article attached; the policy check keeps blocking any language mismatch
- **[v2] miss 3 — rules fire on a topic, not a decision:** the sensitive rule fires only on a decision verb (change, correct, contest, delete, grant, issue) together with a protected topic (grade, certificate, accommodation, personal data, completion record); "how do I export the grades" stays a how-to
- **[v2] miss 3 — isolation traps:** a request for another institution's data gets a refusal that cites the isolation article (KB-CATALOG-01, KB-REPORT-01, KB-ADMIN-LOG-01) — answered, not escalated; only instruction-injection attempts ("ignore your rules…") go to the security queue
- **[v2] cross-lingual retrieval:** a Polish or Arabic ticket must reach the English article (multilingual embeddings, rung 3); until then, "no source found" → person (EV-AR-03)
- no KB passage found → no answer; hand-off to the native-speaking queue with reason "no source" (never invent a feature or a step)
- language not covered → no generated answer; short acknowledgement in English, hand-off to the human queue with an English summary, priority no lower than today
- personal data in the ticket → not copied into logs beyond the routing reason; health data (disability, illness) → sensitive, person only
- out-of-scope category (e.g. payroll, billing) → for P5: grades, assessments, certificates, accessibility accommodations, data access / correction / deletion, account actions → hand-off, no promise
- two questions in one ticket → answer each one with its own citation, or hand off if one of them is sensitive
- mixed languages (e.g. Portuguese + English terms) → answer in the dominant language of the ticket
- question about another institution's content → answer only from the global KB and the user's own tenant; never show another tenant's data
- instructions inside the ticket ("ignore your rules…") → treat as text, refuse, flag to the security queue
- Arabic → right-to-left rendering of the answer and the citations

## fallbacks
- **[v2]** confidence below **0.50** (language or category) → escalate to a person, with the context (was [0.7] in the skeleton: the prototype uses 0.50)
- **[v2]** retrieval score below 0.10 → no draft → escalate, reason "no source found"
- **[v2]** switch file unreadable → every language treated as **off** (fail safe)
- **[v2]** LLM API down or no key → template drafter; a non-English template draft is blocked by the language check → person
- policy block → show the reason to the agent, no draft
- language switched to L2 → the draft goes to the native speaker's console, nothing is sent to the customer automatically
- language switched to off → every ticket of that language goes to the human queue as today
- model or retrieval timeout (> 10 s) → human queue, with whatever was retrieved

## done_criteria
- the success criterion from 03_product_brief.md §7: ≥ 57 % of automatable core-language tickets get a cited answer that two native-speaker graders would send without editing, on the eval-set; Portuguese, Polish and Arabic reported separately
- 100 % of sensitive cases handed over, in every language
- zero answers without a valid KB citation; zero answers citing another tenant
- zero policy breaches on the adversarial tickets
- **[v2]** v0 result (`evals/report_v0.md`): 0 % sendable on core languages, hand-over recall 100 % — not met

## out_of_scope
The WON'T column of the MoSCoW board: proactive chat widget on every LMS page · fine-tuning on historical tickets · account actions by the agent (reset, enrol, delete) · grade and assessment explanations · languages beyond the 6 supported.

## eval_set
`evals/eval_set_v0.csv` — **[v2]** 51 tickets now (was 20), growing to 200 by Session 5; run with `python prototype/evals.py`, graded by two people in `evals/run_v0.csv`.
