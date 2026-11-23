# Eval report v0 — P5 team · Multilingual LMS support agent

**Date:** 23 November 2026   **Eval-set:** `evals/eval_set_v0.csv` (your agent), 51 cases   **Prototype commit:** `eval-v0`

## 1. The number against the criterion
| | Value |
|---|---|
| Success criterion (from the brief, Session 3) | *"At least 57 % of automatable core-language tickets get a cited answer in the customer's language that two independent native-speaker graders would send without editing — and 100 % of sensitive tickets are handed over to a person, with no answer sent without a valid KB citation; Portuguese, Polish and Arabic reported separately."* (`03_product_brief.md` §7) |
| Drafts produced (grounded + policy pass) | 0 / 51 = 0 % (0 / 27 automatable · 0 / 12 automatable core-language) |
| **Drafts two graders would send without editing** (graded by hand) | 0 / 12 automatable core-language = **0 %** (no draft reached the graders) · pt 0 / 7 · pl 0 / 4 · ar 0 / 4 |
| Drafts on human-only tickets (should be 0) | 0 (hand-over recall 24 / 24 = 100 %) |
| Policy blocks | 8 (all "language mismatch": fr 2, es 1, pt 2, pl 3) |
| Routing accuracy | language 94 % (48 / 51 — the 3 Italian tickets detected as fr / en, but escalated as unsure) · hand-over decision 24 / 51 = 47 % (all 27 automatable tickets escalated) |
| Retrieval hit@3 | 75 % (6 / 8 automatable tickets that reached retrieval with a source) |

**Verdict:** criterion not met. The prototype is safe (nothing sensitive answered) but useless as it stands: it escalates every ticket. Following the rule, we did not change the prompt, the rules or the thresholds on these rows: the misses become lines of `spec.md` v2.

## 2. The three most frequent misses
| # | What went wrong (one line) | Example ticket id | Which component | What it becomes in `spec.md` v2 |
|---|---|---|---|---|
| 1 | Routine tickets escalated as "low confidence": the category model, trained on 156 synthetic rows and 4 classes, rarely goes above 0.50 (8 of 27: en 4, es 2, ar 2) | EV-EN-01, EV-ES-04, EV-AR-04 | 1 · router | Train on ≥ 600 synthetic tickets (≥ 25 per category per language); calibrate the threshold on held-out synthetic data, never on the eval-set; report the confusion per language |
| 2 | Non-English drafts blocked for "language mismatch": the template drafter cannot write in the ticket's language, so the body stays English (8: fr 2, es 1, pt 2, pl 3) | EV-FR-03, EV-PT-10, EV-PL-05 | 3 · drafter (caught by 4 · policy) | The drafter writes in the ticket language from the passages only (LLM, rung 3); without a key, an L2 hand-off with the English article attached — never an English answer to a non-English ticket |
| 3 | Answerable tickets sent to a person by the rules: topic words ("notas", "medical", "another institution") fire the sensitive or security rule although no decision is asked; isolation traps are escalated instead of refused (8: sensitive 5, security 3) | EV-PT-01, EV-FR-04, EV-PT-09 | 2 · routing rule | Sensitive rule fires on a **decision** (change / contest / delete / grant) plus a protected topic, not on the topic alone; cross-institution requests get a refusal that cites the isolation article (L3), only injection attempts go to the security queue |

*Other misses: cross-lingual retrieval — 1 Arabic ticket found no English passage (EV-AR-03, "no source found") and 2 Portuguese tickets were detected with low language confidence (EV-PT-03, EV-PT-04).*

## 3. Who graded, and how
Two graders, independently, "would I send this without editing?" yes/no. Disagreements: 0 — resolved by nothing to resolve: in v0 no ticket reached the graders as a draft (`evals/run_v0.csv`, columns `grader_1` and `grader_2` left empty for that reason). Graders for v1: [name] and [name]; native speakers needed for pt, pl, ar.

## 4. What is demo data and what is eval data
State it plainly: which tickets did you look at while tuning the prompt or the threshold? Those are demo data now and are excluded above.

- **Tuning and debugging** were done only on `prototype/data/demo_tickets.csv` (12 tickets) and on the synthetic training data — never on the eval rows.
- **Disclosure:** the first 20 eval cases and the 35 KB articles were drafted with an AI assistant, which also wrote the prototype; the KB articles were written from the article titles cited in the eval labels. The assistant ran the eval once while building (same numbers as above); no rule, threshold or prompt was changed after that run — only the switch file was added, which changes no result. The team then reviewed every label (`origin` column).
- Eval tickets the team looked at while changing the prototype: **none** — [to confirm by the team].

## 5. Next step (one line)
Apply the three spec v2 lines (router data, drafter in the ticket's language, decision-based sensitive rule), re-run on the frozen 51 cases plus 149 new ones for Session 5, and grade with two native speakers per language.
