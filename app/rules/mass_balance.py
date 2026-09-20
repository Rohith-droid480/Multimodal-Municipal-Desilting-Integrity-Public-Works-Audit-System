"""Weighbridge Mass Balance Deterministic Rule."""

from typing import Any

from app.domain.epistemic import AdministrativeState
from app.rules.base import DeterministicRule, RuleEvaluationResult

DEFAULT_MASS_TOLERANCE_KG = 20.0


class WeighbridgeMassBalanceRule(DeterministicRule):
    """Evaluates the arithmetic identity Gross - Tare = Net within scale calibration tolerance."""

    rule_id: str = "R-001-MASS-BALANCE"
    rule_name: str = "Weighbridge Mass Balance Invariant"

    def __init__(self, tolerance_kg: float = DEFAULT_MASS_TOLERANCE_KG) -> None:
        self.tolerance_kg = tolerance_kg

    def evaluate(  # type: ignore[override]
        self,
        gross_weight_kg: float | None = None,
        tare_weight_kg: float | None = None,
        net_weight_kg: float | None = None,
        evidence_refs: list[str] | None = None,
        **kwargs: Any,
    ) -> RuleEvaluationResult:
        refs = evidence_refs or []

        # 1. Missing Data Safe Failure
        if gross_weight_kg is None or tare_weight_kg is None or net_weight_kg is None:
            return RuleEvaluationResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status=AdministrativeState.INCONCLUSIVE_DATA,
                observed_value={
                    "gross_kg": gross_weight_kg,
                    "tare_kg": tare_weight_kg,
                    "net_kg": net_weight_kg,
                },
                expected_value="Gross, Tare, and Net weights must all be recorded",
                tolerance=self.tolerance_kg,
                evidence_refs=refs,
                justification=(
                    f"Inconclusive data: required weight measurement is missing "
                    f"(Gross={gross_weight_kg}, Tare={tare_weight_kg}, Net={net_weight_kg}). "
                    f"Missing data cannot establish an adverse finding."
                ),
            )

        # 2. Non-positive Weights Physical Violation
        if gross_weight_kg <= 0.0 or tare_weight_kg <= 0.0 or net_weight_kg <= 0.0:
            return RuleEvaluationResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status=AdministrativeState.SUBSTANTIVE_INCONSISTENCY,
                observed_value={
                    "gross_kg": gross_weight_kg,
                    "tare_kg": tare_weight_kg,
                    "net_kg": net_weight_kg,
                },
                expected_value="All weight values must be strictly positive (> 0.0 kg)",
                evidence_refs=refs,
                justification=(
                    f"Physical violation: non-positive weight recorded on weighbridge slip "
                    f"(Gross={gross_weight_kg}, Tare={tare_weight_kg}, Net={net_weight_kg})."
                ),
            )

        # 3. Physical Tare Violation: Gross <= Tare
        if gross_weight_kg <= tare_weight_kg:
            return RuleEvaluationResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status=AdministrativeState.SUBSTANTIVE_INCONSISTENCY,
                observed_value={
                    "gross_kg": gross_weight_kg,
                    "tare_kg": tare_weight_kg,
                },
                expected_value="Gross weight must be strictly greater than tare weight",
                discrepancy_delta=round(tare_weight_kg - gross_weight_kg, 2),
                evidence_refs=refs,
                justification=(
                    f"Physical tare violation: Gross weight ({gross_weight_kg:,.1f} kg) does not exceed "
                    f"tare weight ({tare_weight_kg:,.1f} kg). Loaded truck cannot weigh less than empty truck."
                ),
            )

        # 4. Arithmetic Identity Balance Check
        expected_net = gross_weight_kg - tare_weight_kg
        delta = round(abs(expected_net - net_weight_kg), 2)

        if delta <= self.tolerance_kg:
            return RuleEvaluationResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status=AdministrativeState.VERIFIED_COMPLIANT,
                observed_value=net_weight_kg,
                expected_value=expected_net,
                discrepancy_delta=delta,
                tolerance=self.tolerance_kg,
                evidence_refs=refs,
                justification=(
                    f"Mass balance verified: Gross ({gross_weight_kg:,.1f} kg) - "
                    f"Tare ({tare_weight_kg:,.1f} kg) = Expected Net ({expected_net:,.1f} kg). "
                    f"Claimed Net is {net_weight_kg:,.1f} kg (drift delta: {delta} kg <= tolerance {self.tolerance_kg} kg)."
                ),
            )
        else:
            return RuleEvaluationResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status=AdministrativeState.SUBSTANTIVE_INCONSISTENCY,
                observed_value=net_weight_kg,
                expected_value=expected_net,
                discrepancy_delta=delta,
                tolerance=self.tolerance_kg,
                evidence_refs=refs,
                justification=(
                    f"Mass balance discrepancy: Gross ({gross_weight_kg:,.1f} kg) - "
                    f"Tare ({tare_weight_kg:,.1f} kg) = Expected Net ({expected_net:,.1f} kg), "
                    f"but claimed Net is {net_weight_kg:,.1f} kg. Discrepancy delta ({delta} kg) "
                    f"exceeds scale tolerance ({self.tolerance_kg} kg)."
                ),
            )
