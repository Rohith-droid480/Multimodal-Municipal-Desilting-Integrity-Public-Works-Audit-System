"""Municipal GIS & KML/GeoJSON Drain Reach Parser with WGS-84 Chainage."""

import json
import math
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

# Default BBMP (Bruhat Bengaluru Mahanagara Palike) Geographic Bounding Box
BBMP_BOUNDS = {
    "min_lat": 12.80,
    "max_lat": 13.15,
    "min_lng": 77.45,
    "max_lng": 77.75,
}


def haversine_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates the great-circle distance between two points on the WGS-84 ellipsoid in meters."""
    r_earth = 6371000.0  # Mean radius of Earth in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return r_earth * c


class ParsedDrainReach(BaseModel):
    """Normalized municipal drain reach segment with stationing and coordinate chainage."""

    drain_reach_id: str
    tenant_id: str = "WARD-09-CENTRAL"
    name: str
    start_point_lat: float
    start_point_lng: float
    end_point_lat: float
    end_point_lng: float
    length_meters: float
    coordinates: list[tuple[float, float]] = Field(
        default_factory=list, description="List of (lat, lng) points along reach"
    )
    is_within_bounds: bool = True
    validation_warnings: list[str] = Field(default_factory=list)


@dataclass
class ParseResult:
    reaches: list[ParsedDrainReach] = field(default_factory=list)
    has_errors: bool = False
    error_message: str | None = None
    is_inconclusive: bool = False


class MunicipalGISParser:
    """Parses municipal storm-water-drain reach alignments from KML and GeoJSON."""

    def __init__(self, bounding_box: dict[str, float] | None = None) -> None:
        self.bounds = bounding_box or BBMP_BOUNDS

    def validate_coordinate_bounds(self, lat: float, lng: float) -> bool:
        """Checks if a point falls within municipal operational jurisdiction."""
        return (
            self.bounds["min_lat"] <= lat <= self.bounds["max_lat"]
            and self.bounds["min_lng"] <= lng <= self.bounds["max_lng"]
        )

    def compute_chainage(self, coords: list[tuple[float, float]]) -> float:
        """Computes total cumulative reach distance in meters along coordinate nodes."""
        if len(coords) < 2:
            return 0.0
        total_dist = 0.0
        for i in range(len(coords) - 1):
            total_dist += haversine_meters(
                coords[i][0], coords[i][1], coords[i + 1][0], coords[i + 1][1]
            )
        return round(total_dist, 2)

    def parse_geojson(self, file_path_or_content: dict[str, Any] | str | Path) -> ParseResult:
        """Parses GeoJSON Features into ParsedDrainReach objects."""
        try:
            if isinstance(file_path_or_content, dict):
                data = file_path_or_content
            elif isinstance(file_path_or_content, Path) or (
                isinstance(file_path_or_content, str) and Path(file_path_or_content).exists()
            ):
                content = Path(file_path_or_content).read_text(encoding="utf-8")
                data = json.loads(content)
            else:
                data = json.loads(str(file_path_or_content))
        except (json.JSONDecodeError, ValueError, TypeError, OSError, KeyError) as e:
            return ParseResult(
                has_errors=True,
                error_message=f"Malformed GeoJSON payload: {e}",
                is_inconclusive=True,
            )

        features = data.get("features", [])
        if not features and data.get("type") == "Feature":
            features = [data]

        reaches: list[ParsedDrainReach] = []
        for idx, feat in enumerate(features):
            geom = feat.get("geometry", {})
            props = feat.get("properties", {})
            reach_id = str(props.get("reach_id") or props.get("id") or f"REACH-{idx+1:04d}")
            name = str(props.get("name") or props.get("reach_name") or f"Drain Reach {idx+1}")
            tenant_id = str(props.get("tenant_id") or "WARD-09-CENTRAL")

            geom_type = geom.get("type")
            coords_raw = geom.get("coordinates", [])

            # Normalize to list of (lat, lng)
            coords: list[tuple[float, float]] = []
            if geom_type == "LineString":
                # GeoJSON coordinates are [lng, lat, (elev)]
                coords = [(float(c[1]), float(c[0])) for c in coords_raw if len(c) >= 2]
            elif geom_type == "MultiLineString":
                # Flatten first line or combine
                for line in coords_raw:
                    coords.extend([(float(c[1]), float(c[0])) for c in line if len(c) >= 2])

            if len(coords) < 2:
                reaches.append(
                    ParsedDrainReach(
                        drain_reach_id=reach_id,
                        tenant_id=tenant_id,
                        name=name,
                        start_point_lat=coords[0][0] if coords else 0.0,
                        start_point_lng=coords[0][1] if coords else 0.0,
                        end_point_lat=coords[-1][0] if coords else 0.0,
                        end_point_lng=coords[-1][1] if coords else 0.0,
                        length_meters=0.0,
                        coordinates=coords,
                        is_within_bounds=False,
                        validation_warnings=["Insufficient nodes to form a continuous reach alignment"],
                    )
                )
                continue

            length_m = self.compute_chainage(coords)
            all_in_bounds = all(self.validate_coordinate_bounds(lat, lng) for lat, lng in coords)

            warnings: list[str] = []
            if not all_in_bounds:
                warnings.append(
                    f"Coordinates outside municipal boundary [{self.bounds['min_lat']}, {self.bounds['max_lat']}]."
                )

            reach = ParsedDrainReach(
                drain_reach_id=reach_id,
                tenant_id=tenant_id,
                name=name,
                start_point_lat=coords[0][0],
                start_point_lng=coords[0][1],
                end_point_lat=coords[-1][0],
                end_point_lng=coords[-1][1],
                length_meters=length_m,
                coordinates=coords,
                is_within_bounds=all_in_bounds,
                validation_warnings=warnings,
            )
            reaches.append(reach)

        return ParseResult(reaches=reaches, has_errors=False)

    def parse_kml(self, file_path_or_content: str | Path) -> ParseResult:
        """Parses KML XML documents into ParsedDrainReach objects with safe failover."""
        try:
            if isinstance(file_path_or_content, Path) or (
                isinstance(file_path_or_content, str) and Path(file_path_or_content).exists()
            ):
                content = Path(file_path_or_content).read_text(encoding="utf-8")
            else:
                content = str(file_path_or_content)

            root = ET.fromstring(content)
        except (ET.ParseError, ValueError, TypeError, OSError, KeyError) as e:
            return ParseResult(
                has_errors=True,
                error_message=f"Malformed KML XML payload: {e}",
                is_inconclusive=True,
            )

        # XML namespace agnostic findall
        reaches: list[ParsedDrainReach] = []
        placemarks = root.findall(".//{*}Placemark")
        if not placemarks:
            placemarks = root.findall(".//Placemark")

        for idx, pm in enumerate(placemarks):
            name_elem = pm.find("{*}name")
            if name_elem is None:
                name_elem = pm.find("name")
            name = name_elem.text.strip() if name_elem is not None and name_elem.text else f"KML Reach {idx+1}"
            reach_id = f"KML-REACH-{idx+1:04d}"

            # Extract coordinates from LineString or Polygon
            coord_elem = pm.find(".//{*}coordinates")
            if coord_elem is None:
                coord_elem = pm.find(".//coordinates")

            if coord_elem is None or not coord_elem.text:
                reaches.append(
                    ParsedDrainReach(
                        drain_reach_id=reach_id,
                        name=name,
                        start_point_lat=0.0,
                        start_point_lng=0.0,
                        end_point_lat=0.0,
                        end_point_lng=0.0,
                        length_meters=0.0,
                        is_within_bounds=False,
                        validation_warnings=["KML Placemark contains no geometry coordinates"],
                    )
                )
                continue

            raw_str = coord_elem.text.strip()
            coords: list[tuple[float, float]] = []
            for token in raw_str.split():
                parts = token.split(",")
                if len(parts) >= 2:
                    try:
                        lng = float(parts[0])
                        lat = float(parts[1])
                        coords.append((lat, lng))
                    except ValueError:
                        continue

            if len(coords) < 2:
                reaches.append(
                    ParsedDrainReach(
                        drain_reach_id=reach_id,
                        name=name,
                        start_point_lat=coords[0][0] if coords else 0.0,
                        start_point_lng=coords[0][1] if coords else 0.0,
                        end_point_lat=coords[-1][0] if coords else 0.0,
                        end_point_lng=coords[-1][1] if coords else 0.0,
                        length_meters=0.0,
                        coordinates=coords,
                        is_within_bounds=False,
                        validation_warnings=["KML contains fewer than 2 valid coordinate nodes"],
                    )
                )
                continue

            length_m = self.compute_chainage(coords)
            all_in_bounds = all(self.validate_coordinate_bounds(lat, lng) for lat, lng in coords)

            warnings = []
            if not all_in_bounds:
                warnings.append("KML coordinates outside municipal operational boundary")

            reaches.append(
                ParsedDrainReach(
                    drain_reach_id=reach_id,
                    name=name,
                    start_point_lat=coords[0][0],
                    start_point_lng=coords[0][1],
                    end_point_lat=coords[-1][0],
                    end_point_lng=coords[-1][1],
                    length_meters=length_m,
                    coordinates=coords,
                    is_within_bounds=all_in_bounds,
                    validation_warnings=warnings,
                )
            )

        return ParseResult(reaches=reaches, has_errors=False)
