# Simplified demo v3 — development comparison

**Run:** 26 November 2026 on the 51 fictional cases in `eval_set_v0.csv`. Frozen inputs and code and their SHA-256 hashes are in `manifest.json` and `prototype/` here. The run uses `simple_pipeline.py`, Ollama `qwen2.5:1.5b`, multilingual semantic retrieval and the switch snapshot. Model tags rather than digests were captured; outputs can vary. This is a repeated development comparison, **not an independent held-out evaluation**: the cases and their previous results have been inspected.

| Measure | Original v0 | Local v1 | Local v2 | Simplified v3 |
|---|---:|---:|---:|---:|
| Cases | 51 | 51 | 51 | 51 |
| Drafts | 0 | 2 | 7 | 6 |
| Drafts for 12 core-language cases labelled no handoff | 0/12 | 1/12 | 4/12 | 5/12 |
| Labelled-handoff cases escalated | 24/24 | 24/24 | 24/24 | 24/24 |
| Core-language drafts preliminarily judged sendable | 0/12 | Not graded | Not graded | 1/12 (8.3%) |

Drafts produced are **not the sendable rate**. The two workbooks record 25 pass, 25 fail and one pending; both started from the same assistant-generated suggestions, so agreement is not independent evidence. Even if both approved all five core-language drafts, the result would be 5/12 (41.7%), below the 57% criterion. The 24 labelled-handoff cases cover more than sensitive requests, and returning an escalation decision is not the same as delivering a ticket to a real queue. Polish was off during the run.

## Preliminary assistant review — not independent human grades

- `EV-EN-02`: graded pass in the preliminary review: answers the bulk-enrolment question using the correct article.
- `EV-EN-04`: **wrong source** (`KB-CATALOG-03` rather than the audio-troubleshooting article) and no requested troubleshooting; not sendable.
- `EV-EN-05`: the correct article is cited but the response omits the requested steps and institution time zone; not sendable.
- `EV-ES-03`: **wrong source** (`KB-CATALOG-03` rather than the notifications article), with unsupported instructions; not sendable.
- `EV-FR-03`: the draft cites the expected article and covers the main steps but was graded fail because its French needs editing.
- `EV-AR-03`: the draft cites the expected article; Arabic quality, mixed interface labels and sendability need a qualified human review. This was L2.

The two wrong-source drafts were marked L3 by the demo even though the generated answers were incorrect. The existing source check did not prevent these errors. **Do not use this prototype to answer real customers automatically** on the basis of this run. The code does not send real messages or operate a human queue.

All other 45 cases were escalated. Their logged reasons: sensitive 21 (15 pre-check + 6 routing), security 7, switched-off language 6, uncertain/unsupported language 4, no clear source 3, no reliable draft 3, low confidence 1. Reasons are system outputs, not validated diagnoses. These counts are not directly comparable to earlier reason categories because the workflow order and rules changed.

`results.jsonl` contains all outputs. `grader_1_all_51.xlsx` and `grader_2_all_51.xlsx` record the team worksheets, which were prefilled from the same assistant review; their identical verdicts do not establish independent agreement. The Arabic case remains pending qualified language review. Reviewers should compare each draft with the question, expected action and source before reporting sendability. The older `evals/report_v0.md`, `evals/run_v0.csv`, `evals/local_model_v1/` and `evals/local_model_v2/` were preserved.
