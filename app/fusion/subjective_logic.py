"""MuniAudit-AI — Subjective Logic Mathematical Operations.

Provides exact binomial Subjective Logic opinion representations and the Jøsang
Consensus Operator (⊕) for uncertainty-aware multi-source evidence fusion.
Adheres strictly to Locked Architecture v1.0 and Section 31 epistemic standards.
"""

from __future__ import annotations

import math

from pydantic import BaseModel, Field, field_validator


class SubjectiveOpinion(BaseModel):
    """Binomial Subjective Logic opinion representing belief, disbelief, uncertainty, and prior.

    Attributes:
        belief (b): Evidential mass supporting the target proposition (e.g. inconsistency / anomaly).
        disbelief (d): Evidential mass supporting the contrary proposition (e.g. compliance / coherence).
        uncertainty (u): Epistemic mass reflecting data missingness or sensor unreliability.
        base_rate (a): Prior probability / base rate in the absence of evidence (default 0.5).
    """

    belief: float = Field(..., ge=0.0, le=1.0, description="Belief mass supporting inconsistency")
    disbelief: float = Field(..., ge=0.0, le=1.0, description="Disbelief mass supporting compliance")
    uncertainty: float = Field(..., ge=0.0, le=1.0, description="Epistemic uncertainty mass")
    base_rate: float = Field(default=0.5, ge=0.0, le=1.0, description="Prior base rate probability")

    @field_validator("uncertainty")
    @classmethod
    def validate_sum_to_one(cls, v: float, info: object) -> float:
        """Validate that belief + disbelief + uncertainty == 1.0 within floating tolerance."""
        # Note: In Pydantic v2 field_validator, other fields may be in info.data
        return v

    def model_post_init(self, context: object, /) -> None:
        """Enforce strict normalization constraint: b + d + u == 1.0."""
        total = self.belief + self.disbelief + self.uncertainty
        if not math.isclose(total, 1.0, abs_tol=1e-4):
            msg = (
                f"Subjective opinion components must sum to 1.0; "
                f"got belief={self.belief:.4f}, disbelief={self.disbelief:.4f}, "
                f"uncertainty={self.uncertainty:.4f} (sum={total:.4f})"
            )
            raise ValueError(msg)

    @property
    def expected_value(self) -> float:
        """Projected probability expectation: E(ω) = b + a * u."""
        return self.belief + self.base_rate * self.uncertainty


def create_opinion(
    belief: float,
    disbelief: float,
    uncertainty: float,
    base_rate: float = 0.5,
) -> SubjectiveOpinion:
    """Safely construct and normalize a SubjectiveOpinion from raw masses."""
    # Ensure non-negative masses
    raw_b = max(0.0, float(belief))
    raw_d = max(0.0, float(disbelief))
    raw_u = max(0.0, float(uncertainty))

    total = raw_b + raw_d + raw_u
    if total > 0.0:
        b = raw_b / total
        d = raw_d / total
        u = raw_u / total
    else:
        # Default fallback to vacuous opinion if all masses are zero
        b, d, u = 0.0, 0.0, 1.0

    return SubjectiveOpinion(
        belief=round(b, 6),
        disbelief=round(d, 6),
        uncertainty=round(u, 6),
        base_rate=round(float(base_rate), 4),
    )


def vacuous_opinion(base_rate: float = 0.5) -> SubjectiveOpinion:
    """Return a completely uninformative / vacuous opinion (b=0, d=0, u=1).

    This serves as the neutral identity element under the Subjective Logic consensus operator:
    ω ⊕ vacuous = ω.
    """
    return SubjectiveOpinion(belief=0.0, disbelief=0.0, uncertainty=1.0, base_rate=base_rate)


def dogmatic_opinion(belief: float, base_rate: float = 0.5) -> SubjectiveOpinion:
    """Return a dogmatic opinion with zero uncertainty (u=0)."""
    b = max(0.0, min(1.0, float(belief)))
    d = 1.0 - b
    return SubjectiveOpinion(belief=round(b, 6), disbelief=round(d, 6), uncertainty=0.0, base_rate=base_rate)


def fuse_opinions(
    omega_a: SubjectiveOpinion,
    omega_b: SubjectiveOpinion,
    relative_weight_a: float = 0.5,
) -> SubjectiveOpinion:
    """Fuse two independent subjective opinions using the Jøsang Consensus Operator (⊕).

    Mathematical Formulation:
        κ = u_A + u_B - u_A * u_B
        If κ > 0:
            b_{A⊕B} = (b_A * u_B + b_B * u_A) / κ
            d_{A⊕B} = (d_A * u_B + d_B * u_A) / κ
            u_{A⊕B} = (u_A * u_B) / κ
        If κ == 0 (both opinions dogmatic, u_A == u_B == 0):
            Weighted average of beliefs using relative source weights.
    """
    u_a = omega_a.uncertainty
    u_b = omega_b.uncertainty

    kappa = u_a + u_b - (u_a * u_b)

    # Base rate consensus: harmonic / mean
    a_fused = (omega_a.base_rate + omega_b.base_rate) / 2.0

    if kappa > 1e-9:
        b_fused = (omega_a.belief * u_b + omega_b.belief * u_a) / kappa
        d_fused = (omega_a.disbelief * u_b + omega_b.disbelief * u_a) / kappa
        u_fused = (u_a * u_b) / kappa
        return create_opinion(b_fused, d_fused, u_fused, base_rate=a_fused)

    # Dogmatic case: u_a == 0 and u_b == 0
    w_a = max(0.0, min(1.0, relative_weight_a))
    w_b = 1.0 - w_a
    b_fused = w_a * omega_a.belief + w_b * omega_b.belief
    d_fused = w_a * omega_a.disbelief + w_b * omega_b.disbelief
    u_fused = 0.0
    return create_opinion(b_fused, d_fused, u_fused, base_rate=a_fused)


def fuse_multi_opinions(opinions: list[SubjectiveOpinion]) -> SubjectiveOpinion:
    """Iteratively fuse a collection of opinions using the commutative consensus operator.

    If the collection is empty, returns the vacuous opinion.
    """
    if not opinions:
        return vacuous_opinion()

    current = opinions[0]
    for nxt in opinions[1:]:
        current = fuse_opinions(current, nxt)
    return current
