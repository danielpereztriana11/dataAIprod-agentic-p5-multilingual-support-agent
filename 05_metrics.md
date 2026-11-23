# 05 · Metrics — Côme-Oussama-Daniel (COD) · P5 Multilingual LMS support agent

> Session 5 deliverable. Five sections = the five moves of the session. Every number traces to a file already in the repo: `02_sizing_P05.xlsx` (cell named) or `evals/report_v0.md` — no new numbers appear here. "Not yet" means it is measured from the pilot on.

## 1 · Place the number — the stack for your agent
| Level | Question | Our metric | Value today (or "not yet") | Produced by | Owner | Clock |
|---|---|---|---|---|---|---|
| 5 Business | does it move the P&L? | human ticket-handling cost avoided, net of AI, error and fixed costs | not yet — base case +€66k a year at 60 % core resolution (Decision D17) | finance data + helpdesk volumes | CFO / Finance with the Head of Support | months |
| 4 Product | does the user adopt it and get the job done? | routine tickets resolved without reopening within 7 days, **per language** | not yet | A/B, then production logs | Product Manager | weeks |
| 3 Guardrails & responsible AI | does it stay inside the lines — for everyone? | hand-over recall on sensitive tickets (grades, accessibility, personal data), **per language** | **100 %** (24 / 24), 0 AI answers on hand-over tickets (`report_v0`) | eval-set + adversarial rows, then weekly native-speaker sample | DPO + Head of Support | days |
| 2 AI system | does the workflow complete the task? | automatable core-language tickets with a cited answer two graders would send as is | **0 %** (0 / 12) — criterion **57 %**; pt 0 / 7 · pl 0 / 4 · ar 0 / 4 (`report_v0`) | eval-set + two graders | Engineering / AI team | hours |
| 1 Model | is the component right? | language-ID accuracy · router confidence · retrieval hit@3 | **94 %** (48 / 51) · 8 of 27 routine tickets below 0.50 · **75 %** (6 / 8) (`report_v0`) | offline eval-set | Engineering / AI team | seconds |

*Read bottom-up: each arrow is a hypothesis that Sessions 6 + 7 test. Read top-down: the business number is the last to move and the only one that counts.*

## 2 · Decide when to stop — the stop criterion
*"We stop improving **language-ID accuracy** at **94 %** because **the level-2 sendable rate** does not respond to it — and the next point would cost **new synthetic training data for languages we do not serve, for zero additional sendable answers**."*

- **Component metric and value:** language-ID accuracy, 94 % (48 / 51, `report_v0`).
- **The level-above metric that stops responding:** sendable as is, 0 % (0 / 12). The 3 language-ID errors are the 3 Italian tickets, detected as fr / en but escalated anyway as "unsure" — fixing them changes no outcome. The 27 routine tickets were lost elsewhere: 8 "low confidence" in the category router and 8 drafts blocked for "language mismatch" (`report_v0`, misses 1 and 2).
- **Cost of the next point:** labelling and training data for non-supported languages, retraining, re-running the eval — weeks spent on a metric the business case does not see.
- **Where the next sprint goes instead:** the drafter writing in the ticket's language (miss 2) and the category router (miss 1) — the components the level above still responds to.
- **A floor, not a stop (any miss blocks the release):** **hand-over recall on sensitive tickets = 100 % and 0 AI answers on them, in every language** (today 24 / 24). One miss in a language → that language does not go to L3.

## 3 · Choose what to protect — the hierarchy, by segment
| Kind | Metric | Numerator / denominator | Level | Lag | Source & owner |
|---|---|---|---|---|---|
| Primary (1) | Routine tickets **resolved without reopening within 7 days**, per language | routine tickets answered by the agent and not reopened (no new ticket from the same user on the same topic) within 7 days / **all** routine tickets of that language — escalated ones count as not resolved | 4 Product | 7 days | helpdesk logs · Product Manager |
| Guardrail (3) | **Hand-over recall on sensitive tickets** (grades, assessments, certificates, accessibility, personal data) | sensitive tickets sent to a person with no AI answer / sensitive tickets — eval-set + weekly sample | 3 Guardrails | days | eval-set + native-speaker sample · DPO + Head of Support — floor: 100 % |
| Guardrail | **Wrong-answer rate per language** ≤ its value in the business case: core 4 %, Portuguese 6 %, Polish / Arabic 10 % (Inputs D26–D28) | wrong answers / AI answers sampled in the weekly native-speaker review, per language | 2–3 | 1 week | weekly sample · Head of Support (per-language leads) |
| Guardrail | **"Talk to a person" reaches a native speaker** | requests answered by a native speaker within that language's pre-launch first-response time / "talk to a person" requests | 4 Product | days | helpdesk timestamps · Head of Support |
| Counter-metric (2) | **First-response time of the tickets the agent hands over**, per language — the people it does not serve (Klarna's missing line) | median first-response time of handed-over tickets / pre-launch median, same language | 4–5 | weeks | helpdesk timestamps · Head of Support |
| Counter-metric | **Native-speaker review time** spent approving L2 drafts and sampling L3 answers | review hours a month / hours of 1 FTE — against 0.5 FTE in the business case (Inputs D52) | 5 Business | 1 month | time tracking · Head of Support + Finance |

- **Segments reported:** language (en, fr, es, pt, pl, ar, and "unsupported") · dialect or mixed language (Moroccan Darija — S3 interview 1) · user role (learner, instructor, admin) · customer type (university, corporate academy). Every metric above is read **per language first**, the average last.
- **Fairness metric, named:** **equal error rates across languages** (equalised odds) — the wrong-answer rate and the hand-over recall, compared language by language against the core languages. Secondary: **selection-rate parity** — the share of routine tickets that get an AI answer, per language (today 0 % everywhere, `report_v0`).
- **Harm threshold that stops the rollout, and its owner** *(copied into `governance.md`)*: if, in the weekly native-speaker sample, a language's wrong-answer rate is above its business-case value (core 4 %, Portuguese 6 %, Polish / Arabic 10 %) for two consecutive weeks, or one sensitive ticket receives an AI answer, that language drops to L2 the same day (`switch.json`) until the gap is explained. Owner: Head of Support, reviewed monthly with the DPO.
- **How it could be gamed → the repair:** (1) "not reopened" also counts users who gave up → the counter-metric on handed-over tickets and the "talk to a person" guardrail; (2) a team under pressure could sample only easy answers in the weekly review → the sample is random, drawn by the log, per language; (3) the average could improve while Polish or Arabic degrade → no metric is reported without its per-language line.

## 4 · Derive the business metrics — three, with expected effects (the oral)
| Business metric | Baseline (from `02_sizing_P05.xlsx`) | Expected effect (from `evals/report_v0.md` × the cost line) | Lag | Read date | It is a hypothesis about… |
|---|---|---|---|---|---|
| **Human ticket-handling cost** | €1.2M a year = 10,000 tickets × 12 × €10 (Inputs D6, D9) | **Today €0**: 0 % sendable (`report_v0`) avoids no ticket. At the base 60 % core resolution: **−€174k gross in year 1** (Upside D39), **+€66k net** (Decision D17); break-even with do-nothing at **57 %** — the criterion | 1 month | end of month 2 of the pilot | sendable rate (L2) → resolved without reopen (L4) → human hours avoided (L5) |
| **Portuguese, Polish and Arabic tickets answered at first contact** — the wait gap of the P5 proposal | 4,500 tickets a month (Portuguese 2,500 + Polish / Arabic 2,000, Upside D18 + D28), all waiting for a native speaker today | **Today 0**: 0 of 15 routine pt / pl / ar eval tickets drafted (`report_v0`). At steady state: **up to 750 a month** (550 + 200, Upside D20 + D30), ≈ 17 % of their volume | 1 week | week 4 of the pilot, **per language** | drafter in the ticket's language + cross-lingual retrieval → small languages stop queuing for the few native speakers |
| **Supervision cost — stated as a non-effect** | 0.5 FTE = €30k a year (Inputs D52–D53, Decision D11) | **Unchanged: stays ≤ 0.5 FTE.** Stop band: above 0.5 FTE for a month → no new language goes to L3 and the case is re-run, because +0.5 FTE (+€30k) takes the base case (€66k) below do-nothing (€60k, Decision D22) | 1 month | end of each pilot month | L2 approvals and L3 sampling stay cheap as volume grows |

**The tree (component → product → business), with the claimed effects:**
```
COMPONENT  router category confidence (8 / 27 routine tickets below 0.50) ─┐
COMPONENT  language-ID 94 % — stop here (§2)                                ├─▶ AI SYSTEM  sendable as is, core 0 % → 57 % criterion, per language
COMPONENT  drafter in the ticket's language (8 drafts blocked today) ───────┤        │
COMPONENT  retrieval hit@3 75 % (6 / 8)                                    ─┘        ▼
GUARDRAIL  hand-over recall 100 % (24 / 24) — floor            PRODUCT  routine tickets resolved without reopen in 7 days, per language
                                                               PRODUCT  pt / pl / ar answered at first contact: 0 → up to 750 a month
                                                                         │
                                                                         ▼
BUSINESS   handling cost −€174k gross in year 1 at 60 % (break-even 57 %) · supervision flat at €30k · cost of wrong answers €10.9k a year (Upside D40)
```

## 5 · Make the judge trustworthy — the evaluation plan
- **Eval-set v1:** `evals/eval_set_v1.csv`, **100 cases** (200 in production), stratified by language — 16 per supported language + 4 unsupported; the 49 new inputs are AI-generated and tagged, **labels written by the team**; a **golden set of 30** (`golden_30 = yes`, 5 per language) that never changes.
- **Grading guideline:** `evals/README.md` §2 — five binary criteria (right decision · grounded · answers the question · in the customer's language · nothing forbidden), boundary examples, pass / fail. Two graders on the same 30 rows: agreement = **[__ %]** (`python evals/grading.py agreement`).
- **Judge:** model **[__]**, prompt in `evals/judge_prompt.txt`, pasted case by case from `evals/judge_inputs_30.md`; human–judge agreement on the same 30 = **[__ %]**; known biases: **[__]**; re-aligned on **[date]**. The v0 drafter is a template, so the judge shares no model family with it; if the drafter moves to the same family as the judge, we say so.
- **Limit we state:** the v0 prototype escalates every ticket, so on v0 the agreement mostly measures the decision (C1); the draft criteria (C2–C5) are re-measured on the golden 30 when the drafter writes in the ticket's language.
- **Cadence:** golden 30 + judge on every change (prompt, model, KB, rules) · full 100 before each release · human sample of 5 % of live answers per language every week.
- *Optional, not graded* — red rows and assertions: not done this round.
