# 03 — AI Lean Canvas · P5 Multilingual LMS support agent

> One screen. Nine blocks from the classic Lean Canvas (Ash Maurya) + five blocks that an AI product cannot skip.
> Fill it from your files: most answers already exist in 01, 02 and 03_product_brief.md. Short phrases, not paragraphs.

## The nine classic blocks
| Block | Our answer | Comes from |
|---|---|---|
| 1. Problem — top 3 pains | PT / PL / AR tickets wait 2–3× longer (measured, proposal) · agents spend ≈ 9 of 14 min searching the English KB and translating (guess) · quality per language is invisible in an average KPI | 01 |
| 2. Users / customer segments | Multilingual tier-1 support agents (20) · learners, instructors and admins of universities and corporate academies in 14 countries, 6 languages | 01 (persona) |
| 3. Unique value proposition — one sentence | A correct, cited answer in your own language from our one trusted English knowledge base — and a native speaker whenever it matters | 01 (press release) |
| 4. Solution — the MUST features | Language detection + sensitive router + hand-off note · per-language switch L3 / L2 / off + per-language eval report · cited answer in the customer's language | 03 brief §3 |
| 5. Channels — where it lives | LMS help-centre chat (L3 languages) · helpdesk console of the native-speaking agents (L2 drafts, hand-offs) | 03 brief §6 |
| 6. Value — what it is worth per year (base case, EV) | Base **€66k** net year 1 · EV **€72k** · do-nothing €60k · hurdle €50k → conditional go | 02 |
| 7. Cost structure — the seven cost lines | Integration €18k/yr (€55k over 3 yrs) · evaluation €20k · supervision €30k (0.5 FTE) · monitoring €15k · re-evaluation €12k · AI tokens €1.7k · wrong answers €10.9k | 02 |
| 8. Key metric — the success criterion | ≥ 57 % of automatable core-language tickets sendable without edit (two native-speaker graders, 200-case eval-set), 100 % of sensitive tickets handed over, PT / PL / AR reported separately | 03 brief §7 |
| 9. Unfair advantage — data or know-how nobody else has | Our English KB, our sensitive-request rules for education, our per-language eval-sets graded by native speakers — the workflow, not the model (orchestrate 3.30 vs buy 3.05) | 02 (build / buy) |

## The five AI blocks
| Block | Our answer | Comes from |
|---|---|---|
| 10. Data — sources, rights, gaps | English KB (ours) · invented eval-set, human-labelled, no real customer data · processor under the LMS DPA, Art. 9 health data in accessibility requests · gaps: no ticket logs, no PL / AR graders yet | governance.md · S3 |
| 11. Model — rung per part | Language ID: 2 · sensitive router: 4 (rules OR classifier) · retrieval: 3 (multilingual embeddings + keywords) · answer: 3 (LLM via API, no fine-tuning) · gate, switch, logs: 1 (rules) | 03 brief §5 |
| 12. Evaluation — the eval-set and its size | `evals/eval_set_v0.csv`: 20 cases now (7 core, 5 PT, 4 PL, 3 AR, 1 unsupported; 10 hand-overs) → 50 (A4) → 200 (S5); two graders, per-language report | evals/ |
| 13. Human in the loop — trust level per step, way back to a person | Language ID, routing, gate, logs L4 · retrieval L3 · answer L3 core / L2 PT, PL, AR · sensitive = person only · "talk to a person" button + native-speaker queue + per-language switch | 03 brief §2 |
| 14. Risks & governance — what it must never do, rollback trigger | Never answer grades, assessments, certificates, accessibility, personal-data requests; never answer without a cited source; never show one institution's data to another · rollback: one sensitive ticket answered or a language below threshold → that language to L2 the same day | governance.md |
