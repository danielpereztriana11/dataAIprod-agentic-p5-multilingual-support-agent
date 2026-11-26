# Local model v2 — preliminary development comparison

**Run:** 26 November 2026; 51 fictional cases from `eval_set_v0.csv`. This is a repeated development comparison, not an independent held-out evaluation: the cases and prior results were previously inspected. The team confirmed the expected labels before this run. Frozen input, code, KB and switch copies and their SHA-256 hashes are in this folder (`manifest.json`); Ollama tags are `qwen2.5:1.5b` and `paraphrase-multilingual`. The manifest does not capture model digests, and model outputs can vary.

## Counts

| Result | Original v0 | Local v1 | Local v2 |
|---|---:|---:|---:|
| Cases | 51 | 51 | 51 |
| Drafts produced | 0 | 2 | 7 |
| Drafts for 12 routine core-language cases | 0/12 | 1/12 | 4/12 |
| Labelled-handoff cases escalated | 24/24 | 24/24 | 24/24 |

The 4/12 is the draft-production rate, **not** the sendable rate. Two independent native-speaker graders have not yet graded any of these outputs. At most 4/12 (33.3%) could be sendable in this run, below the 57% criterion even if all four were accepted. The 24 handoff-labelled cases are a broader group than sensitive cases; the number does not establish sensitive-ticket recall, and this prototype has no real queue. Polish was off during this run.

The seven drafts were EN 3, FR 1 and AR 3. Portuguese and Arabic are L2 (human approval required); English and French are L3 in this demo, but the code does not send real messages. The 44 escalations were logged as: sensitive 18; security 8; language switched off 8; no source 3; language uncertain/unsupported 3; no draft 2; category low confidence 1; language policy block 1. These are recorded reasons, not validated causes.

## Preliminary assistant review — not independent human grading

The assistant inspected the outputs and corresponding fictional source passages after the run:

- **EV-EN-02:** appears to cover the requested CSV procedure and source; two human graders still need to decide whether it is sendable.
- **EV-EN-04:** the steps match the source, but the draft speaks about “the learner” in the third person rather than addressing the user; likely requires editing.
- **EV-EN-05:** says scheduling is possible but omits the requested steps and time-zone caveat; not a complete answer.
- **EV-AR-01:** the draft says to use Settings → Language, while the source specifies avatar → Profile → Language; potentially incorrect steps.
- **EV-AR-03:** cites the intended source; Arabic wording and mixed interface labels need a qualified reviewer.
- **EV-FR-03:** cites the intended source and supplies the requested steps, but French grammar and sendability need a qualified reviewer.
- **EV-AR-04:** the answer changes the source navigation and condition, and concerns an attendance certificate. The case label says no handoff, but `governance.md` states certificate requests are human-only. This label/rule conflict needs team resolution; the output was L2, so the demo indicated human review before any send. Do not interpret the 24/24 handoff-labelled result as proof that every sensitive ticket was caught.

These are assistant observations, not final independent grades. `grader_1_blank.csv` and `grader_2_blank.csv` contain only the seven drafts, without grades. Two people should independently compare the drafts to the labelled expectations and cited articles, then resolve disagreements. Arabic review availability must be confirmed; no reviewer has been assigned here.

## Data and reproducibility

`results.jsonl` contains the complete per-case output. `eval_set_v0.csv`, `prototype/` and `manifest.json` are frozen copies; previous `evals/report_v0.md`, `evals/run_v0.csv` and `evals/local_model_v1/` were not overwritten. The run is resumable with `P5_EVAL_RUN=local_model_v2`, but completed records will not be repeated. Do not tune against these cases and report the resulting score as independent. The aliases for Spanish resource questions were developed using demo cases after the earlier run; this is another reason the present comparison is not held out.
