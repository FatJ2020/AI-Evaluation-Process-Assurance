"""Run AEPA on synthetic review sessions and write CSV."""

from __future__ import annotations
import argparse
import csv
import json
import sys
from pathlib import Path

# Allow `python src/aepa_run.py` from repo root
sys.path.insert(0, str(Path(__file__).resolve().parent))
from aepa_rules import evaluate_session


def load_sessions(path: Path):
    sessions = []
    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                sessions.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSON on line {line_no}: {exc}")
    if not sessions:
        raise SystemExit("No sessions found.")
    return sessions


def main():
    parser = argparse.ArgumentParser(description="AEPA evaluation-process assurance runner")
    parser.add_argument("--input", default="data/review_sessions.jsonl")
    parser.add_argument("--output", default="reports/aepa_results.csv")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    sessions = load_sessions(input_path)
    results = [evaluate_session(s) for s in sessions]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(results[0].keys())
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    print("AEPA — Evaluation Process Assurance")
    print(f"Evaluated {len(results)} review sessions -> {output_path}")
    print()
    for r in results:
        print(
            f"{r['session_id']:10}  severity={r['severity']}  "
            f"flags={r['flags'][:40]:40}  -> {r['recommendation']}"
        )
    print()
    print("Note: synthetic data; rules are illustrative. Severity is H/M/L, not RPN.")


if __name__ == "__main__":
    main()
