# 02 — Investment memo (one page)

**Recommendation:** CONDITIONAL GO on **≥ 57 % resolution of automatable core-language tickets**, measured on an independent eval-set with the Session 4 prototype — with Portuguese, Polish and Arabic reported separately, and human supervision confirmed at ≤ 0.5 FTE.

> Line one is the decision. Everything below is evidence for that line. Same base case as `02_sizing_P05.xlsx` — every € figure comes from that sheet.

| €/year, year 1 | Pessimistic | Base | Optimistic | Expected value |
|---|---|---|---|---|
| Net annual value | −119,084 | 66,474 | 274,256 | **72,030** |
| Probability | 0.25 | 0.50 | 0.25 | — |
| Do-nothing (value of the current process improving on its own) | 36,000 | 60,000 | 84,000 | 60,000 (base) |
| Next-best project: localised help centre + language routing, no GenAI (the hurdle) | 50,000 | 50,000 | 50,000 | 50,000 |

## 1. How much?
Our LMS handles an assumed **10,000 tickets a month** with **20 agents** at €60k all-in each, i.e. **€10 per human ticket** (20 × €60k ÷ 120,000 tickets) — below Gartner's 2024 median of $13.50 per assisted contact, so our value per ticket is conservative. Base case, bottom-up by language: 55 % of tickets come from three core languages, 25 % Portuguese, 20 % Polish and Arabic. At steady state the agent resolves **3,060 tickets a month** (2,310 core · 550 Portuguese · 200 Polish/Arabic), 31 % of volume. With a staged rollout (20 % → 70 % adoption over the year), year 1 deflects **17,442 tickets**: **€174k** of human work avoided, minus €10.9k of wrong answers and €1.7k of AI cost, minus **€95k of fixed costs** = **€66k net**.
**Measured** (from the course case): 14 countries, 6 languages, 20 agents. **Analogy**: Gartner's cost per contact. **Everything else is a guess** — ticket volume, language mix, agent cost, resolution rates. **The one guess that matters: 60 % resolution of automatable core-language tickets.**

## 2. How sure?
Not very, yet. Scenario probabilities (25 / 50 / 25) are a team judgement; they give an expected value of **€72k**. **The flip point:** keeping every other base input fixed, the agent needs **≈ 57 % core-language resolution to beat do-nothing** (≈ 52 % to beat the hurdle). The base case assumes 60 % — a margin of only three points. **How S4 tests it:** run the prototype on an independent eval-set of real core-language tickets (≈ 200, graded by two reviewers), with the same protocol per language, and log reviewer time. Second check: supervision. Each extra 0.5 FTE costs €30k a year, which would take the base case (€66k) below do-nothing (€60k).

## 3. What if we're wrong?
**It is not the model:** AI tokens are €1.7k a year, under 2 % of costs. The bill is fixed — supervision €30k, evaluation €20k, integration €18k a year (€55k amortised over 3 years), monitoring €15k, re-evaluation €12k. The pessimistic case (−€119k) is low resolution (35 %), slow adoption and a full supervision FTE together. The rollout is staged, so if the Q1 eval fails we stop and lose roughly the integration plus one quarter of running costs. **The tail by language — Simpson's paradox:** the blended error rate is ≈ 4.8 %, but Polish/Arabic run at 10 % against 4 % for core languages, and their error cost eats 25 % of their gross value (4 % for core). An aggregate score would hide that. We report every metric per language, and each language has its own switch from L3 down to L2. **Governance line:** a wrong answer on grades, accessibility or data access is a GDPR and reputational risk, not just a cost. These requests are never automated; they are routed to a native-speaking agent (owners: DPO and Head of Support — see `governance.md`).

## 4. Compared to what?
**Do-nothing is not zero:** better documentation and agent experience improve today's €1.2M ticket-handling cost by ≈ 5 % a year, i.e. **€60k**. Our expected value beats it by only **€12k**. **The hurdle:** the same team could instead build a **localised help centre** (translate the most-viewed English articles into Portuguese, Polish and Arabic) with language-based routing to native speakers, no GenAI. It is valued at **€50k** as a placeholder; we still have to size it bottom-up. The expected value clears it by €22k, but **the pessimistic case does not clear the hurdle** — hence a conditional, staged GO, not a full launch.

## 5. Build, buy or orchestrate?
**We orchestrate because** the workflow, not the model, is our edge: existing LLM APIs + our English knowledge base + our own language detection, sensitive-request routing, per-language switch and per-language evals. Training our own model (build) is out of reach for a 20-agent support team. A vendor (buy) is faster, but gives us less control over per-language thresholds, logs and EU data residency. Weighted scores from the `Build or buy` tab: Build **[x.x]** · Buy **[x.x]** · Orchestrate **[x.x]** *(to fill once the tab is scored)*. **What would change our mind:** a vendor that offers per-language autonomy controls, EU residency and exportable logs and eval-sets, at a per-resolution price below our build-specific costs (€52k a year at year-1 volume).

*Sources: [1] Gartner (2024), *Benchmarks to Assess Your Customer Service Costs* — median $13.50 per assisted contact, $1.84 self-service, https://www.gartner.com/en/documents/5164231 · [2] Albert School (2026), Data & AI Product, P5 project proposal (14 countries, 6 languages, 20 agents) · [3] Albert School (2026), Session 2, Opportunity Sizing & Investment Decision (method, seven cost lines, Octopus Energy adoption ramp) · [4] `02_sizing_P05.xlsx` — all other figures are team assumptions to validate with support logs, payroll, vendor quotes and the S4 eval.*
