# 03 — Product brief · P5 Multilingual LMS support agent · v1

> Session 3. One page. Start from `01_problem_statement.md` and `02_investment_memo.md` — do not start from a blank page.
> v1 in class (16 October). v2 before Session 4 (30 October), after your users: fill the last two sections.

**Team:** P5 project team (members to be added) · **Starting point:** P5 · **Version:** v1 — [23 November 2026]

## 1. Problem, user, do-nothing  *(from 01)*
- **Problem in one sentence (with a number):** Learners and LMS administrators in our 14 countries ask questions in their own language while the knowledge base is in English; tickets in Portuguese, Polish and Arabic wait 2–3× longer (P5 proposal, measured), and in our scenario 4,000 non-English tickets a month × 6 extra minutes = 400 support hours a month, ≈ €10k a month (guesses, `01_problem_statement_P05_.md`).
- **User (persona):** a multilingual tier-1 support agent (1 of 20) answering learners, instructors and admins — goal: resolve a routine "how do I…" ticket correctly in the customer's language — pain: finding the right English article, then translating and adapting it (≈ 9 of 14 minutes). Second user: the learner or admin who asks — goal: a correct answer in their language without waiting.
- **Do-nothing baseline:** better documentation and agent experience improve today's €1.2M ticket-handling cost by ≈ 5 % a year = **€60k a year** (`02_sizing_P05.xlsx`, Decision tab). Next-best project (the hurdle): localised help centre + language routing, no GenAI = **€50k a year**.

## 2. The process — as-is and to-be
*As-is: one routine non-English ticket (e.g. Portuguese), handled by one agent. Minutes and error rates are guesses (scenario from 01; total checked against 23.8 tickets per agent per day in `02_sizing_P05.xlsx`), to be measured by watching two agents (time-and-motion) and on a sample of helpdesk logs.*

| # | Step | Who today | Minutes | Error rate | Cost of an error | Automate / augment / keep human (test it fails) | Trust level (L1–L4 or person) | Minutes after | Metric for this step |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Read the ticket, identify language and category (machine-translate it if needed) | agent | 2 (guess) | 5 % misrouted (guess) | ticket in the wrong language queue: +1 day wait, re-contact (≈ €10) | **Automate** — passes the 8 tests (clear input/output, many examples, cheap error: a wrong queue is caught by the next person) | **L4** above a confidence threshold; below → human queue | 0 | language-ID accuracy and routing accuracy, **per language** |
| 2 | Check whether the request is sensitive (grade, assessment, certificate, accessibility, personal-data request) | agent | 1 (guess) | 3 % missed (guess) | GDPR Art. 9 / Art. 15 breach, contract breach with the institution, EU AI Act Annex III drift — legal and reputational, not just € | **Automate the routing only, never the answer** — fails test 6 (errors are not cheap); the system can only send a ticket *to* a person, never decide alone to answer a sensitive one | **L4 in one direction (escalate only)**; the answer to a sensitive ticket = **person only** | 0 for routing; sensitive tickets stay human (≈ 9, with the hand-off note) | **recall of sensitive tickets = 100 %**, per language, on the adversarial cases |
| 3 | Search the English knowledge base for the right article | agent | 4 (guess) | 10 % wrong or outdated article (guess) | wrong answer, reopened ticket (€10–25, `02_sizing_P05.xlsx` error-cost rows) | **Automate** — passes the tests (clear input, KB is stable for months, citations are enough to explain) | **L3** — retrieval runs alone; a native speaker samples | 0 | retrieval hit rate @3 (right article in the top 3), per language |
| 4 | Translate / adapt the answer into the customer's language | agent | 5 (guess) | 8 % mistranslation or wrong step (guess) | wrong guidance, re-contact, loss of trust in that country (€10–40 per error, higher for PL/AR) | **Augment** — fails test 6 in small languages (errors cost more, PL/AR 10 % error rate in the sizing) and test 3 (no feedback signal yet per language) | **L3 per language** for the core languages that pass their eval (a native speaker samples weekly) · **L2** for Portuguese, Polish, Arabic until they pass (draft, a native speaker approves) | core L3: ≈ 0.2 (weekly sample) · PT/PL/AR L2: ≈ 1.5 (read and approve) | **sendable-without-edit rate**, judged by two native-speaker graders, per language |
| 5 | Check policy and reply to the customer | agent | 1 (guess) | 1 % (guess) | a promise the company cannot keep (a grade, a deadline, a deletion) | **Automate the checks (rules), keep the send human where the level is L2** — the gate blocks: no citation, language mismatch, low confidence, sensitive words | **L4 for the gate** (block → human) · send: L3 languages = agent sends with an "AI answer" label and a "talk to a person" button · L2 languages = the native speaker sends | L3: 0 · L2: ≈ 0.3 | policy catches on adversarial cases (target 100 %); share of conversations where the user clicks "talk to a person" |
| 6 | Log the ticket: language, category, resolution | agent | 1 (guess) | 15 % mis-tagged (guess) | per-language metrics are blind — the Simpson's-paradox risk of 02 goes unseen | **Automate** — passes all tests | **L4** | 0 | share of tickets with complete log fields (language, category, sources, model version, answer/escalate) |

**Before:** 14 min of human time per routine non-English ticket. **After:** ≈ 0.2 min in an L3 core language, ≈ 1.8 min in an L2 language (PT/PL/AR), sensitive tickets unchanged in who answers (≈ 9 min, the hand-off note saves the reading and part of the search).

**Where the pain sits (the two steps):** step 3 (search the English KB, 4 min, 10 % errors) and step 4 (translate/adapt, 5 min, 8 % errors) — 9 of the 14 minutes, and the reason small-language tickets wait 2–3× longer: they queue for the few native speakers who can do step 4.

**The way back to a person (designed first):** (1) a "talk to a person" button on every AI answer, in every language; (2) every sensitive, low-confidence, no-source or unsupported-language ticket goes to the **native-speaking human queue** with a hand-off note (language, category, reason, sources retrieved, confidence) and a priority no lower than today; (3) the **per-language switch** L3 → L2 → off, held by the Head of Support, flipped without a deployment.

**Where the governance line sits:** between step 2 and step 4 — grades, assessments, certificates, accessibility accommodations and personal-data requests are never answered by the agent (EU AI Act Annex III point 3; GDPR Art. 9 and 15–17). Below the line, only routine "how do I…" questions answerable from a cited KB article.

*Trust levels — same scale as Session 1: L1 suggests · L2 drafts, a person approves · L3 acts on a scope, a person samples · L4 acts alone under a threshold.*

## 3. Features — RICE and MoSCoW
*Reach from `02_sizing_P05.xlsx` (base): 10,000 tickets/month; automatable = 3,850 core + 1,375 Portuguese + 800 Polish/Arabic = 6,025/month; automatable outside the core languages = 2,175/month. Shares of grade, account and unsupported-language tickets are guesses. Sorted by RICE.*

| Feature | Reach / month (from 02_sizing.xlsx) | Impact (0.25–3) | Confidence (50/80/100 %) | Effort (person-weeks) | RICE | MoSCoW |
|---|---|---|---|---|---|---|
| Language detection + sensitive-request router + hand-off note to a native speaker ("talk to a person" button) | 10,000 | 3 | 80 % | 1.5 | 16,000 | MUST |
| Per-language switch (L3 / L2 / off) + eval report per language | 6,025 | 2 | 80 % | 1 | 9,640 | MUST |
| Cited answer in the customer's language from the English KB | 6,025 | 3 | 50 % | 4 | 2,259 | MUST |
| Chat widget on every LMS page (proactive, in-app) | 10,000 | 1 | 50 % | 4 | 1,250 | WON'T |
| Fine-tuning a model on historical tickets | 6,025 | 0.5 | 50 % | 6 | 251 | WON'T |
| Account actions (reset password, enrol, delete data) done by the agent | 1,000 (guess: 10 %) | 2 | 50 % | 5 | 200 | WON'T |
| Grade and assessment explanations ("why did I get this grade?") | 500 (guess: 5 %) | 2 | 50 % | 3 | 167 | WON'T |
| Languages beyond the 6 supported (answer in any language) | 200 (guess: 2 %) | 1 | 50 % | 2 | 50 | WON'T |

- **MUST (≤ 4):** language detection + sensitive router + hand-off note · per-language switch + per-language eval report · cited answer in the customer's language.
- **SHOULD:** none this time — with eight candidates, ≤ 4 MUST and ≥ 5 WON'T leave no room; native-speaker feedback on drafts (approve / edit / reject + reason) is the first candidate for v2.
- **COULD:** none this time — pre-translated top articles in PT/PL/AR is the hurdle project, kept as the baseline we compare against, not a feature.
- **WON'T this time (≥ 5) — this is the out-of-scope list:** proactive chat widget on every page · fine-tuning on historical tickets · account actions by the agent · grade and assessment explanations · languages beyond the 6. *(Dated [23 november 2026]; revisited after the Session 5 eval.)*
- **The feature that tests our flip assumption, and why it is a MUST:** the **cited answer in the customer's language** — it is only third by RICE because its confidence is 50 %: it *is* the guess that flips the decision (≈ 57 % resolution of automatable core-language tickets to beat do-nothing, `02_investment_memo.md`). We build it first to learn whether that number is reachable.
- **The cut that hurt the most:** the chat widget on every LMS page — highest reach, but it talks to every learner at a higher trust level than this MVP can justify, and it would hide per-language failures behind volume.

## 4. Data  *(from the six-question audit — details in governance.md)*
Sources · volume and labels · coverage by segment · legal basis · leakage · freshness: **sources** — the English KB (ours, no personal data) and a 20-case eval-set, invented and labelled by the team (no ticket logs exist for P5; never real customer data) · **volume and labels** — KB size unknown (to count); 20 cases now → 50 (Assignment 4) → 200 (Session 5), labelled by hand before any run, two graders · **coverage** — 6 languages: 3 core (assumed EN, FR, ES — to confirm), Portuguese, Polish, Arabic; Polish and Arabic need native-speaker graders we do not have yet · **legal basis** — we are processor (GDPR Art. 28) for ticket content under the LMS contract's DPA; accessibility requests can be health data (Art. 9) · **leakage** — eval cases never used as prompt examples; retrieval filtered by institution · **freshness** — KB changes with each LMS release; index rebuilt on article change, every answer cites the article version.

## 5. Model — one rung per part
| Part | Rung (1 rules · 2 classical ML · 3 pretrained model · 4 hybrid) | Why the rung below fails |
|---|---|---|
| Language detection | 2 — off-the-shelf language-ID model (e.g. fastText lid) | rules (script, keywords) cannot separate Portuguese from Spanish or tag a two-line Polish ticket reliably |
| Sensitive-request router | 4 — hybrid: per-language keyword rules reviewed by native speakers **OR** a pretrained multilingual classifier; either flag → person | rules alone miss paraphrases, typos and Polish/Arabic morphology; a classifier alone gives no auditable floor for a 100 % recall target |
| Retrieval over the English KB | 3 — pretrained multilingual embeddings + keyword search (hybrid ranking) | English keyword search cannot match a Polish or Arabic question to an English article; translate-then-search is our hurdle baseline, kept for comparison |
| Answer in the customer's language | 3 — pretrained LLM via API, no fine-tuning, answers only from the retrieved passages, with citations | macros and translated FAQs cannot cover the phrasing variety of 6 languages; machine translation of a whole article is not an answer to the question |
| Policy / quality gate | 1 — rules: citation present and valid, answer language = ticket language, confidence ≥ threshold, blocklist (grades, accommodations, deletion promises), no other institution's data | — lowest rung; it must stay deterministic and auditable, so we do not climb |
| Per-language switch and logging | 1 — rules / configuration | — lowest rung |

## 6. Where it lives (integration surface)
Surface · speed needed · format · fallback · who sees the log: **surface** — the help-centre chat of the LMS for learners and admins (L3 languages) and the helpdesk console of the native-speaking agents (L2 drafts and hand-offs) · **speed** — answer in < 10 s in the chat; drafts ready before the agent opens the ticket · **format** — answer in the customer's language, "AI answer" label, link to the English source article, "talk to a person" button; for the agent, a hand-off note (language, category, reason, sources, confidence) · **fallback** — any failure, timeout or low confidence → the native-speaking human queue, never a guess · **who sees the log** — Head of Support and per-language leads (per-language dashboard), DPO on request (conversation log: language, category, sources, model version, answer/escalate).

## 7. Success criterion — one sentence
> By [23 novembre 2026], on our 200-case eval-set (stratified by language, labelled before the first run), at least **57 %** of automatable core-language tickets get a cited answer in the customer's language that two independent native-speaker graders would send without editing — and 100 % of sensitive tickets (grades, assessments, certificates, accessibility, personal-data requests) are handed over to a person, with no answer sent without a valid KB citation; Portuguese, Polish and Arabic reported separately.

*Threshold = our flip point: ≈ 57 % to beat do-nothing (≈ 52 % to beat the hurdle), `02_sizing_P05.xlsx`, Decision tab.*

## 8. Risks and rollback trigger
- Top risks (from your Working Backwards FAQ): (1) a sensitive request (grade, accessibility, data access) is answered instead of routed — GDPR and EU AI Act exposure; (2) a good average hides a failing small language (Simpson's paradox: Polish/Arabic 10 % errors vs 4 % core); (3) the answer invents a feature or a step not in the KB; (4) one institution's content appears in another's answer; (5) the escalation queue of a small language becomes slower than today; (6) supervision grows beyond 0.5 FTE and the case falls below do-nothing.
- **Rollback trigger (one line):** one sensitive ticket answered by the agent, or a language's sendable rate below its threshold on the weekly sample → that language switches to L2 the same day (Head of Support), and to off if it happens again.

---
*v2 only — after the users (before 30 October)*

## 9. What the users changed
| Change | Evidence (who said / did what — e.g. “3 of 3 never opened the tab”) |
|---|---|
| | |

## 10. What they could not decide
(The threshold, the model, the legal basis… — and who or what decides instead.)
