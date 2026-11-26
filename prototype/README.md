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

## Using the multilingual model drafter

The optional model path sends the ticket and retrieved fictional KB passages to the configured provider and asks for a cited answer in the ticket language. Use only invented data unless the team has approved the necessary provider and data-processing arrangements. The policy checker runs after generation; its checks do not prove factual accuracy, and a human must review outputs for evaluation.

Install Python 3.11+ and the base dependencies above. Then install **one** optional provider package: `python -m pip install anthropic` or `python -m pip install google-genai`.

In PowerShell, set a key in the current terminal (do not paste or commit the actual key in a project file):

```powershell
$env:ANTHROPIC_API_KEY = "<your-key>"
# Alternatively, use $env:GEMINI_API_KEY for Gemini.
python prototype/app.py "<fictional development ticket>"
```

In Git Bash use `export ANTHROPIC_API_KEY="<your-key>"` (or `GEMINI_API_KEY`) instead. If both are set, Anthropic is selected first. The optional `MODEL` environment variable overrides the default model for the selected provider; set a compatible model when needed. `.env.example` is documentation only and is not loaded automatically.

When no key is configured, the existing English template is used. When a provider call fails, the prototype currently falls back to that template; the policy checker may then block a non-English answer. A draft requires a retrieved source and the routing and policy checks to pass. A configured model has not yet been evaluated on this machine, and the router and retrieval limitations remain. Do not overwrite the existing `evals/run_v0.csv` when preparing a future evaluation: the current evaluation command writes to that path.

## Local Ollama model (no API key)

Install Ollama and download the small multilingual model with `ollama pull qwen2.5:1.5b`. Ensure Ollama is running. In PowerShell, from the repository root:

```powershell
.\.venv\Scripts\Activate.ps1
$env:OLLAMA_MODEL = "qwen2.5:1.5b"
python prototype/app.py "How do I change my profile photo?"
```

In Git Bash use `source .venv/Scripts/activate` and `export OLLAMA_MODEL=qwen2.5:1.5b`. Ollama takes priority over configured cloud keys. Without `OLLAMA_MODEL`, existing API or template behavior remains. If Ollama is enabled but unavailable, the ticket is handed over. The model only runs after the existing router and retrieval have passed; those stages may still hand over a routine question. Outputs need human review; no local model performance has been evaluated yet. The endpoint is fixed to `127.0.0.1:11434`.

For the local demo, only the top retrieved passage is sent to Ollama. Common refusal-style outputs are handed off, and Ollama performs a second check for relevance and support before the citation is attached. The check can miss unsupported statements: a development retest passed a draft that incorrectly instructed the user to set an institution-controlled time zone. The citation records the source supplied; it does not prove the claims. Always review the answer against the article before sending. For the presentation demo, English, French and Spanish are L3; Portuguese and Arabic are L2, and Polish is off. The prototype returns decisions but does not implement a real approval interface or human queue.

## Local multilingual search

Optionally download the embedding model once with `ollama pull paraphrase-multilingual`. Start Ollama, then set **both** variables to enable local search and local drafting:

```bash
source .venv/Scripts/activate
export RETRIEVAL_MODE=semantic
export OLLAMA_MODEL=qwen2.5:1.5b
python prototype/app.py "How do I change my profile photo?"
```

Semantic search compares the ticket with English KB passages using a local multilingual embedding model. The KB vectors are cached only for the life of the process, so the first request can be slow. The minimum similarity (0.50) and margin over the next different article (0.04) are **provisional**, not calibrated probabilities or safety guarantees. Weak, ambiguous, unavailable or invalid embedding results return no source, leading to handoff; the system does not silently fall back to TF-IDF in semantic mode. Unset `RETRIEVAL_MODE` to use the original TF-IDF retriever. The router and other policy limitations still apply.

Run `python prototype/check_retrieval_demo.py` to compare the two retrievers on six development questions (not a held-out evaluation). On this machine, the semantic mode ranked the intended article first on 4/6 and handed off 2/6; TF-IDF ranked it first on 2/6. This is too small to establish quality or choose a production threshold. Preserve the frozen evaluation outputs, and evaluate a later frozen version on separately labelled cases before claiming performance.

## Presentation interface
Run `python prototype/demo_server.py` from the project root, then open http://127.0.0.1:8765. Use invented questions only; the demo does not send tickets to a human queue.

For uncertain language detection in local Ollama mode, the router asks the local model to confirm the classifier's proposed language. If they disagree or the model is unavailable, it hands off. This is a demo heuristic, not calibrated confidence or proof of language accuracy; other routing, source and policy checks still apply.

Development update: the router can ask the local model to confirm uncertain routine classifications; explicit security and sensitive rules still take precedence. Semantic search uses multilingual article descriptions (`kb/search_aliases.json`), and for ambiguous candidates can ask the local model to choose a source or abstain. Both checks are experimental and can be wrong; they do not prove a request is safe or an answer grounded. Polish remains off. The 51-case results under `evals/local_model_v1/` were created before this change and remain unchanged. Retesting the same cases would be a development comparison, not an independent evaluation.

Search update: translated article descriptions are now embedded separately from the English passage, so a relevant short description is not diluted by unrelated wording. The language policy may use the local model for a second opinion when the small language classifier disagrees; an unconfirmed mismatch is blocked. These model checks are experimental and cannot guarantee correctness. In development, the Spanish enrolled-courses question now retrieves the correct source and generates an answer, but that draft had grammatical mistakes and needs review. The previously frozen evaluation results are unchanged.

## Current simplified presentation flow

The browser demo now calls `simple_pipeline.py`: language/category routing and handoff rules → local multilingual source search → local model draft → citation/language/policy check. For ambiguous retrieval it hands off instead of making an additional model reranking call. The existing compact classifier is retained because the 1.5B model alone misclassified demo languages; the local model can confirm uncertain detections. The local drafter retains a model-based source check, which is imperfect. The system returns a simulated handoff, not a real human queue. English, French and Spanish are L3 for fictional demonstration only; Portuguese/Arabic remain L2 and Polish off. No new independent evaluation of this simplified version has been completed. Historical v0/v1/v2 evaluations refer to earlier implementations.
