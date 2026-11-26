"""Run a frozen local-model evaluation without overwriting earlier results."""
import csv
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN_NAME = os.getenv("P5_EVAL_RUN", "local_model_v1")
if not RUN_NAME.startswith("local_model_") or not RUN_NAME.replace("_", "").isalnum():
    raise ValueError("Invalid evaluation run name")
RUN = ROOT / "evals" / RUN_NAME
SNAPSHOT = RUN / "prototype"
SOURCES = ("router.py", "route_rule.py", "retrieve.py", "draft.py", "policy.py", "pipeline.py", "simple_pipeline.py", "switch.json")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def setup():
    RUN.mkdir(parents=True, exist_ok=False)
    SNAPSHOT.mkdir()
    for name in SOURCES:
        shutil.copy2(ROOT / "prototype" / name, SNAPSHOT / name)
    for directory in ("kb", "data"):
        shutil.copytree(ROOT / "prototype" / directory, SNAPSHOT / directory)
    shutil.copy2(ROOT / "evals" / "eval_set_v0.csv", RUN / "eval_set_v0.csv")
    files = sorted(p for p in RUN.rglob("*") if p.is_file())
    manifest = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "dataset": "eval_set_v0.csv; 51 cases; reused for development comparison",
        "ollama_model": "qwen2.5:1.5b",
        "retrieval_mode": "semantic; paraphrase-multilingual",
        "files_sha256": {str(p.relative_to(RUN)).replace("\\", "/"): sha(p) for p in files},
    }
    (RUN / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def run():
    if not RUN.exists():
        setup()
    manifest = json.loads((RUN / "manifest.json").read_text(encoding="utf-8"))
    for name, digest in manifest["files_sha256"].items():
        if sha(RUN / name) != digest:
            raise RuntimeError(f"Frozen file changed: {name}")
    os.environ["OLLAMA_MODEL"] = "qwen2.5:1.5b"
    os.environ["RETRIEVAL_MODE"] = "semantic"
    sys.path.insert(0, str(SNAPSHOT))
    if (SNAPSHOT / "simple_pipeline.py").exists():
        import simple_pipeline as pipeline
    else:
        import pipeline
    with (RUN / "eval_set_v0.csv").open(encoding="utf-8-sig", newline="") as f:
        cases = list(csv.DictReader(f))
    output = RUN / "results.jsonl"
    completed = set()
    if output.exists():
        completed = {json.loads(line)["id"] for line in output.read_text(encoding="utf-8").splitlines() if line}
    with output.open("a", encoding="utf-8") as f:
        for row in cases:
            if row["id"] in completed:
                continue
            result = pipeline.run_one(row["input_the_agent_receives"])
            entry = {"id": row["id"], "language_expected": row["segment"].split("·")[0].strip(),
                     "expected_handoff": row["hand_over_to_a_person"],
                     "question": row["input_the_agent_receives"],
                     "expected_action": row["expected_output_or_action"], **result}
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            f.flush()
            print(f"{len(completed) + 1}/{len(cases)} {row['id']}: {result['decision']}", flush=True)
            completed.add(row["id"])


if __name__ == "__main__":
    run()
