# /prototype — P5 multilingual LMS support agent · v0

The smallest workflow that can pass or fail our success criterion (`03_product_brief.md` §7). Built from `spec.md`, on the structure of the Session 4 Paylio demo. Runs **without an API key** (template drafter), as Assignment 4 allows.

```
ticket ─▶ [1 router] ─▶ [2 routing rule] ─▶ [3 retrieve + draft] ─▶ [4 policy check] ─▶ send (L3) or ⊘ native speaker approves (L2)
             │                 │ sensitive · security · language not covered · low confidence      │ block
             └─────────────────┴────────────────────────▶ ⊘ native-speaking person ◀───────────────┘
⏻ switch.json — per language L3 / L2 / off (Head of Support)
```

| Step | File | What it does |
|---|---|---|
| 1 · router | `router.py` | language (en, fr, es, pt, pl, ar, other) and category (how_do_i, sensitive, security, technical), each with a confidence — TF-IDF on characters + logistic regression, trained on `data/tickets_synthetic.csv` |
| 2 · routing rule | `route_rule.py` | rules: language not covered, switch off, security, sensitive (governance.md row 4), low confidence → a person |
| 3 · retrieve + draft | `retrieve.py`, `draft.py`, `kb/` | top-3 passages from the English KB, then a draft that cites them; an LLM if `ANTHROPIC_API_KEY` or `GEMINI_API_KEY` is set, else the template drafter |
| 4 · policy check | `policy.py` | blocks: no citation, citation not retrieved, grade / deletion / certificate promises, secrets, language mismatch |
| workflow | `pipeline.py` | the four steps in a fixed order, no loop, no tools |
| eval | `evals.py` | runs `evals/eval_set_v0.csv`, writes `evals/run_v0.csv` for the two graders |

## Run it

```shell
python -m pip install -r prototype/requirements.txt
python prototype/app.py "How do I change my profile photo?"
python prototype/evals.py
```
Then two graders fill `grader_1` and `grader_2` (yes / no, independently) in `evals/run_v0.csv`, and:
```shell
python prototype/evals.py --grades evals/run_v0.csv
```

## Data
- `kb/` — 35 fictional English help articles written by the team (no real product).
- `data/tickets_synthetic.csv` — 156 synthetic training tickets: 144 in the 6 languages (24 per language) + 12 in other languages, written for the router. **Never the eval-set.**
- `data/demo_tickets.csv` — 12 demo tickets used to debug and to demo. **Never the eval-set.**

Rule: never tune a threshold, a rule or the prompt while looking at `evals/`.
