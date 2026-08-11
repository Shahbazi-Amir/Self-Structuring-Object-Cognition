from __future__ import annotations

import json
from pathlib import Path
import unittest

from rational_core import AssessmentStatus, Polarity, Proposition, RationalCore
from rational_core.cli import assess_payload


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "contradiction_cases.json"


class ContradictionFixtureTests(unittest.TestCase):
    def test_all_predeclared_cases(self) -> None:
        cases = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(cases), 10)
        for case in cases:
            with self.subTest(case=case["case_id"]):
                result = assess_payload(case)
                self.assertEqual(case["expected"], result["status"])


class RationalCoreUnitTests(unittest.TestCase):
    def proposition(self, proposition_id: str, **overrides: object) -> Proposition:
        values = {
            "subject": "الف",
            "relation": "هست",
            "object": "ب",
            "polarity": Polarity.AFFIRM,
            "context": "جهان آزمون",
            "time": "t1",
            "source": "unit-test",
        }
        values.update(overrides)
        return Proposition(proposition_id=proposition_id, **values)  # type: ignore[arg-type]

    def test_trace_identifies_evidence_and_reason(self) -> None:
        core = RationalCore(
            [
                self.proposition("positive"),
                self.proposition("negative", polarity=Polarity.DENY),
            ]
        )
        assessment = core.assess()
        self.assertEqual(AssessmentStatus.CONTRADICTORY, assessment.status)
        self.assertEqual(1, len(assessment.contradictions))
        judgment = assessment.contradictions[0]
        self.assertEqual("positive", judgment.left_id)
        self.assertEqual("negative", judgment.right_id)
        self.assertEqual("same_identity_opposite_polarity", judgment.reason_code)

    def test_duplicate_proposition_ids_are_rejected(self) -> None:
        core = RationalCore([self.proposition("same")])
        with self.assertRaisesRegex(ValueError, "duplicate proposition_id"):
            core.add(self.proposition("same"))

    def test_blank_required_field_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "subject must not be blank"):
            self.proposition("p1", subject="  ")

    def test_memory_view_is_immutable_tuple(self) -> None:
        core = RationalCore([self.proposition("p1")])
        self.assertIsInstance(core.propositions, tuple)

    def test_assessment_is_independent_of_insertion_order(self) -> None:
        positive = self.proposition("p1")
        negative = self.proposition("p2", polarity=Polarity.DENY)
        first = RationalCore([positive, negative]).assess().status
        second = RationalCore([negative, positive]).assess().status
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()

