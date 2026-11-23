"""Golden-30 grading for Assignment 5 — the two agreement rates (human-human, human-judge).

  python evals/grading.py sheet
      runs the prototype on the 30 golden cases of eval_set_v1.csv and writes
      evals/grading_30.csv (for the two graders) and evals/judge_inputs_30.md (for the judge)
  python evals/grading.py import
      copies what the team filled by hand in evals/to_fill/*.xlsx into the CSV files:
      the labels of labels_v1.xlsx into eval_set_v1.csv, the verdicts of grader_1.xlsx and
      grader_2.xlsx into grading_30.csv
  python evals/grading.py agreement
      reads grader_1, grader_2 and judge (pass / fail) in grading_30.csv and prints the
      two agreement rates for evals/README.md

The script never grades: two people fill grader_1 and grader_2 independently,
following the guideline in evals/README.md.
"""

import csv
import os
import re
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prototype")
)
import pipeline

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Windows consoles default to cp1252 and crash on non-Latin tickets (Polish, Arabic).
sys.stdout.reconfigure(encoding="utf-8")

EVAL = os.path.join(ROOT, "evals", "eval_set_v1.csv")
SHEET = os.path.join(ROOT, "evals", "grading_30.csv")
JUDGE_INPUTS = os.path.join(ROOT, "evals", "judge_inputs_30.md")
KB = os.path.join(ROOT, "prototype", "kb")
KB_ID = re.compile(r"KB-[A-Z]+(?:-[A-Z]+)?-\d+")
VERDICTS = {"pass", "fail"}


def golden_rows():
    with open(EVAL, encoding="utf-8", newline="") as f:
        return [r for r in csv.DictReader(f) if r.get("golden_30") == "yes"]


def kb_text(article):
    path = os.path.join(KB, article + ".md")
    if not os.path.exists(path):
        return f"({article}: article not found)"
    with open(path, encoding="utf-8") as f:
        return f.read().strip()


def sheet():
    out, blocks = [], []
    for r in golden_rows():
        o = pipeline.run_one(r["input_the_agent_receives"])
        draft = "" if o["draft"] == "NO_DRAFT" else o["draft"]
        if draft and o["decision"] != "draft":
            draft = "(not sent — " + o["reason"] + ") " + draft
        articles = sorted({a for c in o["citations"] for a in KB_ID.findall(c)})
        out.append(
            {
                "id": r["id"],
                "segment": r["segment"],
                "ticket": r["input_the_agent_receives"],
                "reference_expected_output": r["expected_output_or_action"],
                "reference_hand_over": r["hand_over_to_a_person"],
                "system_decision": o["decision"],
                "system_reason": o["reason"],
                "sent_to": o["send"],
                "draft": draft,
                "sources": "; ".join(o["citations"]),
                "grader_1": "",
                "grader_2": "",
                "judge": "",
                "disagreement_note": "",
            }
        )
        passages = "\n\n".join(kb_text(a) for a in articles) or "(no passage retrieved)"
        blocks.append(
            f"## {r['id']}\n\n"
            f"TICKET:\n{r['input_the_agent_receives']}\n\n"
            f"REFERENCE (what a good system does):\n{r['expected_output_or_action']}\n"
            f"Hand over to a person: {r['hand_over_to_a_person']}\n\n"
            f"SYSTEM DECISION: {o['decision']} — {o['reason'] or 'answer'}"
            f" — sent to: {o['send']}\n\n"
            f"SYSTEM DRAFT:\n{draft or '(none)'}\n\n"
            f"KB PASSAGES RETRIEVED:\n{passages}\n"
        )
    with open(SHEET, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    with open(JUDGE_INPUTS, "w", encoding="utf-8") as f:
        f.write(
            "# Judge inputs — golden 30\n\n"
            "Paste `evals/judge_prompt.txt`, then ONE block below, into the chat. "
            "Copy the final verdict (pass / fail) into the `judge` column of "
            "`evals/grading_30.csv`.\n\n"
        )
        f.write("\n---\n\n".join(blocks))
    print(f"{len(out)} cases -> {SHEET}\n            -> {JUDGE_INPUTS}")


def _xlsx_rows(path, sheet, header_row):
    from openpyxl import load_workbook

    ws = load_workbook(path, data_only=True)[sheet]
    rows = list(ws.iter_rows(min_row=header_row, values_only=True))
    head = [str(h) for h in rows[0]]
    return ws, [
        dict(zip(head, ["" if v is None else str(v).strip() for v in r], strict=True))
        for r in rows[1:]
        if r[0]
    ]


def import_manual():
    folder = os.path.join(ROOT, "evals", "to_fill")
    # 1. labels written by the team
    _, labels = _xlsx_rows(os.path.join(folder, "labels_v1.xlsx"), "To label", 1)
    labels = {r["id"]: r for r in labels}
    with open(EVAL, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    done, missing = 0, []
    for r in rows:
        lab = labels.get(r["id"])
        if not lab or r["hand_over_to_a_person"]:
            continue
        keys = ("expected_output_or_action", "evidence_or_source", "hand_over_to_a_person")
        if not all(lab[k] for k in keys) or not lab["labelled_by"]:
            missing.append(r["id"])
            continue
        for k in keys:
            r[k] = lab[k]
        r["origin"] = "AI-generated input · labelled by " + lab["labelled_by"]
        done += 1
    with open(EVAL, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(
        f"labels: {done} rows written into eval_set_v1.csv · still incomplete: {missing or 'none'}"
    )
    # 2. verdicts of the two graders
    with open(SHEET, encoding="utf-8", newline="") as f:
        sheet_rows = list(csv.DictReader(f))
    for n in (1, 2):
        ws, graded = _xlsx_rows(os.path.join(folder, f"grader_{n}.xlsx"), "Grade", 3)
        name = "" if ws["B1"].value is None else str(ws["B1"].value).strip()
        graded = {r["id"]: r for r in graded}
        count = 0
        for r in sheet_rows:
            g = graded.get(r["id"], {})
            verdict = g.get("verdict", "").lower()
            if verdict in VERDICTS:
                r[f"grader_{n}"] = verdict
                count += 1
            if g.get("comment"):
                note = f"g{n} ({name}): {g['comment']}"
                r["disagreement_note"] = " | ".join(x for x in (r["disagreement_note"], note) if x)
        print(
            f"grader_{n} ({name or 'name missing'}): {count} / {len(sheet_rows)} verdicts imported"
        )
    with open(SHEET, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(sheet_rows[0].keys()))
        w.writeheader()
        w.writerows(sheet_rows)


def kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b, strict=True)) / n
    pe = sum((a.count(v) / n) * (b.count(v) / n) for v in VERDICTS)
    return po, (po - pe) / (1 - pe) if pe < 1 else 1.0


def report(name, rows, col_a, col_b):
    pairs = [(r[col_a], r[col_b]) for r in rows if r[col_a] in VERDICTS and r[col_b] in VERDICTS]
    if not pairs:
        print(f"{name:32s} not graded yet")
        return
    a, b = [p[0] for p in pairs], [p[1] for p in pairs]
    po, k = kappa(a, b)
    print(f"{name:32s} {po:.0%} agreement on {len(pairs)} cases · Cohen's kappa {k:.2f}")
    for r in rows:
        if r[col_a] in VERDICTS and r[col_b] in VERDICTS and r[col_a] != r[col_b]:
            print(f"    disagree on {r['id']}: {col_a}={r[col_a]} {col_b}={r[col_b]}")


def agreement():
    with open(SHEET, encoding="utf-8", newline="") as f:
        rows = [
            {
                k: (v or "").strip().lower() if k in ("grader_1", "grader_2", "judge") else v
                for k, v in r.items()
            }
            for r in csv.DictReader(f)
        ]
    report("human-human (grader_1 vs grader_2)", rows, "grader_1", "grader_2")
    report("human-judge (grader_1 vs judge)", rows, "grader_1", "judge")
    report("human-judge (grader_2 vs judge)", rows, "grader_2", "judge")
    both = [r for r in rows if r["grader_1"] in VERDICTS and r["grader_1"] == r["grader_2"]]
    report(
        "judge vs the graders' consensus",
        [dict(r, consensus=r["grader_1"]) for r in both],
        "consensus",
        "judge",
    )
    passed = [r for r in both if r["grader_1"] == "pass"]
    if both:
        print(f"\npass rate (graders agree) {len(passed)}/{len(both)}")


if __name__ == "__main__":
    {"sheet": sheet, "import": import_manual, "agreement": agreement}.get(
        sys.argv[1] if len(sys.argv) > 1 else "", lambda: print(__doc__)
    )()
