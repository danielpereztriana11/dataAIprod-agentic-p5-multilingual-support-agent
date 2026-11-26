# Launch memo — P5 multilingual LMS support — 26 November 2026

## 1 · Decision
**No-go for a real-user launch; proceed with a local presentation using fictional questions.** The current prototype has not met its quality gate and does not connect to a real support queue. A future pilot requires a fresh release evaluation, human handoff capability, operational owners and approval. Next decision date and signatories: **to be agreed**; no launch has been signed.

**Budget:** the sizing model estimates €95,333/year in fixed and semi-fixed costs (integration €18,333, evaluation €20,000, supervision €30,000, monitoring €15,000 and re-evaluation €12,000). This is a business-case estimate, not approved funding or the cost of the local demo (`02_sizing_P05.xlsx`, Decision tab).

## 2 · Evidence
- **Quality:** the original prototype scored 0/12 sendable core-language cases. The simplified Ollama version produced 5/12 drafts; the preliminary review rated 1/12 (8.3%) sendable without editing, below the 57% criterion. The 51 fictional cases were reused during development, and both grading workbooks were prefilled from the same assistant review: this is not independent held-out evidence (`evals/report_v0.md`, `evals/local_model_v3/README.md`).
- **Guardrails:** all 24 cases labelled for handoff were escalated in the local run; this includes more than sensitive cases. The handoff is simulated and does not reach a person. Wrong-source drafts occurred; citations alone do not prove correctness. The Arabic draft remains pending qualified language review.
- **Experiment:** compare first-contact resolution and handling cost for eligible routine issues with and without AI support, while tracking errors and handoff times. The live baseline, minimum useful effect, sample size and start date remain unmeasured or unapproved (`06_07_experiments_operations.md` §§1–2).
- **Sizing:** modelled base annual net value €66,474; expected value €72,030; do-nothing €60,000; next-best alternative €50,000. These are assumptions, not realised savings (`02_sizing_P05.xlsx`, Decision tab).

## 3 · Rollout steps
| Step | Scope and status | Gate before next step | Decision owner |
|---|---|---|---|
| 0 | Local presentation with fictional questions; available | Demonstrate and describe limitations; no real users | Project team |
| 1 | Improve quality and evaluate on separately held-out cases; pending | Meet the 57% core-language criterion and sensitive handoff requirement, with qualified independent grading and language-level results | Proposed Product Manager and AI Lead |
| 2 | Internal/shadow testing; pending | Human queue, monitoring, named operators, full rollback test and DPO review in place | Proposed Product Manager and Head of Support |
| 3 | Controlled real-user pilot; not approved | Pre-register baseline, effect, sample, timing and guardrails; obtain Product Manager approval and DPO review | Proposed Product Manager; DPO reviews |

No traffic percentages or rollout dates have been approved.

## 4 · Rollback and switch
For a proposed pilot, one sensitive AI answer or a language exceeding its wrong-answer ceiling for two consecutive weekly samples triggers the Head of Support to move that language to L2 the same day, or off when review cannot contain the harm (`05_metrics.md` §3). A night operator and execution-time target remain unassigned. In the local prototype, `prototype/switch.json` changes each language's setting; the switch was tested on 26 November 2026 by the Codex assistant and Daniel with a fictional English question. A timed full rollback and real human handoff remain untested.

## 5 · Owners and signatures
| Decision | Proposed owner |
|---|---|
| Approve real-user experiment | Product Manager signs; DPO reviews |
| Read results and act | Head of Support, Product Manager and Finance |
| Operate switch | Head of Support by day; support on-call at night, person pending |
| Approve release | Product Manager with AI Lead's evaluation evidence |
| Retain traces and respond to users/regulators | DPO and Engineering; storage and retention approval pending |

People have not been assigned to these roles and no real-user launch has been signed (`governance.md`, Sessions 6–8).

## 6 · What we do not know yet
- **Quality and coverage:** improve retrieval and generation, then independently grade held-out cases per language; obtain qualified Arabic and Polish reviewers.
- **Live impact and cost:** measure support baselines, calculate sample size and validate the financial assumptions before any pilot.
- **Operational readiness:** implement a real human queue, monitoring and trace storage, assign operators, and time a complete rollback rehearsal.
