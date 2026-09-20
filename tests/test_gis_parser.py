"""Unit tests for Municipal GIS & KML/GeoJSON Reach Parser."""

from app.ingestion.gis_parser import MunicipalGISParser, haversine_meters


def test_haversine_meters():
    # Bengaluru Vidhana Soudha (12.9797, 77.5907) to MG Road Metro (12.9756, 77.6068)
    dist = haversine_meters(12.9797, 77.5907, 12.9756, 77.6068)
    # Approx 1.8 km
    assert 1700.0 < dist < 1950.0


def test_parse_geojson_valid():
    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "reach_id": "REACH-KORAMANGALA-01",
                    "name": "Koramangala Valley Drain Reach 1",
                    "tenant_id": "WARD-09-CENTRAL",
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [77.6150, 12.9300],
                        [77.6200, 12.9350],
                        [77.6250, 12.9400],
                    ],
                },
            }
        ],
    }

    parser = MunicipalGISParser()
    result = parser.parse_geojson(geojson_data)

    assert result.has_errors is False
    assert len(result.reaches) == 1
    reach = result.reaches[0]
    assert reach.drain_reach_id == "REACH-KORAMANGALA-01"
    assert reach.length_meters > 1000.0
    assert reach.is_within_bounds is True
    assert len(reach.validation_warnings) == 0


def test_parse_geojson_out_of_bounds():
    geojson_data = {
        "type": "Feature",
        "properties": {"name": "Delhi Drain in Wrong Jurisdiction"},
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [77.2090, 28.6139],
                [77.2100, 28.6150],
            ],
        },
    }
    parser = MunicipalGISParser()
    result = parser.parse_geojson(geojson_data)

    assert result.has_errors is False
    assert len(result.reaches) == 1
    reach = result.reaches[0]
    assert reach.is_within_bounds is False
    assert any("outside municipal boundary" in w for w in reach.validation_warnings)


def test_parse_kml_valid():
    kml_data = """<?xml version="1.0" encoding="UTF-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
      <Document>
        <Placemark>
          <name>Varthur Secondary Canal Reach A</name>
          <LineString>
            <coordinates>
              77.7000,12.9500,0 77.7050,12.9550,0 77.7100,12.9600,0
            </coordinates>
          </LineString>
        </Placemark>
      </Document>
    </kml>
    """
    parser = MunicipalGISParser()
    result = parser.parse_kml(kml_data)

    assert result.has_errors is False
    assert len(result.reaches) == 1
    reach = result.reaches[0]
    assert reach.name == "Varthur Secondary Canal Reach A"
    assert reach.length_meters > 1000.0
    assert reach.is_within_bounds is True


def test_parse_malformed_payloads_safe_failure():
    parser = MunicipalGISParser()

    bad_geojson = parser.parse_geojson("{NOT_VALID_JSON}")
    assert bad_geojson.has_errors is True
    assert bad_geojson.is_inconclusive is True

    bad_kml = parser.parse_kml("<kml><UnclosedTag>")
    assert bad_kml.has_errors is True
    assert bad_kml.is_inconclusive is True
