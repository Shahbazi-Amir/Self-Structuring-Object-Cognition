"""Deterministic contradiction assessment for rational-core 0.1."""

from __future__ import annotations

from itertools import combinations
from typing import Iterable

from .model import (
    Assessment,
    AssessmentStatus,
    PairJudgment,
    PairStatus,
    Proposition,
)


class RationalCore:
    """Append-only proposition memory with explicit contradiction judgments."""

    def __init__(self, propositions: Iterable[Proposition] = ()) -> None:
        self._propositions: list[Proposition] = []
        self._ids: set[str] = set()
        for proposition in propositions:
            self.add(proposition)

    @property
    def propositions(self) -> tuple[Proposition, ...]:
        return tuple(self._propositions)

    def add(self, proposition: Proposition) -> Proposition:
        if not isinstance(proposition, Proposition):
            raise TypeError("proposition must be a Proposition")
        if proposition.proposition_id in self._ids:
            raise ValueError(f"duplicate proposition_id: {proposition.proposition_id}")
        self._ids.add(proposition.proposition_id)
        self._propositions.append(proposition)
        return proposition

    def compare(self, left: Proposition, right: Proposition) -> PairJudgment:
        """Compare two propositions without using unstated world knowledge."""

        if left.semantic_key != right.semantic_key:
            return self._judgment(
                left,
                right,
                PairStatus.UNRELATED,
                "different_semantic_key",
                "موضوع، نسبت یا محمول یکسان نیست؛ این زوج تناقض مستقیم نیست.",
            )

        if left.polarity is right.polarity:
            return self._judgment(
                left,
                right,
                PairStatus.COMPATIBLE,
                "same_polarity",
                "دو گزاره دربارهٔ یک ساختار معنایی، قطب یکسان دارند.",
            )

        scope_status, scope_reason = self._compare_scope(left, right)
        if scope_status == "different":
            return self._judgment(
                left,
                right,
                PairStatus.COMPATIBLE,
                "different_scope",
                "قطب‌ها مخالف‌اند، اما زمان یا زمینه متفاوت است.",
            )
        if scope_status == "unknown":
            return self._judgment(
                left,
                right,
                PairStatus.INDETERMINATE,
                "incomplete_scope",
                f"قطب‌ها مخالف‌اند، اما {scope_reason} برای احراز وحدت کامل نیست.",
            )
        return self._judgment(
            left,
            right,
            PairStatus.CONTRADICTION,
            "same_identity_opposite_polarity",
            "موضوع، نسبت، محمول، زمان و زمینه یکسان و قطب‌ها مخالف‌اند.",
        )

    def assess(self) -> Assessment:
        judgments = tuple(
            self.compare(left, right)
            for left, right in combinations(self._propositions, 2)
        )
        statuses = {judgment.status for judgment in judgments}
        if PairStatus.CONTRADICTION in statuses:
            status = AssessmentStatus.CONTRADICTORY
        elif PairStatus.INDETERMINATE in statuses:
            status = AssessmentStatus.INDETERMINATE
        else:
            status = AssessmentStatus.CONSISTENT
        return Assessment(
            status=status,
            proposition_count=len(self._propositions),
            judgments=judgments,
        )

    @staticmethod
    def _compare_scope(left: Proposition, right: Proposition) -> tuple[str, str]:
        unknown_dimensions: list[str] = []
        for label, left_value, right_value in (
            ("زمینه", left.context, right.context),
            ("زمان", left.time, right.time),
        ):
            if left_value is not None and right_value is not None:
                if left_value != right_value:
                    return "different", label
            else:
                unknown_dimensions.append(label)
        if unknown_dimensions:
            return "unknown", " و ".join(unknown_dimensions)
        return "same", ""

    @staticmethod
    def _judgment(
        left: Proposition,
        right: Proposition,
        status: PairStatus,
        reason_code: str,
        explanation: str,
    ) -> PairJudgment:
        return PairJudgment(
            left_id=left.proposition_id,
            right_id=right.proposition_id,
            status=status,
            reason_code=reason_code,
            explanation=explanation,
        )

