# 06_07 — Experiments & operations · COD · P5 multilingual LMS support

**Status: proposed plan, not an approved experiment or a description of deployed monitoring.** No live pilot, production dashboard or incident response has been performed. A local switch-off check was run on 26 November 2026; it is not a production rollback exercise. Owners are proposed roles; the team must name the people and obtain approvals before real-user testing. Baselines and targets below are referenced or explicitly marked pending.

## §1 Prove the effect — hypothesis, unit and design

The original prototype produced no sendable drafts on 12 automatable core-language evaluation cases (`evals/report_v0.md`). The simplified Ollama version produced five drafts for these 12 cases; the preliminary review judged one sendable (1/12, approximately 8.3%), below the 57% criterion (`evals/local_model_v3/README.md`). Both grading worksheets were prefilled from the same assistant review, and the cases were reused during development, so this is not an independent held-out result. It is not ready for a real-user experiment. First improve the router, cross-language retrieval and drafter using separate development data; complete the release checks in §3. The offline 57% sendable-draft criterion is a prerequisite, not an estimate of live first-contact resolution.

**Hypotheses — measured against normal human support:**

1. **Handling cost:** for eligible routine tickets, AI-assisted support reduces human ticket-handling cost relative to the control by the end of pilot month 2, without exceeding the per-language wrong-answer thresholds or increasing handoff response time beyond its pre-launch baseline. The €1.2m/year overall baseline and projected €174k gross annual savings at 60% core resolution are business-case assumptions, not pilot results (`05_metrics.md` §4). Minimum detectable cost reduction: pending Finance's pre-registration.
2. **Portuguese / Polish / Arabic first contact:** AI assistance increases the number of eligible tickets answered at first contact versus control, read by language at week 4, without worsening the handoff first-response-time baseline. The business case assumes 4,500 tickets/month across these languages and up to 750/month at steady state, not a measured pilot baseline or a four-week target (`05_metrics.md` §4). Baseline and minimum effect per language: pending. Polish remains human-only until Polish review and a capable handoff recipient are available; include it in baseline reporting, not treatment, until that is resolved.
3. **Supervision cost:** AI-assisted operation remains at or below 0.5 FTE of review time during each pilot month (`05_metrics.md` §4), without relaxing the sensitive-ticket handoff requirement. This is a cost ceiling, not a claim that measured baseline supervision equals 0.5 FTE.

**Unit:** initially randomise eligible routine issues, stratified by language and institution, to current human workflow (control) or AI-assisted workflow (treatment). Count the first eligible ticket for each issue as the analysis unit; repeated tickets about the same issue stay in the same arm and count as follow-up. All sensitive requests go to humans in both arms. Because agents may learn from drafts and change their behaviour on control tickets, check for contamination. If material, randomise teams or shifts instead, account for clustering and reassess sample size. Prevent cross-institution access and maintain human escalation in both arms.

**How to measure the comparison:** Before allocation, define how the helpdesk identifies repeat tickets about the same issue. In each arm, first-contact resolution is the number of first eligible tickets resolved at first contact without reopening within seven days, divided by all first eligible tickets in that arm. Count resolution by either a person or AI in both arms; report AI-resolved cases separately. Compare the rates overall and by language where samples permit. Record handling time and relevant support and AI costs for both arms, using the same accounting method, then compare cost per eligible issue. Track handoff response time, wrong answers and supervision separately. The team still needs to agree on outcome definitions, live baselines and minimum improvements before enrolment.

**Plan B:** if randomisation is impractical, run shadow mode with invented or approved data, then a controlled before/after comparison with a comparable untreated team or institution. This cannot eliminate differences between groups or time trends; it does not establish causality as strongly as an A/B test. No intervention on real users until Product Manager approval and DPO review.

## §2 Decide before — duration and decision rule

**Smallest improvement:** 57% is the offline core-language sendable-draft threshold in `05_metrics.md` / `02_sizing_P05.xlsx`, not an A/B treatment effect. Minimum live improvement and control baselines for first-contact resolution, handling cost and handoff wait: **pending measurement and approval by Product Manager and Finance**. Do not substitute the README's P5 illustrative 55% → 65% example as a measured baseline.

**Business-case reference:** `02_sizing_P05.xlsx` projects approximately €66,474 annual net value in its base case versus €60,000 for do-nothing, a difference of approximately €6,474. These are modelled assumptions, not experimental results. Finance should apply a consistent, pre-agreed annualisation and cost method to pilot observations before comparing an updated business case with do-nothing; this comparison does not establish a minimum live treatment effect by itself.

**Slowest guardrail:** seven-day reopening needs seven days after the final ticket; supervision is read monthly (`05_metrics.md` §3–4). Proposed minimum read: after one complete pilot month plus the seven-day follow-up for the final enrolled ticket; extend if the sample-size calculation or segment volumes require it. This is a proposed schedule, not a powered duration.

| Input | Value | Source / status |
|---|---|---|
| Live control baseline p0 | Pending, measured before allocation | Helpdesk baseline; Product Manager |
| Minimum live improvement | Pending Finance and Product Manager decision | Business case and control baseline |
| False-positive risk / missed-win risk | 5% / 20% | Optional template calculator defaults |
| Units per group | Pending calculation after baseline and effect are agreed | `sample_size.xlsx` template (not yet populated) |
| Eligible volume per week | Pending actual helpdesk data, per language and arm | 10,000 tickets/month overall is a business-case input, not eligible pilot volume (`05_metrics.md` §4) |
| Proposed earliest decision read | One complete pilot month plus 7-day outcome follow-up; extend if required | `05_metrics.md` §3–4; proposed |

**Segments proposed for pre-registration:** en, fr, es, pt, pl, ar and unsupported; dialect/mixed language including Darija; learner/instructor/admin; university/corporate academy (`05_metrics.md` §3). Report languages first; do not make per-language efficacy claims without adequate sample and reviewers.

**Decision rule: draft for approval, not yet registered.** Before enrolling anyone, record the actual approval date, baselines, minimum effects, sample size, eligible languages and read date.
- **Ship / expand:** at the planned read, meet the pre-registered cost and first-contact effects with sufficient evidence, maintain ≤0.5 FTE supervision for the completed month, and satisfy the per-language guardrails. The Product Manager approves each language on the evidence.
- **Iterate:** evidence or sample is insufficient, effect is below the agreed minimum, or the offline 57% gate is unmet; stay in shadow mode or L2 as appropriate and re-evaluate before release.
- **Kill:** Finance and Product Manager stop the pilot if the pre-registered effect is not achieved at the planned final read or the revised business case no longer beats do-nothing; retain human support.
- **Stop early for harm, never for a favourable result:** one sensitive ticket receives an AI answer, or a language exceeds its wrong-answer rate ceiling for two consecutive weekly samples (core 4%, pt 6%, pl/ar 10%; `05_metrics.md` §3). Head of Support drops the affected language to L2 the same day; use `off` if L2 cannot contain the harm or human review is unavailable. DPO reviews sensitive incidents. No inference that a small sample proves safety.

## §3 Watch the four layers — monitoring and drift

All alert routes, tools and clocks below are proposed; no instrumentation or on-call service is in place yet. A threshold not in the existing business case is marked pending rather than invented.

| Layer | Metric | Alert threshold | Clock | Owner | Startup / larger organisation |
|---|---|---|---|---|---|
| Infrastructure | Workflow/API failures and latency | Any outage → humans-only; latency alert threshold pending baseline | Real time; on-call Engineering | Engineering on-call | Platform logs / Cloud Monitoring or Datadog |
| Model quality | Sendable-without-edit rate and retrieval hit@3 by language | Core offline sendable rate below 57% blocks release; language-specific targets pending | Each release; weekly sample | AI Lead | Local eval report / Langfuse or equivalent |
| Product & guardrails | Sensitive handoff; wrong-answer rate and handoff response time by language | One sensitive AI answer → same-day L2; wrong-answer thresholds per §2; wait-time alert threshold pending baseline | Sensitive: immediately; error: weekly; wait: weekly | Head of Support; DPO for sensitive incidents | SQL + Metabase / warehouse + BI |
| Business | Handling cost, first contact and supervision | Supervision >0.5 FTE for one month → no new language to L3 and rerun business case | Weekly first contact; monthly cost | Finance and Product Manager | Spreadsheet / BI dashboard |
| Paging | Route incident to accountable role | Any confirmed sensitive answer or outage | Immediately | Engineering on-call and Head of Support | Manual phone / incident paging tool, pending setup |

**Current demo checks:** Before presenting, start Ollama and the local demo, try the prepared fictional English and Spanish questions, check each answer against its cited article, and try a sensitive question to confirm a simulated handoff. The switch check is documented in §4. The demo has no real human queue, production dashboard or automated alerting; the monitoring table describes a proposed pilot setup. Keep the previous evaluation results intact and label any new results with the version, dataset and grading method.

**Hosting:** current implementation includes a local browser demo and command-line prototype, not an integrated support service. The browser demo is for fictional questions; hosting, security and capacity for a pilot are pending Engineering review. Secrets belong in environment variables, not Git. Do not claim a tunnel, cloud service or tracing exists until configured.

**Release gates:** development: run code checks and isolated demo tests. Staging, before each prompt/model/KB/rule change: run golden 30 and judge, then full 100 before release (`evals/README.md`); review by two human graders and inspect safety failures per language. Shadow mode, human queue, rollback path and a documented switch test must exist before pilot. Production progression internal → limited pilot → broader rollout is proposed; traffic percentages, approval date and thresholds require pre-registration. Do not progress to a real-user pilot until the current version has been independently evaluated and meets the applicable offline gates; the historical 0/12 result does not measure the current version.

**First expected drift:** knowledge drift when LMS articles or steps change. Signal: rising no-source, stale-citation or wrong-answer rates, reviewed weekly by the KB owner and Head of Support. Re-run the frozen evaluation on every model, rule, prompt or source release, recording dataset and version; do not tune on the held-out cases. Current frozen set has 100 cases; a separate 200-case set is a future target (`05_metrics.md` §5).

## §4 Contain the incident — trace, classes and rollback

**Proposed trace:** one request ID with timestamp, language/segment, model and prompt versions, source IDs/versions, outcome, latency and cost → classify (category and confidence) → retrieve (permitted source IDs and scores) → generate (model and latency) → policy decision → human decision when applicable. Proposed storage: access-controlled observability service, location and vendor pending DPO/Engineering approval. Avoid raw ticket text, health information and credentials in traces. Proposed retention: 90 days for pseudonymised logs, then deletion (`governance.md` Session 3); this is not implemented or approved.

**Proposed dashboard:** (1) alert status and thresholds; (2) trend of handoff and wrong-answer rates; (3) latency distribution this week vs last; (4) resolution and errors per language; (5) reviewed failures with redacted examples. Tool and data pipeline pending Engineering selection; no dashboard exists yet.

| Class | P5 example | Response |
|---|---|---|
| Caught | Policy blocks an uncited draft | Handoff, count and review weekly; add a spec requirement when a pattern is confirmed |
| Sent wrong | Routine learner receives incorrect LMS steps | Stop affected language if harm threshold is met; correct through human support, investigate and record incident |
| Harmful | AI answers a sensitive grade or data-access request | Same-day L2 or off if L2 cannot contain risk; Head of Support leads incident and contacts DPO for data issues |
| Outage | Model, retrieval or routing service unavailable | For a pilot, route to human-only support and alert Engineering immediately. The demo can show a simulated handoff for some failures or an unavailable message if its server fails; it cannot deliver a ticket to a person |

| Rollback field | Proposed plan |
|---|---|
| Trigger | Harm threshold in §2 or outage; also off if approved human review is unavailable |
| Who decides | Head of Support by day; designated support on-call by night, person not yet assigned; DPO advises on data incidents |
| Action | Change affected language to L2 in `prototype/switch.json`, or `off` if necessary; revert release if the issue is version-specific. Production switch and human queue do not yet exist |
| Time to execute | Same day for harm threshold (`05_metrics.md`); operational target and on-call availability pending rehearsal |
| What people see | Proposed: acknowledgement and handoff to human support, with no unapproved AI draft shown; UI not implemented |
| Last tested | 26 November 2026, local prototype, by the Codex assistant: English changed from L3 to off; a fictional English question returned `escalate · language switched off`; the original file was restored. Daniel also rehearsed the switch on the local demo on 26 November 2026 and confirmed that the fictional English profile-photo question showed HUMAN HANDOFF when English was off. English is now back to L3. A timed full rollback rehearsal remains pending |

**Local demo procedure:** If an answer is unsafe or a language should stop answering, edit that language in `prototype/switch.json` to `off`, save the file, then send an invented question in that language and confirm the browser displays HUMAN HANDOFF. The demo reads the switch during routing; this is a simulated handoff, not a notification to support. Restore the agreed demo setting after the check and verify it. For a suspected outage, stop the live demonstration and explain the failure; never enter real user data. Changing a switch does not recall an answer already displayed.

**Before a real pilot:** Assign the day and night operators, create a real human queue and incident contact path, test the end-to-end fallback and the complete rollback with a timer, and agree the execution-time target. If a real answer causes harm, the proposed incident owner records the event, arranges human follow-up and involves the DPO for data issues. None of these steps is recorded as completed.

## §5 Own the system — five owners

| Decision | Proposed owner | Written where |
|---|---|---|
| Approve an experiment on real users | Product Manager signs; DPO reviews before launch | §1–2; `governance.md` Session 6 |
| Read weekly numbers and act | Head of Support; Product Manager for product results; Finance for monthly cost | §3 |
| Operate the switch | Head of Support by day; designated support on-call at night (assignment pending) | §4; `governance.md` Session 7 |
| Approve a model, prompt or source release | Product Manager, with AI Lead's eval evidence and DPO review where applicable | §3; `evals/README.md` |
| Retain traces and answer customer/regulator | DPO with Engineering for storage and access | §4; `governance.md` Session 7 |

**People and handover:** Daniel completed the local switch rehearsal described in §4; this does not assign him the Head of Support or on-call role. The people responsible for the Product Manager, Head of Support, support on-call, AI Lead, Engineering, Finance and DPO roles are still to be agreed. Before a pilot, record a primary and backup for switch operation and the contact path for each incident role. For the presentation, the team should agree who demonstrates the switch and who explains the experiment and limitations.

**Outstanding before an actual pilot:** real baselines and sample calculation; per-language grader and human-queue coverage (especially Polish); named owners and approval; working instrumentation, integration, monitoring, and a timed end-to-end rollback rehearsal; quality improvement and release evaluation. All remain pending.
