"""Comprehensive Unit and Invariant Tests for Deterministic Civil Engineering Rules."""

from datetime import UTC, datetime, timedelta

from app.domain.epistemic import AdministrativeState, EpistemicCategory
from app.domain.models import Dossier
from app.ingestion.benchmark_loader import BenchmarkDossierLoader, BenchmarkDossierType
from app.rules.geospatial_reach import GeospatialTransitSpeedRule
from app.rules.mass_balance import WeighbridgeMassBalanceRule
from app.rules.physical_capacity import PhysicalSiltDensityRule
from app.rules.runner import evaluate_dossier_rules
from app.rules.temporal_sequence import TemporalSequenceRule
from app.storage.interface import LocalStorageAdapter

# ==============================================================================
# R-001: Weighbridge Mass Balance Rule Tests
# ==============================================================================

def test_mass_balance_nominal_compliant() -> None:
    rule = WeighbridgeMassBalanceRule()
    res = rule.evaluate(
        gross_weight_kg=24500.0,
        tare_weight_kg=8200.0,
        net_weight_kg=16300.0,
    )
    assert res.status == AdministrativeState.VERIFIED_COMPLIANT
    assert res.discrepancy_delta == 0.0
    assert res.epistemic_category == EpistemicCategory.RULE_RESULT


def test_mass_balance_boundary_within_tolerance() -> None:
    rule = WeighbridgeMassBalanceRule(tolerance_kg=20.0)
    # Expected net: 16,300 kg. Observed: 16,319.5 kg (drift: 19.5 kg <= 20.0 kg)
    res = rule.evaluate(
        gross_weight_kg=24500.0,
        tare_weight_kg=8200.0,
        net_weight_kg=16319.5,
    )
    assert res.status == AdministrativeState.VERIFIED_COMPLIANT
    assert res.discrepancy_delta == 19.5


def test_mass_balance_boundary_exceeds_tolerance() -> None:
    rule = WeighbridgeMassBalanceRule(tolerance_kg=20.0)
    # Expected net: 16,300 kg. Observed: 16,321.0 kg (drift: 21.0 kg > 20.0 kg)
    res = rule.evaluate(
        gross_weight_kg=24500.0,
        tare_weight_kg=8200.0,
        net_weight_kg=16321.0,
    )
    assert res.status == AdministrativeState.SUBSTANTIVE_INCONSISTENCY
    assert res.discrepancy_delta == 21.0


def test_mass_balance_tare_exceeds_gross() -> None:
    rule = WeighbridgeMassBalanceRule()
    # Gross 8000 kg <= Tare 8500 kg
    res = rule.evaluate(
        gross_weight_kg=8000.0,
        tare_weight_kg=8500.0,
        net_weight_kg=1000.0,
    )
    assert res.status == AdministrativeState.SUBSTANTIVE_INCONSISTENCY
    assert "tare violation" in res.justification.lower()


def test_mass_balance_missing_data_inconclusive() -> None:
    rule = WeighbridgeMassBalanceRule()
    # Missing Gross weight
    res = rule.evaluate(
        gross_weight_kg=None,
        tare_weight_kg=8200.0,
        net_weight_kg=16300.0,
    )
    assert res.status == AdministrativeState.INCONCLUSIVE_DATA
    # Safety Invariant: missing data is never an adverse finding
    assert res.status != AdministrativeState.SUBSTANTIVE_INCONSISTENCY


# ==============================================================================
# R-002: Geospatial Transit Velocity Rule Tests
# ==============================================================================

def test_geospatial_speed_compliant() -> None:
    rule = GeospatialTransitSpeedRule(max_velocity_kmh=80.0)
    # 2 Bengaluru points ~11.1 km apart along North-South corridor
    pt_a = (12.9500, 77.6000)
    pt_b = (13.0500, 77.6000)  # ~11.1 km difference
    t_a = datetime(2026, 9, 20, 10, 0, 0, tzinfo=UTC)
    t_b = datetime(2026, 9, 20, 10, 20, 0, tzinfo=UTC)  # 20 minutes (apparent speed ~33.3 km/h)

    res = rule.evaluate(point_a=pt_a, point_b=pt_b, timestamp_a=t_a, timestamp_b=t_b)
    assert res.status == AdministrativeState.VERIFIED_COMPLIANT
    assert res.observed_value is not None
    assert float(res.observed_value) <= 80.0


def test_geospatial_speed_exceeds_ceiling() -> None:
    rule = GeospatialTransitSpeedRule(max_velocity_kmh=80.0)
    pt_a = (12.9000, 77.5000)
    pt_b = (13.2000, 77.7000)  # ~39 km difference
    t_a = datetime(2026, 9, 20, 10, 0, 0, tzinfo=UTC)
    t_b = datetime(2026, 9, 20, 10, 10, 0, tzinfo=UTC)  # 10 minutes -> ~234 km/h

    res = rule.evaluate(point_a=pt_a, point_b=pt_b, timestamp_a=t_a, timestamp_b=t_b)
    assert res.status == AdministrativeState.SUBSTANTIVE_INCONSISTENCY
    assert float(res.observed_value) > 80.0


def test_geospatial_speed_negative_time_travel() -> None:
    rule = GeospatialTransitSpeedRule()
    pt_a = (12.9500, 77.6000)
    pt_b = (13.0500, 77.6000)
    t_a = datetime(2026, 9, 20, 10, 30, 0, tzinfo=UTC)
    t_b = datetime(2026, 9, 20, 10, 15, 0, tzinfo=UTC)  # Arrived before departing

    res = rule.evaluate(point_a=pt_a, point_b=pt_b, timestamp_a=t_a, timestamp_b=t_b)
    assert res.status == AdministrativeState.SUBSTANTIVE_INCONSISTENCY
    assert "impossibility" in res.justification.lower()


def test_geospatial_missing_coords_inconclusive() -> None:
    rule = GeospatialTransitSpeedRule()
    res = rule.evaluate(
        point_a=(12.95, 77.60),
        point_b=None,
        timestamp_a=datetime.now(UTC),
        timestamp_b=None,
    )
    assert res.status == AdministrativeState.INCONCLUSIVE_DATA


# ==============================================================================
# R-003: Physical Silt Density & Tipper Capacity Tests
# ==============================================================================

def test_physical_density_compliant() -> None:
    rule = PhysicalSiltDensityRule(max_density_t_m3=1.90)
    # 16,500 kg (16.5 tonnes) in 10 m³ tipper -> density 1.65 t/m³ <= 1.90 t/m³
    res = rule.evaluate(net_weight_kg=16500.0, tipper_volume_m3=10.0)
    assert res.status == AdministrativeState.VERIFIED_COMPLIANT
    assert res.observed_value == 1.65


def test_physical_density_exceeds_limit() -> None:
    rule = PhysicalSiltDensityRule(max_density_t_m3=1.90)
    # 22,000 kg (22.0 tonnes) in 10 m³ tipper -> density 2.20 t/m³ > 1.90 t/m³
    res = rule.evaluate(net_weight_kg=22000.0, tipper_volume_m3=10.0)
    assert res.status == AdministrativeState.SUBSTANTIVE_INCONSISTENCY
    assert res.observed_value == 2.20
    assert res.discrepancy_delta == 0.30


def test_physical_density_missing_volume_inconclusive() -> None:
    rule = PhysicalSiltDensityRule()
    res = rule.evaluate(net_weight_kg=16500.0, tipper_volume_m3=None)
    assert res.status == AdministrativeState.INCONCLUSIVE_DATA


# ==============================================================================
# R-004: Temporal Sequence Rule Tests
# ==============================================================================

def test_temporal_sequence_compliant() -> None:
    rule = TemporalSequenceRule()
    base_time = datetime(2026, 8, 1, 10, 0, 0, tzinfo=UTC)
    res = rule.evaluate(
        contract_award_at=base_time,
        work_order_at=base_time + timedelta(days=5),
        work_execution_at=base_time + timedelta(days=10),
        weighbridge_at=base_time + timedelta(days=12),
        invoice_submitted_at=base_time + timedelta(days=15),
    )
    assert res.status == AdministrativeState.VERIFIED_COMPLIANT


def test_temporal_sequence_inversion() -> None:
    rule = TemporalSequenceRule()
    base_time = datetime(2026, 8, 1, 10, 0, 0, tzinfo=UTC)
    # Weighbridge date predates Work Order issuance date!
    res = rule.evaluate(
        contract_award_at=base_time,
        work_order_at=base_time + timedelta(days=10),
        work_execution_at=base_time + timedelta(days=12),
        weighbridge_at=base_time + timedelta(days=5),  # Inversion!
        invoice_submitted_at=base_time + timedelta(days=15),
    )
    assert res.status == AdministrativeState.SUBSTANTIVE_INCONSISTENCY
    assert "chronological sequence violation" in res.justification.lower()


def test_temporal_sequence_insufficient_timestamps_inconclusive() -> None:
    rule = TemporalSequenceRule()
    res = rule.evaluate(
        contract_award_at=datetime(2026, 8, 1, tzinfo=UTC),
        work_order_at=None,
        work_execution_at=None,
        weighbridge_at=None,
        invoice_submitted_at=None,
    )
    assert res.status == AdministrativeState.INCONCLUSIVE_DATA


# ==============================================================================
# Rule Runner Suite Orchestrator Tests
# ==============================================================================

def test_rule_runner_on_benchmark_clean_dossier(tmp_path) -> None:
    storage = LocalStorageAdapter(base_path=tmp_path)
    loader = BenchmarkDossierLoader(storage_adapter=storage)
    clean_dossier = loader.build_benchmark_dossier(BenchmarkDossierType.CLEAN_COMPLIANT)

    results = evaluate_dossier_rules(clean_dossier)
    assert len(results) >= 3

    # All evaluations should have EpistemicCategory.RULE_RESULT
    for r in results:
        assert r.epistemic_category == EpistemicCategory.RULE_RESULT

    # Mass balance on clean dossier must be VERIFIED_COMPLIANT
    mb_res = next(r for r in results if r.rule_id == "R-001-MASS-BALANCE")
    assert mb_res.status == AdministrativeState.VERIFIED_COMPLIANT


def test_rule_runner_on_inconsistent_dossier(tmp_path) -> None:
    storage = LocalStorageAdapter(base_path=tmp_path)
    loader = BenchmarkDossierLoader(storage_adapter=storage)
    inconsistent_dossier = loader.build_benchmark_dossier(BenchmarkDossierType.SUBSTANTIVE_INCONSISTENCY)

    results = evaluate_dossier_rules(inconsistent_dossier)
    assert len(results) >= 3

    # Density on impossible haul weight dossier must be SUBSTANTIVE_INCONSISTENCY
    density_res = next(r for r in results if r.rule_id == "R-003-PHYSICAL-DENSITY")
    assert density_res.status == AdministrativeState.SUBSTANTIVE_INCONSISTENCY
    assert density_res.observed_value == 4.65  # 46.5 tonnes in 10 m3 tipper


def test_rule_runner_empty_dossier_safe_failure() -> None:
    empty_dossier = Dossier(
        work_order_id="WO-EMPTY-01",
        contractor_id="CONT-EMPTY-01",
    )
    results = evaluate_dossier_rules(empty_dossier)
    assert len(results) >= 3

    # When evidence is absent, all rules must evaluate to INCONCLUSIVE_DATA
    for r in results:
        assert r.status == AdministrativeState.INCONCLUSIVE_DATA
        # Never an adverse finding on absent evidence
        assert r.status != AdministrativeState.SUBSTANTIVE_INCONSISTENCY
