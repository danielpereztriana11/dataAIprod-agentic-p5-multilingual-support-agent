# Local model v1 — preliminary development comparison

**Run date:** 26 November 2026. **Input:** frozen copy of `evals/eval_set_v0.csv`, 51 fictional cases. **System:** local Ollama `qwen2.5:1.5b`, `paraphrase-multilingual` semantic search, switch configuration and source snapshots in this folder; SHA-256 hashes of the code, knowledge base, training data, switch and dataset are in `manifest.json`. The reference is a frozen local snapshot, not a Git commit. Model versions are recorded by tag; the Ollama model digests are not captured and outputs can vary. Re-running may append only unfinished cases, not repeat completed ones.

**Scope:** the original 51 cases are reused and some were previously inspected, so this is a development comparison, not an independent held-out evaluation. The team had already reviewed the labels before the run. The model did not receive expected labels during inference. `results.jsonl` preserves each outcome; `grader_1_blank.csv` and `grader_2_blank.csv` are separate, unfilled sheets for independent human review of the two drafts.

## Automatic counts

| Measure | Original v0 (`evals/report_v0.md`) | Local model v1 |
|---|---:|---:|
| All cases | 51 | 51 |
| Draft decisions | 0 | 2 |
| Core-language cases labelled no handoff | 12 | 12 |
| Core-language drafts | 0/12 | 1/12 (8.3%) |
| Cases labelled handoff returned escalation | 24/24 | 24/24 |

The 1/12 is **draft production, not the sendable rate**. The two independent graders have not assessed it. At most 1/12 could count as sendable in this run, below the 57% criterion even if both reviewers approve it. The second draft is Arabic, returned at L2, not part of the core-language denominator. All 24 labelled-handoff cases escalated, but the category includes more than sensitive cases; this is not a measured sensitive-only recall, and the prototype has no real queue. Polish was switched off for this run, so routine Polish handoffs do not measure its drafting quality.

The two drafts are `EV-FR-03` (French, L3) and `EV-AR-03` (Arabic, L2). Their factual correctness, requested language, citation and sendability remain to be independently graded by suitable language reviewers. A local model's source check and the fact a citation is present do not establish correctness. No claim is made that the Arabic draft is suitable for a customer.

The 49 escalation reasons include 18 sensitive flags, 8 low-category-confidence decisions, 8 switched-off language cases, 7 security flags, 4 uncertain/unsupported-language decisions, 2 no-source results, 1 missing or rejected draft and 1 language-policy block. These are system reasons, not validated root causes or error counts; review each case against its label. Automated counts and the prior model evaluation cannot substitute for native-speaker human grading.

## Next action

Each reviewer separately fills their blank sheet. Review the question, expected action, article and generated draft for relevance, factual support, language and forbidden claims. Resolve disagreements after independent grading and record who graded and when. Before a production-like or independent performance claim, freeze a new held-out set and evaluate the current version without tuning on it. Never send real customer data through this demo.
