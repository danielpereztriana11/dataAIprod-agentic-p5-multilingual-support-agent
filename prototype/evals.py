"""Run the prototype on evals/eval_set_v0.csv. Never tune while looking at these rows.
  python prototype/evals.py                 -> runs, prints the automatic numbers, writes evals/run_v0.csv for the graders
  python prototype/evals.py --grades FILE   -> reads grader_1 / grader_2 (yes/no) and prints the success criterion
Sendable without editing is decided by two people, never by this script."""

import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd

# Windows consoles default to cp1252 and crash on arrows and non-Latin answers (Polish, Arabic).
sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVAL = os.path.join(ROOT, "evals", "eval_set_v0.csv")
OUT = os.path.join(ROOT, "evals", "run_v0.csv")
CRITERION = 0.57
CORE = {"en", "fr", "es"}
KB_ID = re.compile(r"KB-[A-Z]+(?:-[A-Z]+)?-\d+")


def expected(row):
    lang = row["segment"].split("·")[0].strip()
    return dict(
        lang=lang if lang in {"en", "fr", "es", "pt", "pl", "ar"} else "other",
        handover=str(row["hand_over_to_a_person"]).strip().lower().startswith("yes"),
        articles=set(KB_ID.findall(str(row["evidence_or_source"]))),
    )


def run():
    import pipeline

    df = pd.read_csv(EVAL)
    rows = []
    for _, r in df.iterrows():
        e = expected(r)
        o = pipeline.run_one(r["input_the_agent_receives"])
        cited = set(KB_ID.findall(o["draft"]))
        retrieved = {c.split(" · ")[0] for c in o["citations"]}
        rows.append(
            {
                "id": r["id"],
                "lang_expected": e["lang"],
                "lang_detected": o["language"],
                "handover_expected": e["handover"],
                "decision": o["decision"],
                "reason": o["reason"],
                "hit@3": (
                    bool(e["articles"] & retrieved)
                    if e["articles"] and not e["handover"] and o["citations"]
                    else None
                ),
                "auto_ok": o["decision"] == "draft" and bool(e["articles"] & cited),
                "ticket": r["input_the_agent_receives"],
                "expected_output": r["expected_output_or_action"],
                "draft": o["draft"] if o["decision"] == "draft" else "",
                "sources": "; ".join(o["citations"]),
                "grader_1": "",
                "grader_2": "",
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(OUT, index=False, quoting=csv.QUOTE_NONNUMERIC)
    show = out[
        [
            "id",
            "lang_expected",
            "lang_detected",
            "handover_expected",
            "decision",
            "reason",
            "hit@3",
            "auto_ok",
        ]
    ]
    print(show.to_string(index=False))
    sens = out[out["handover_expected"]]
    auto = out[~out["handover_expected"]]
    core = auto[auto["lang_expected"].isin(CORE)]
    print(
        f"\ncases                          {len(out)}  ({len(sens)} hand-over, {len(auto)} automatable, {len(core)} automatable core-language)"
    )
    print(
        f"language accuracy              {(out['lang_expected'] == out['lang_detected']).mean():.0%}"
    )
    print(
        f"hand-over recall               {(sens['decision'] == 'escalate').mean():.0%}   (must be 100 %)"
    )
    print(
        f"drafts on hand-over tickets    {int((sens['decision'] == 'draft').sum())}   (must be 0)"
    )
    print(f"automatable tickets drafted    {int((auto['decision'] == 'draft').sum())}/{len(auto)}")
    print(
        f"retrieval hit@3                {out['hit@3'].dropna().astype(bool).mean():.0%}  (on {out['hit@3'].notna().sum()} cases with sources)"
    )
    print(
        f"drafts grounded + pass + right article (automatic)  core {int(core['auto_ok'].sum())}/{len(core)}"
    )
    print("\nby language (automatable): drafted / auto_ok / n")
    for l, g in auto.groupby("lang_expected"):
        print(
            f"  {l:5s} {int((g['decision'] == 'draft').sum()):2d} / {int(g['auto_ok'].sum()):2d} / {len(g)}"
        )
    print("\nescalation reasons on automatable tickets:")
    for k, v in (
        auto[auto["decision"] == "escalate"]["reason"]
        .str.replace(r"\(.*\)", "", regex=True)
        .value_counts()
        .items()
    ):
        print(f"  {v:2d} × {k.strip()}")
    print(
        f"\n-> {OUT} written. Two graders fill grader_1 and grader_2 (yes/no) independently, then: python prototype/evals.py --grades evals/run_v0.csv"
    )


def grades(path):
    g = pd.read_csv(path)
    eval_df = pd.read_csv(EVAL).set_index("id")
    g["handover_expected"] = g["id"].map(lambda i: expected(eval_df.loc[i])["handover"])
    yes = lambda s: s.astype(str).str.strip().str.lower().isin(["yes", "y", "oui", "1", "true"])
    g["sendable"] = (g["decision"] == "draft") & yes(g["grader_1"]) & yes(g["grader_2"])
    auto = g[~g["handover_expected"]]
    core = auto[auto["lang_expected"].isin(CORE)]
    drafted = g[g["decision"] == "draft"]
    disagree = int((yes(drafted["grader_1"]) != yes(drafted["grader_2"])).sum())
    rate = core["sendable"].mean() if len(core) else 0
    print(
        f"sendable without editing (both graders), core languages: {int(core['sendable'].sum())}/{len(core)} = {rate:.0%}   (criterion {CRITERION:.0%})"
    )
    for l, x in auto.groupby("lang_expected"):
        print(f"  {l:5s} {int(x['sendable'].sum())}/{len(x)}")
    print(f"grader disagreements on drafts: {disagree}")
    print(
        "verdict:",
        "criterion met"
        if rate >= CRITERION
        else "criterion NOT met — do not fix the prompt on these rows; turn the misses into spec.md v2",
    )


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--grades":
        grades(sys.argv[2])
    else:
        run()
