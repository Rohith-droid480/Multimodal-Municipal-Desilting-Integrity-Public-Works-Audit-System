"""Physical Silt Density & Tipper Capacity Deterministic Rule."""

from typing import Any

from app.domain.epistemic import AdministrativeState
from app.rules.base import DeterministicRule, RuleEvaluationResult

# Maximum theoretical wet desilted sludge saturation density (CPHEEO / MoHUA standards)
MAX_WET_SILT_DENSITY_T_M3 = 1.90  # 1,900 kg/m3


class PhysicalSiltDensityRule(DeterministicRule):
    """Reconciles reported tipper volume capacity and net desilted silt weight.

    Calculates apparent material density and validates that it does not exceed the
    maximum theoretical physical saturation limit of wet municipal silt (1.90 t/m³).
    """

    rule_id: str = "R-003-PHYSICAL-DENSITY"
    rule_name: str = "Physical Silt Density & Tipper Capacity Invariant"

    def __init__(self, max_density_t_m3: float = MAX_WET_SILT_DENSITY_T_M3) -> None:
        self.max_density_t_m3 = max_density_t_m3

    def evaluate(  # type: ignore[override]
        self,
        net_weight_kg: float | None = None,
        tipper_volume_m3: float | None = None,
        evidence_refs: list[str] | None = None,
        **kwargs: Any,
    ) -> RuleEvaluationResult:
        refs = evidence_refs or []

        # 1. Missing Data Safe Failure
        if net_weight_kg is None or tipper_volume_m3 is None:
            return RuleEvaluationResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status=AdministrativeState.INCONCLUSIVE_DATA,
                observed_value={
                    "net_weight_kg": net_weight_kg,
                    "tipper_volume_m3": tipper_volume_m3,
                },
                expected_value=f"Apparent density <= {self.max_density_t_m3} t/m³",
                tolerance=self.max_density_t_m3,
                evidence_refs=refs,
                justification=(
                    "Inconclusive data: Tipper volumetric capacity or net haul weight is not recorded. "
                    "Cannot compute material density without both parameters."
                ),
            )

        # 2. Non-positive Values Physical Violation
        if net_weight_kg <= 0.0 or tipper_volume_m3 <= 0.0:
            return RuleEvaluationResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status=AdministrativeState.SUBSTANTIVE_INCONSISTENCY,
                observed_value={
                    "net_weight_kg": net_weight_kg,
                    "tipper_volume_m3": tipper_volume_m3,
                },
                expected_value="Both net weight and volume must be strictly positive (> 0.0)",
                evidence_refs=refs,
                justification=(
                    f"Physical violation: non-positive physical parameter "
                    f"(Net Weight={net_weight_kg} kg, Volume={tipper_volume_m3} m³)."
                ),
            )

        # 3. Calculate Apparent Density (tonnes per cubic meter)
        net_weight_tonnes = net_weight_kg / 1000.0
        apparent_density_t_m3 = round(net_weight_tonnes / tipper_volume_m3, 3)

        if apparent_density_t_m3 <= self.max_density_t_m3:
            return RuleEvaluationResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status=AdministrativeState.VERIFIED_COMPLIANT,
                observed_value=apparent_density_t_m3,
                expected_value=f"<= {self.max_density_t_m3} t/m³",
                discrepancy_delta=0.0,
                tolerance=self.max_density_t_m3,
                evidence_refs=refs,
                justification=(
                    f"Physical material density verified: apparent density {apparent_density_t_m3:.3f} t/m³ "
                    f"({net_weight_tonnes:.2f} tonnes in {tipper_volume_m3:.1f} m³) is within the maximum "
                    f"saturation density for wet desilted silt ({self.max_density_t_m3} t/m³)."
                ),
            )
        else:
            delta = round(apparent_density_t_m3 - self.max_density_t_m3, 3)
            return RuleEvaluationResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status=AdministrativeState.SUBSTANTIVE_INCONSISTENCY,
                observed_value=apparent_density_t_m3,
                expected_value=f"<= {self.max_density_t_m3} t/m³",
                discrepancy_delta=delta,
                tolerance=self.max_density_t_m3,
                evidence_refs=refs,
                justification=(
                    f"Physical density violation: apparent density {apparent_density_t_m3:.3f} t/m³ "
                    f"({net_weight_tonnes:.2f} tonnes in {tipper_volume_m3:.1f} m³) exceeds the theoretical "
                    f"physical saturation limit for wet silt ({self.max_density_t_m3} t/m³ by {delta} t/m³). "
                    f"Reported mass cannot fit in the declared tipper volumetric capacity."
                ),
            )
