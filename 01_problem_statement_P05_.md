# 01 — Problem statement

**Team:** P5 project team (members to be added) · **Agent:** P5 — Multilingual support agent for an ed-tech LMS · **Last updated:** 2026-11-08

> The course brief establishes an ed-tech learning management system (LMS) operating in **14 countries**, with an **English-language knowledge base**, an agent answering in customers' languages, escalation of sensitive requests to a native-speaking support representative, and **L3 per language**. It does **not** provide company ticket logs, language distribution, staffing costs, current accuracy, or customer satisfaction. All additional company-specific quantitative values below are **provisional assumptions for planning**, not observations. Gartner (2024) provides **external industry cost benchmarks**, not measurements of this hypothetical LMS company. Replace them with real or instructor-provided figures before using them as an investment case.

## 1. The problem in one sentence

Learners and LMS administrators in a B2B ed-tech company operating in **14 countries** experience delayed or inconsistent support when they ask questions in their own language but the official knowledge base is written in English; in an **illustrative scenario** of 10,000 tickets per month, with 40% in non-English languages and six extra minutes of handling per such ticket, this creates **400 additional support hours per month** (approximately **€10,000/month** at an assumed fully loaded €25/hour). Separately, applying Gartner’s 2024 industry median of **$13.50 per assisted contact** to the assumed 10,000 contacts implies **$135,000/month in total assisted-contact costs** as an external-benchmark scenario, not a verified company cost or multilingual surcharge; today customers rely on English documentation, translations, or multilingual human agents. **Proposed success** is to resolve at least **50% of eligible, routine tickets** in the customer's language using cited documentation, while routing every identified sensitive ticket to an appropriate native speaker and avoiding a material quality decline in any pilot language.

| Number in the sentence | Value | Measured / analogy / guess | Source or test |
|---|---|---|---|
| Countries served | 14 | **Given in project brief** | Session 2, P5 project proposal; confirm actual supported languages separately |
| Monthly ticket volume | 10,000 | **Guess (scenario only)** | Replace with 6–12 months of helpdesk ticket logs |
| Non-English ticket share | 40% (4,000/month) | **Guess (scenario only)** | Helpdesk language tags or language detection validated on a random sample |
| Incremental handling time | 6 minutes per non-English ticket | **Guess (scenario only)** | Time-and-motion sample and ticket handling timestamps, stratified by language |
| Extra monthly workload | 400 hours = 4,000 × 6 / 60 | **Derived from guesses** | Recompute using measured ticket volume, language mix and handling times |
| Fully loaded support cost | €25/hour | **Guess (scenario only)** | Finance/HR: salaries, benefits, overhead and paid hours |
| Median cost per assisted contact | **$13.50/contact** | **Analogy — published industry benchmark** | Gartner (2024), *Benchmarks to Assess Your Customer Service Costs* [1]; benchmark is not specific to LMS or multilingual tickets |
| Median cost per self-service contact | **$1.84/contact** | **Analogy — published industry benchmark** | Gartner (2024) [1]; traditional self-service is not equivalent to an AI-resolved contact |
| Total assisted support cost under Gartner benchmark | **$135,000/month = 10,000 × $13.50** | **Derived: guess × analogy** | Assumes *all* 10,000 tickets are assisted contacts; verify channel mix and actual costs before reuse |
| Difference between Gartner assisted/self-service medians | **$11.66/contact = $13.50 − $1.84** | **Derived from analogy** | A cross-channel benchmark gap, **not** guaranteed AI savings, AI marginal cost, or a multilingual surcharge |
| Illustrative monthly cost of extra workload | €10,000 = 400 × €25 | **Derived from guesses** | Not an estimate of realizable savings; validate avoidable time and agent supervision in S2 |
| Eligible-ticket resolution target | ≥50% | **Proposed target / guess** | S4 evaluation, then S5 per-language metrics and S6 controlled pilot; may be revised after baseline collection |
| Sensitive-ticket routing target | 100% of identified sensitive cases | **Proposed safety requirement** | Labelled test set with sensitive examples in every pilot language; inspect false negatives |
| Per-language quality guardrail | No pilot language falls >5 percentage points below its measured pre-launch quality baseline | **Proposed threshold / guess** | Compare like-for-like ticket types and confidence intervals by language; investigate small samples |

**Interpretation:** The €10,000/month figure describes a *hypothetical incremental multilingual workload burden*, not the agent's net benefit. The Gartner-derived **$135,000/month** instead refers to a hypothetical **total** assisted-support cost and **must not be added** to the €10,000 estimate: they describe different cost views and use different currencies. The **$11.66/contact** benchmark gap is not an AI savings forecast. S2 must subtract AI operating costs, evaluation, translation/QA, escalation, and expected error costs. The 14-country footprint should not be confused with 14 distinct languages.

## 2. Problem tree — from symptom to cause

- **Symptom** (what people complain about): Customers using non-English languages may wait longer, receive uneven answers, or need repeated follow-ups; multilingual agents spend time translating English documentation. These are **hypotheses to validate**, not reported customer complaints.
- **Problem** (what is actually going wrong): Customers cannot consistently access accurate, understandable, timely support in their preferred language, even when an answer exists in the company's English knowledge base. Service quality could vary by language and remain hidden in an aggregate KPI.
- **Root cause** (5 Whys — a provisional causal chain to test):
  1. **Why might response times and answer quality vary by language?** Because requests in some languages require extra manual translation or scarce specialist support.
  2. **Why is extra translation or specialist support necessary?** Because the authoritative support documentation exists mainly in English.
  3. **Why can't customers reliably use that documentation themselves?** Because discoverability, localisation, and language-specific guidance may be insufficient.
  4. **Why hasn't localisation fully solved this?** Because translating and maintaining every article in every supported language can be costly, slow, and prone to outdated versions.
  5. **Why does the problem persist?** Because the support workflow may lack a governed way to retrieve authoritative English content, provide verified multilingual answers, and escalate requests that need human judgement.
- **What would fix the cause:** First assess **non-AI fixes**: improve the English knowledge base, translate the most-used articles, clarify navigation, create standard bilingual macros, and allocate native speakers more effectively. If those measures do not meet the response-time and quality goals, test a **multilingual retrieval-grounded AI assistant** for routine questions, with language-specific quality gates and mandatory native-speaker escalation for sensitive cases. The solution must address the documented cause, not merely translate every ticket.

## 3. Is AI the right tool?

| Question | Our answer |
|---|---|
| Is there a rule that solves 80% of it? | **Not established.** Fixed FAQs, routing rules and translated templates may solve many frequent questions. Measure their coverage first. AI is justified only for the remaining varied, context-dependent questions where static rules or documentation fall short. |
| Is it a prediction / generation problem, or an organisational decision? | **Both generation and organisational decisions are involved, but they must be separated.** Retrieving relevant English material and explaining it in the user's language are language-generation tasks. Deciding which topics are sensitive, who may answer them, and when to escalate is a product/policy decision encoded as deterministic guardrails—not delegated entirely to a model. |
| Do we have the data — which, how much, who owns it? | The **English knowledge base is specified** in the project brief. Availability of historical multilingual tickets, labels, resolutions, permissions and representative samples is **unknown**. The LMS/support organisation would own or control these records, subject to customer contracts and GDPR. Confirm provenance, language coverage, freshness, retention rights and cross-customer isolation before use. |
| What does one error cost — and who pays it? | Costs range from re-contact and wasted agent time to incorrect LMS guidance, lost trust or mishandling of personal/account information. Learners and administrators bear disruption; the SaaS provider bears operational, contractual and reputational consequences. **Probability and severity are not measured**; classify high-impact ticket types and estimate expected error cost in S2. |

**Level chosen:** **GenAI + retrieval (RAG) within a bounded support workflow**, with routing rules and human escalation; **L3 only for languages and routine topics that pass their own evaluation thresholds**. *Why not the level below:* simple rules, translation templates, and search may not handle the diversity and phrasing of real user questions adequately. This must be demonstrated against a rule-based or translated-FAQ baseline; an unrestricted autonomous agent is **not** justified. The safe workflow is: **identify language → classify topic/sensitivity → retrieve approved English sources → generate an answer in that language with citations → validate confidence/policy → answer or escalate to a native-speaking human**. No unsupported answer when retrieval fails.

## 4. Why this agent — the four selection questions

| Criterion | Our answer, one line |
|---|---|
| High frequency — is the work done every day or every hour? | LMS support is assumed to be recurring across the 14-country footprint, but frequency **must be confirmed** in ticket logs by language and issue category. |
| Bounded decision space — can we list its tools and outcomes on one slide? | Yes, for an MVP limited to approved FAQ/how-to topics: detect language, identify sensitivity, search approved KB, draft cited answer, apply quality gate; outcomes are **answer** or **escalate**. |
| Measurable success — can we say in one sentence whether it succeeded on one ticket? | A routine ticket succeeds when the customer receives a **correct, source-grounded answer in the requested language** without unnecessary escalation; a sensitive ticket succeeds when it is **correctly routed to a native-speaking human**. |
| Recoverable failure — if it is wrong, is the damage limited and reversible? | For low-risk informational questions, usually yes via correction and handoff; for account access, privacy, payments, educational consequences or other sensitive requests, **not necessarily**—these must be excluded from automated responses. |

## 5. Press release (Working Backwards)

*Illustrative future launch announcement — drafted as a goal, not a claim of achieved results.*

**6 November 2027 — Multilingual LMS support, grounded in one trusted knowledge base.** Today, our ed-tech LMS announced a multilingual AI support assistant designed to help learners and administrators in our 14-country footprint get clear answers in their own language, even when the original support article is in English. The assistant retrieves approved knowledge-base content, answers routine questions with source references and transfers sensitive requests to a native-speaking support specialist. Our **launch goal** is to resolve **at least 50% of eligible routine requests** without a human reply, **without reducing quality in any pilot language**. “I want to understand the answer immediately, without having to translate it myself or wonder whether it is correct,” says an **illustrative learner persona** (not a real customer testimonial). The assistant will first be piloted in a small set of languages, with performance reported separately for each language and expanded only when quality and escalation safeguards pass.

## 6. What would have to be true?

| # | Hypothesis | Measured / analogy / guess | How we will test it | Session |
|---|---|---|---|---|
| 1 | A meaningful share of multilingual tickets are routine questions whose correct answers already exist in the **approved English knowledge base**. | **Guess** | Sample and label tickets by language, topic, sensitivity and KB answerability; audit article freshness and coverage; compare to a simple FAQ/search baseline. | S3 data audit / S4 prototype |
| 2 | Retrieval-grounded generation can provide **accurate, helpful answers in each pilot language** and achieve the proposed **≥50% eligible-ticket resolution** threshold **without masking poorer results in low-volume languages**. | **Guess** | Evaluate a representative frozen set with per-language answer correctness, citation validity, language fluency and resolution; report both aggregate and per-language outcomes, volumes and uncertainty; expand only on passing languages. | S4 prototype / S5 metrics / S6 A/B |
| 3 | The workflow reliably recognises sensitive requests and low-confidence/no-source cases, and hands them to a **native-speaking human** with enough context to prevent unsafe or frustrating handoffs. | **Guess** | Run adversarial and realistic multilingual escalation tests; inspect false negatives, availability of native speakers, transfer latency, CSAT and any cross-tenant leakage. | S4 tests / S5 metrics / S6 A/B |

**Simpson's paradox guardrail:** A strong overall resolution or satisfaction rate is **not sufficient**. Weighted averages may improve while individual low-volume languages get worse, or language mix may distort comparisons. Report results **within each language**, with counts and comparable ticket categories, before claiming success or increasing autonomy.

## 7. Do-nothing baseline

If the company does not develop this agent over the next **12 months**, customers may continue to use English-language articles, browser translation, standard multilingual macros and human support. The support team may still become more efficient through documentation improvements, language-specific staffing, better routing or existing translation tools; therefore **do-nothing is not “no improvement.”** Conversely, new markets, new course features and changing ticket volumes could increase the workload. The actual direction is **unknown** without a historical trend.

For a **transparent numerical illustration only**, assume the same 10,000 monthly tickets, 40% non-English share and six extra minutes per non-English ticket: the baseline is **400 additional human hours/month** or **€120,000/year** at €25/hour, *before any organic improvement*. **External cost cross-check (Gartner, 2024 [1]):** If all 10,000 monthly tickets are assisted contacts, the **$13.50 median cost per assisted contact** implies **$135,000/month ($1,620,000/year)** for the *total* assisted workload. Gartner also reports a **$1.84 median per self-service contact**, a **$11.66 difference**. These benchmarks describe different support channels, not P5-specific multilingual costs or AI resolution costs. Do **not** sum them with the €120,000 incremental workload figure or claim $11.66 as net savings per AI ticket. Actual cost and potential savings depend on eligible volume, channel mix, effective resolution, human review, AI inference, errors and recontacts. If documentation and process changes independently reduce that extra time by **20%** (another **guess**), the year-12 run-rate becomes **320 hours/month / €8,000 per month**. This is the **next-best, non-AI improvement scenario**, not money the AI can automatically claim as savings.

In S2, replace these assumptions with observed language-by-language volumes, average handling time, first-contact resolution, CSAT, error rates, human cost and expected 12-month growth. Compare three options: **(a)** improve documentation and human workflows only, **(b)** buy an existing multilingual support product, and **(c)** build/orchestrate the P5 assistant. Evaluate *net* value, including human oversight, monitoring, maintenance and expected error costs.

## 8. Personas and current journey (Session 1 milestone)

**Customer persona — illustrative:** A learner (or school administrator) in a non-English-speaking market needs an answer about a routine LMS feature. **Job-to-be-Done:** “When I get stuck using my LMS, I want a correct explanation in my own language so that I can continue learning or working without waiting for translation or a support reply.”

**Current customer journey (hypothesis):** encounters issue → searches help centre → finds English documentation → translates/tries to interpret it → submits a ticket if unresolved → waits for multilingual support → follows answer or reopens ticket. **Likely friction to validate:** comprehension, article discoverability, waiting time, repeated contacts.

**Support-agent persona — illustrative:** A multilingual support specialist responsible for reliable responses, often needing to locate the authoritative English policy/article. **Job-to-be-Done:** “When I receive a customer question in another language, I want the relevant current guidance and case context so I can resolve it correctly without repeatedly translating or escalating.”

**Current agent journey (hypothesis):** read ticket → identify language and issue → search English KB → translate/adapt explanation → check policy/sensitivity → reply → log resolution or escalate. **Likely friction to validate:** search, translation, verification and access to native-speaking specialists.

## 9. Stakeholders and decision ownership (Session 1 milestone)

| Stakeholder | Interest / responsibility | Engagement |
|---|---|---|
| Head of Support / Customer Success | Owns response quality, staffing, escalation and support KPIs | **Manage closely** — proposed operational owner |
| Product Manager / LMS product team | Owns scope, customer value, feature priorities and launch decision | **Manage closely** |
| Engineering / AI team | Builds retrieval, multilingual generation, routing, evaluations and controls | **Manage closely** |
| Native-speaking support agents | Validate language quality; receive sensitive or failed cases; provide feedback | **Keep informed and involve in design/testing** |
| Legal / DPO / Security | Assess lawful data use, retention, access rights and cross-tenant exposure | **Consult early; approval before using customer data** |
| Finance / CFO | Validates baseline costs, investment hurdle and economic case | **Manage closely for S2 go/no-go** |
| Learners, educators and LMS administrators | Experience service quality and trust; provide user feedback | **Research and test across languages, including low-volume cohorts** |

**Open decisions to confirm with the team/company:** actual languages supported and pilot subset; current ticket counts and answerability; which issue types are sensitive; authoritative KB owner; native-speaker coverage; baseline performance by language; accountable go/no-go decision-maker. These are not specified in the P5 course prompt and should not be presented as established facts.


## Sources

[1] Gartner (1 February 2024). **Benchmarks to Assess Your Customer Service Costs.** Gartner Research, public *Key Findings*: median customer-service contact cost **$13.50 for assisted channels** and **$1.84 for self-service**. https://www.gartner.com/en/documents/5164231 (accessed 8 November 2026). *Scope note:* cross-industry medians; neither measures P5’s actual support costs nor represents a quoted price for AI support.
