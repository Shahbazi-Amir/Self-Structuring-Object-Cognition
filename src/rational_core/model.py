"""Explicit data types used by the rational core.

Version 0.1 intentionally accepts a controlled symbolic representation. Natural
language parsing, probabilistic inference, learning, and belief revision are out
of scope.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import unicodedata
from types import MappingProxyType
from typing import Any, Mapping


def normalize_symbol(value: str, field_name: str) -> str:
    """Return a stable Unicode/whitespace representation for symbolic values."""

    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = " ".join(unicodedata.normalize("NFKC", value).split())
    if not normalized:
        raise ValueError(f"{field_name} must not be blank")
    return normalized


def normalize_optional_symbol(value: str | None, field_name: str) -> str | None:
    if value is None:
        return None
    return normalize_symbol(value, field_name)


class Polarity(str, Enum):
    AFFIRM = "affirm"
    DENY = "deny"


class PairStatus(str, Enum):
    CONTRADICTION = "contradiction"
    COMPATIBLE = "compatible"
    INDETERMINATE = "indeterminate"
    UNRELATED = "unrelated"


class AssessmentStatus(str, Enum):
    CONTRADICTORY = "contradictory"
    CONSISTENT = "consistent"
    INDETERMINATE = "indeterminate"


@dataclass(frozen=True, slots=True)
class Proposition:
    """A controlled proposition with explicit identity and provenance fields."""

    proposition_id: str
    subject: str
    relation: str
    object: str
    polarity: Polarity
    context: str | None
    time: str | None
    source: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "proposition_id", normalize_symbol(self.proposition_id, "proposition_id")
        )
        object.__setattr__(self, "subject", normalize_symbol(self.subject, "subject"))
        object.__setattr__(self, "relation", normalize_symbol(self.relation, "relation"))
        object.__setattr__(self, "object", normalize_symbol(self.object, "object"))
        object.__setattr__(self, "context", normalize_optional_symbol(self.context, "context"))
        object.__setattr__(self, "time", normalize_optional_symbol(self.time, "time"))
        object.__setattr__(self, "source", normalize_symbol(self.source, "source"))
        if not isinstance(self.polarity, Polarity):
            object.__setattr__(self, "polarity", Polarity(self.polarity))
        if not isinstance(self.metadata, Mapping):
            raise TypeError("metadata must be a mapping")
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))

    @property
    def semantic_key(self) -> tuple[str, str, str]:
        return (self.subject, self.relation, self.object)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.proposition_id,
            "subject": self.subject,
            "relation": self.relation,
            "object": self.object,
            "polarity": self.polarity.value,
            "context": self.context,
            "time": self.time,
            "source": self.source,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class PairJudgment:
    left_id: str
    right_id: str
    status: PairStatus
    reason_code: str
    explanation: str

    def to_dict(self) -> dict[str, str]:
        return {
            "left_id": self.left_id,
            "right_id": self.right_id,
            "status": self.status.value,
            "reason_code": self.reason_code,
            "explanation": self.explanation,
        }


@dataclass(frozen=True, slots=True)
class Assessment:
    status: AssessmentStatus
    proposition_count: int
    judgments: tuple[PairJudgment, ...]

    @property
    def contradictions(self) -> tuple[PairJudgment, ...]:
        return tuple(
            judgment
            for judgment in self.judgments
            if judgment.status is PairStatus.CONTRADICTION
        )

    @property
    def indeterminate_pairs(self) -> tuple[PairJudgment, ...]:
        return tuple(
            judgment
            for judgment in self.judgments
            if judgment.status is PairStatus.INDETERMINATE
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "proposition_count": self.proposition_count,
            "contradiction_count": len(self.contradictions),
            "indeterminate_count": len(self.indeterminate_pairs),
            "judgments": [judgment.to_dict() for judgment in self.judgments],
        }
