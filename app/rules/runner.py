"""Deterministic Rule Suite Orchestrator."""

import logging
from typing import Any

from app.domain.epistemic import AdministrativeState, EvidenceSourceType
from app.domain.models import Dossier
from app.rules.base import RuleEvaluationResult
from app.rules.geospatial_reach import GeospatialTransitSpeedRule
from app.rules.mass_balance import WeighbridgeMassBalanceRule
from app.rules.physical_capacity import PhysicalSiltDensityRule
from app.rules.temporal_sequence import TemporalSequenceRule

logger = logging.getLogger(__name__)


def evaluate_dossier_rules(dossier: Dossier) -> list[RuleEvaluationResult]:
    """Executes the full suite of civil engineering deterministic rules on a submitted dossier.

    Extracts operational measurements from evidence items and validates:
      1. Weighbridge Mass Balance (R-001)
      2. Geospatial Transit Velocity Ceiling (R-002)
      3. Physical Wet Silt Density Limit (R-003)
      4. Contractual & Operational Chronology (R-004)

    Resilience: An unhandled exception in any individual rule evaluates to TECHNICAL_ABSTENTION
    rather than halting overall dossier evaluation.
    """
    results: list[RuleEvaluationResult] = []

    mass_rule = WeighbridgeMassBalanceRule()
    speed_rule = GeospatialTransitSpeedRule()
    density_rule = PhysicalSiltDensityRule()
    temporal_rule = TemporalSequenceRule()

    # 1. Inspect Weighbridge Evidence
    wb_items = [
        item for item in dossier.evidence_items
        if item.source_type == EvidenceSourceType.WEIGHBRIDGE_RECEIPT
    ]

    if wb_items:
        for wb_item in wb_items:
            meta = wb_item.metadata or {}
            # Flatten potential ocr_extracted subdict
            raw_ocr = meta.get("ocr_extracted")
            ocr_meta: dict[str, Any] = raw_ocr if isinstance(raw_ocr, dict) else {}

            gross = meta.get("gross_weight_kg", ocr_meta.get("gross_weight_kg"))
            tare = meta.get("tare_weight_kg", ocr_meta.get("tare_weight_kg"))
            net = meta.get("net_weight_kg", ocr_meta.get("net_weight_kg"))
            vol = meta.get("tipper_volume_m3", ocr_meta.get("tipper_volume_m3"))

            # R-001: Mass Balance
            try:
                results.append(
                    mass_rule.evaluate(
                        gross_weight_kg=gross,
                        tare_weight_kg=tare,
                        net_weight_kg=net,
                        evidence_refs=[wb_item.sha256_digest],
                    )
                )
            except Exception as e:
                logger.exception("Error evaluating Mass Balance rule")
                results.append(
                    RuleEvaluationResult(
                        rule_id=mass_rule.rule_id,
                        rule_name=mass_rule.rule_name,
                        status=AdministrativeState.TECHNICAL_ABSTENTION,
                        evidence_refs=[wb_item.sha256_digest],
                        justification=f"Technical abstention: runtime evaluation error ({e}).",
                    )
                )

            # R-003: Physical Silt Density
            try:
                results.append(
                    density_rule.evaluate(
                        net_weight_kg=net,
                        tipper_volume_m3=vol,
                        evidence_refs=[wb_item.sha256_digest],
                    )
                )
            except Exception as e:
                logger.exception("Error evaluating Silt Density rule")
                results.append(
                    RuleEvaluationResult(
                        rule_id=density_rule.rule_id,
                        rule_name=density_rule.rule_name,
                        status=AdministrativeState.TECHNICAL_ABSTENTION,
                        evidence_refs=[wb_item.sha256_digest],
                        justification=f"Technical abstention: runtime evaluation error ({e}).",
                    )
                )
    else:
        # Evaluate missing weighbridge item safely
        results.append(
            mass_rule.evaluate(
                gross_weight_kg=None,
                tare_weight_kg=None,
                net_weight_kg=None,
            )
        )
        results.append(
            density_rule.evaluate(
                net_weight_kg=None,
                tipper_volume_m3=None,
            )
        )

    # 2. Inspect Geospatial & Transit Trip Logs
    trip_items = [
        item for item in dossier.evidence_items
        if item.source_type == EvidenceSourceType.TRIP_LOG
    ]

    evaluated_speed = False
    for trip_item in trip_items:
        meta = trip_item.metadata or {}
        pt_a = meta.get("start_point")
        pt_b = meta.get("end_point")
        ts_a = meta.get("start_time")
        ts_b = meta.get("end_time")

        if pt_a and pt_b:
            evaluated_speed = True
            try:
                results.append(
                    speed_rule.evaluate(
                        point_a=tuple(pt_a),
                        point_b=tuple(pt_b),
                        timestamp_a=ts_a,
                        timestamp_b=ts_b,
                        evidence_refs=[trip_item.sha256_digest],
                    )
                )
            except Exception as e:
                logger.exception("Error evaluating Geospatial Speed rule")
                results.append(
                    RuleEvaluationResult(
                        rule_id=speed_rule.rule_id,
                        rule_name=speed_rule.rule_name,
                        status=AdministrativeState.TECHNICAL_ABSTENTION,
                        evidence_refs=[trip_item.sha256_digest],
                        justification=f"Technical abstention: runtime evaluation error ({e}).",
                    )
                )

    if not evaluated_speed:
        results.append(
            speed_rule.evaluate(
                point_a=None,
                point_b=None,
                timestamp_a=None,
                timestamp_b=None,
            )
        )

    # 3. Inspect Temporal Sequence
    # Harvest milestone dates across dossier and metadata
    dossier_meta: dict[str, Any] = {}
    for item in dossier.evidence_items:
        if item.source_type == EvidenceSourceType.CONTRACT_METADATA and item.metadata:
            dossier_meta.update(item.metadata)

    contract_award = dossier_meta.get("contract_award_at")
    work_order_dt = dossier_meta.get("work_order_at")
    execution_dt = dossier_meta.get("work_execution_at")
    invoice_dt = dossier.finalized_at or dossier_meta.get("invoice_submitted_at")

    wb_dt = None
    if wb_items:
        wb_meta = wb_items[0].metadata or {}
        wb_dt = wb_meta.get("out_timestamp") or wb_meta.get("in_timestamp")

    all_evidence_refs = [item.sha256_digest for item in dossier.evidence_items]

    try:
        results.append(
            temporal_rule.evaluate(
                contract_award_at=contract_award,
                work_order_at=work_order_dt,
                work_execution_at=execution_dt,
                weighbridge_at=wb_dt,
                invoice_submitted_at=invoice_dt,
                evidence_refs=all_evidence_refs,
            )
        )
    except Exception as e:
        logger.exception("Error evaluating Temporal Sequence rule")
        results.append(
            RuleEvaluationResult(
                rule_id=temporal_rule.rule_id,
                rule_name=temporal_rule.rule_name,
                status=AdministrativeState.TECHNICAL_ABSTENTION,
                evidence_refs=all_evidence_refs,
                justification=f"Technical abstention: runtime evaluation error ({e}).",
            )
        )

    return results
