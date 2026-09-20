"""Geospatial Transit Velocity Ceiling and Reachability Deterministic Rule."""

from datetime import datetime
from typing import Any

from app.domain.epistemic import AdministrativeState
from app.ingestion.gis_parser import haversine_meters
from app.rules.base import DeterministicRule, RuleEvaluationResult

DEFAULT_MAX_VELOCITY_KMH = 80.0
GPS_JITTER_TOLERANCE_METERS = 50.0


def _parse_timestamp(ts: datetime | str | None) -> datetime | None:
    """Parses datetime object or ISO-8601 string to a datetime."""
    if ts is None:
        return None
    if isinstance(ts, datetime):
        return ts
    try:
        # Replace space with T if needed
        clean_ts = ts.strip().replace(" ", "T")
        return datetime.fromisoformat(clean_ts)
    except (ValueError, TypeError):
        return None


class GeospatialTransitSpeedRule(DeterministicRule):
    """Validates physical transit reachability between successive GPS coordinates.

    Calculates great-circle WGS-84 geodesic distance and verifies that the apparent
    transit velocity does not exceed the legal municipal tipper speed ceiling (80 km/h).
    """

    rule_id: str = "R-002-GEOSPATIAL-SPEED"
    rule_name: str = "Geospatial Transit Velocity Ceiling Invariant"

    def __init__(self, max_velocity_kmh: float = DEFAULT_MAX_VELOCITY_KMH) -> None:
        self.max_velocity_kmh = max_velocity_kmh

    def evaluate(  # type: ignore[override]
        self,
        point_a: tuple[float, float] | None = None,
        point_b: tuple[float, float] | None = None,
        timestamp_a: datetime | str | None = None,
        timestamp_b: datetime | str | None = None,
        evidence_refs: list[str] | None = None,
        **kwargs: Any,
    ) -> RuleEvaluationResult:
        refs = evidence_refs or []

        # 1. Missing Coordinate or Timestamp Safe Failure
        t_a = _parse_timestamp(timestamp_a)
        t_b = _parse_timestamp(timestamp_b)

        if point_a is None or point_b is None or t_a is None or t_b is None:
            return RuleEvaluationResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status=AdministrativeState.INCONCLUSIVE_DATA,
                observed_value={
                    "point_a": point_a,
                    "point_b": point_b,
                    "timestamp_a": str(timestamp_a),
                    "timestamp_b": str(timestamp_b),
                },
                expected_value="Valid coordinates and timestamps required for both transit points",
                tolerance=self.max_velocity_kmh,
                evidence_refs=refs,
                justification=(
                    "Inconclusive data: GPS coordinates or timestamps are missing/unparseable. "
                    "Cannot compute transit velocity without complete temporal-spatial endpoints."
                ),
            )

        lat1, lon1 = point_a
        lat2, lon2 = point_b

        # Compute geodesic distance
        dist_meters = haversine_meters(lat1, lon1, lat2, lon2)
        dist_km = dist_meters / 1000.0

        elapsed_seconds = (t_b - t_a).total_seconds()

        # 2. Negative / Zero Elapsed Time Check
        if elapsed_seconds <= 0:
            if dist_meters > GPS_JITTER_TOLERANCE_METERS:
                return RuleEvaluationResult(
                    rule_id=self.rule_id,
                    rule_name=self.rule_name,
                    status=AdministrativeState.SUBSTANTIVE_INCONSISTENCY,
                    observed_value=f"{dist_km:.2f} km in {elapsed_seconds:.0f}s",
                    expected_value="Transit time must be positive (> 0s) for distinct locations",
                    discrepancy_delta=round(dist_km, 2),
                    evidence_refs=refs,
                    justification=(
                        f"Temporal impossibility: vehicle appeared at distant coordinates "
                        f"({dist_km:.2f} km apart) with non-positive elapsed time ({elapsed_seconds:.0f}s)."
                    ),
                )
            else:
                # Stationary vehicle within GPS noise
                return RuleEvaluationResult(
                    rule_id=self.rule_id,
                    rule_name=self.rule_name,
                    status=AdministrativeState.VERIFIED_COMPLIANT,
                    observed_value=0.0,
                    expected_value=f"<= {self.max_velocity_kmh} km/h",
                    discrepancy_delta=0.0,
                    tolerance=self.max_velocity_kmh,
                    evidence_refs=refs,
                    justification=(
                        f"Stationary location verified: points are within GPS jitter radius "
                        f"({dist_meters:.1f}m <= {GPS_JITTER_TOLERANCE_METERS}m)."
                    ),
                )

        # 3. Calculate Apparent Velocity
        elapsed_hours = elapsed_seconds / 3600.0
        apparent_velocity_kmh = round(dist_km / elapsed_hours, 2)

        if apparent_velocity_kmh <= self.max_velocity_kmh:
            return RuleEvaluationResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status=AdministrativeState.VERIFIED_COMPLIANT,
                observed_value=apparent_velocity_kmh,
                expected_value=f"<= {self.max_velocity_kmh} km/h",
                discrepancy_delta=0.0,
                tolerance=self.max_velocity_kmh,
                evidence_refs=refs,
                justification=(
                    f"Geospatial velocity verified: apparent speed {apparent_velocity_kmh:.2f} km/h "
                    f"over {dist_km:.2f} km in {elapsed_seconds / 60.0:.1f} mins is within the legal "
                    f"tipper speed ceiling ({self.max_velocity_kmh} km/h)."
                ),
            )
        else:
            delta = round(apparent_velocity_kmh - self.max_velocity_kmh, 2)
            return RuleEvaluationResult(
                rule_id=self.rule_id,
                rule_name=self.rule_name,
                status=AdministrativeState.SUBSTANTIVE_INCONSISTENCY,
                observed_value=apparent_velocity_kmh,
                expected_value=f"<= {self.max_velocity_kmh} km/h",
                discrepancy_delta=delta,
                tolerance=self.max_velocity_kmh,
                evidence_refs=refs,
                justification=(
                    f"Physical speed violation: apparent velocity {apparent_velocity_kmh:.2f} km/h "
                    f"over {dist_km:.2f} km in {elapsed_seconds / 60.0:.1f} mins exceeds the maximum "
                    f"legal tipper speed ceiling ({self.max_velocity_kmh} km/h by {delta} km/h)."
                ),
            )
