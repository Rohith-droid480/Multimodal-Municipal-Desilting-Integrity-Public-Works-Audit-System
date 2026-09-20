"""Deterministic Civil Engineering Rules Base Interface and Evaluation Contracts."""

from abc import ABC, abstractmethod
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

from app.domain.epistemic import AdministrativeState, EpistemicCategory


def utc_now() -> datetime:
    """Returns a timezone-aware current UTC datetime."""
    return datetime.now(UTC)


class RuleEvaluationResult(BaseModel):
    """Immutable result schema for deterministic rule adjudication.

    Epistemic Invariant: Always strictly categorized as RULE_RESULT.
    Missing data must evaluate to INCONCLUSIVE_DATA, never SUBSTANTIVE_INCONSISTENCY.
    """

    rule_id: str = Field(..., description="Standardized rule code (e.g. R-001-MASS-BALANCE)")
    rule_name: str = Field(..., description="Human-readable title of the civil engineering rule")
    epistemic_category: EpistemicCategory = Field(
        default=EpistemicCategory.RULE_RESULT,
        description="Strict epistemic classification (always RULE_RESULT)",
    )
    status: AdministrativeState = Field(
        ...,
        description="Administrative determination resulting from rule evaluation",
    )
    observed_value: Any = Field(default=None, description="Direct measurement or calculated value")
    expected_value: Any = Field(default=None, description="Contractual or physical expected value")
    discrepancy_delta: float | None = Field(
        default=None, description="Magnitude of violation/difference from expected value"
    )
    tolerance: float | None = Field(default=None, description="Configured tolerance threshold")
    evidence_refs: list[str] = Field(
        default_factory=list, description="SHA-256 hashes of supporting evidence items"
    )
    justification: str = Field(..., description="Detailed, explainable engineering rationale")
    evaluated_at: datetime = Field(default_factory=utc_now)


class DeterministicRule(ABC):
    """Abstract base class for all deterministic civil engineering rules."""

    rule_id: str
    rule_name: str

    @abstractmethod
    def evaluate(self, **kwargs: Any) -> RuleEvaluationResult:
        """Evaluates the rule against the provided domain context."""
