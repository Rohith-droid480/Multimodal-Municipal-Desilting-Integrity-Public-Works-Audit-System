from datetime import UTC, datetime
from typing import Any

from app.domain.epistemic import AdministrativeState
from app.rules.base import DeterministicRule, RuleEvaluationResult


def _parse_ts(val: datetime | str | None) -> datetime | None:
    """Safely converts an ISO string or datetime to timezone-aware UTC datetime."""
    if val is None:
        return None
    dt: datetime
    if isinstance(val, datetime):
        dt = val
    else:
        try:
            clean = val.strip().replace(" ", "T")
            dt = datetime.fromisoformat(clean)
        except (ValueError, TypeError):
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    else:
        dt = dt.astimezone(UTC)
    return dt


class TemporalSequenceRule(DeterministicRule):
    """Validates monotonic chronological progression across municipal project lifecycle.

    Enforces causal order:
      Contract Award <= Work Order Issuance <= Work Execution <= Weighbridge Dispatch <= Invoice Submission.
    """

    rule_id: str = "R-004-TEMPORAL-SEQUENCE"
    rule_name: str = "Contractual & Operational Chronology Invariant"

    def evaluate(  # type: ignore[override]
        self,
        contract_award_at: datetime | str | None = None,
        work_order_at: datetime | str | None = None,
        work_execution_at: datetime | str | None = None,
        weighbridge_at: datetime | str | None = None,
        invoice_submitted_at: datetime | str | None = None,
        evidence_refs: list[str] | None = None,
        **kwargs: Any,
    ) -> RuleEvaluationResult:
        refs = evidence_refs or []

        # Sequence definition
        stages = [
            ("Contract Award", _parse_ts(contract_award_at)),
            ("Work Order", _parse_ts(work_order_at)),
            ("Work Execution", _parse_ts(work_execution_at)),
            ("Weighbridge Dispatch", _parse_ts(weighbridge_at)),
            ("Invoice Submission", _parse_ts(invoice_submitted_at)),
        ]

        # Filter present timestamps
        present_stages = [(name, ts) for name, ts in stages if ts is not None]

        if len(present_stages) < 2:
            return RuleEvaluationResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status=AdministrativeState.INCONCLUSIVE_DATA,
                observed_value={name: str(ts) for name, ts in present_stages},
                expected_value="At least two sequential lifecycle timestamps required to evaluate chronology",
                evidence_refs=refs,
                justification=(
                    f"Inconclusive data: only {len(present_stages)} lifecycle timestamp(s) available. "
                    "Cannot verify chronological ordering without multiple verifiable milestone dates."
                ),
            )

        # Check pairwise monotonicity
        for i in range(len(present_stages) - 1):
            name_prev, ts_prev = present_stages[i]
            name_curr, ts_curr = present_stages[i + 1]

            if ts_curr < ts_prev:
                delta_hours = round((ts_prev - ts_curr).total_seconds() / 3600.0, 2)
                return RuleEvaluationResult(
                    rule_id=self.rule_id,
                    rule_name=self.rule_name,
                    status=AdministrativeState.SUBSTANTIVE_INCONSISTENCY,
                    observed_value=f"{name_curr} ({ts_curr.isoformat()}) preceded {name_prev} ({ts_prev.isoformat()})",
                    expected_value=f"{name_prev} must precede or equal {name_curr}",
                    discrepancy_delta=delta_hours,
                    evidence_refs=refs,
                    justification=(
                        f"Chronological sequence violation: '{name_curr}' ({ts_curr.strftime('%Y-%m-%d %H:%M:%S')}) "
                        f"occurred {delta_hours:.2f} hours before predecessor milestone '{name_prev}' "
                        f"({ts_prev.strftime('%Y-%m-%d %H:%M:%S')}). Event cannot occur before its causal prerequisite."
                    ),
                )

        # Monotonically consistent
        summary = " <= ".join([f"{name} ({ts.strftime('%Y-%m-%d')})" for name, ts in present_stages])
        return RuleEvaluationResult(
            rule_id=self.rule_id,
            rule_name=self.rule_name,
            status=AdministrativeState.VERIFIED_COMPLIANT,
            observed_value=summary,
            expected_value="Monotonically non-decreasing lifecycle sequence",
            discrepancy_delta=0.0,
            evidence_refs=refs,
            justification=f"Chronological sequence verified: {summary}.",
        )
