"""JSON command-line interface for controlled rational-core experiments."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

from .core import RationalCore
from .model import Polarity, Proposition


def proposition_from_dict(payload: dict[str, Any]) -> Proposition:
    return Proposition(
        proposition_id=payload["id"],
        subject=payload["subject"],
        relation=payload["relation"],
        object=payload["object"],
        polarity=Polarity(payload["polarity"]),
        context=payload.get("context"),
        time=payload.get("time"),
        source=payload["source"],
        metadata=payload.get("metadata", {}),
    )


def assess_payload(payload: dict[str, Any]) -> dict[str, Any]:
    raw_propositions = payload.get("propositions")
    if not isinstance(raw_propositions, list):
        raise ValueError("top-level 'propositions' must be a list")
    core = RationalCore(proposition_from_dict(item) for item in raw_propositions)
    return core.assess().to_dict()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rational-core",
        description="Assess controlled propositions for direct contradiction.",
    )
    parser.add_argument("input", type=Path, help="UTF-8 JSON input file")
    parser.add_argument("--pretty", action="store_true", help="indent JSON output")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        result = assess_payload(payload)
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False))
        return 2
    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2 if args.pretty else None,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

