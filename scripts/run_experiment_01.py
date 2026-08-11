"""Run the preregistered contradiction cases against core 0.1 and a naive baseline."""

from __future__ import annotations

from itertools import combinations
import json
from pathlib import Path
from typing import Any

from rational_core.cli import assess_payload, proposition_from_dict


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "tests" / "fixtures" / "contradiction_cases.json"


def naive_baseline(payload: dict[str, Any]) -> str:
    """Ignore context/time and collapse every opposite semantic pair."""

    propositions = [proposition_from_dict(item) for item in payload["propositions"]]
    for left, right in combinations(propositions, 2):
        if left.semantic_key == right.semantic_key and left.polarity is not right.polarity:
            return "contradictory"
    return "consistent"


def score(predictions: list[dict[str, str]]) -> dict[str, Any]:
    correct = sum(row["expected"] == row["actual"] for row in predictions)
    return {
        "correct": correct,
        "total": len(predictions),
        "accuracy": correct / len(predictions) if predictions else 0.0,
        "errors": [row for row in predictions if row["expected"] != row["actual"]],
    }


def run() -> dict[str, Any]:
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    core_rows: list[dict[str, str]] = []
    baseline_rows: list[dict[str, str]] = []
    for case in cases:
        expected = case["expected"]
        core_rows.append(
            {
                "case_id": case["case_id"],
                "expected": expected,
                "actual": assess_payload(case)["status"],
            }
        )
        baseline_rows.append(
            {
                "case_id": case["case_id"],
                "expected": expected,
                "actual": naive_baseline(case),
            }
        )
    return {"rational_core_0_1": score(core_rows), "naive_baseline": score(baseline_rows)}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))

