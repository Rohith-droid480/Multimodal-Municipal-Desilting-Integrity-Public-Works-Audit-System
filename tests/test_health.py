"""Tests for the /health diagnostics endpoint."""

from fastapi.testclient import TestClient


def test_health_check_status_code(test_client: TestClient):
    response = test_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "subsystems" in data
    assert "invariants" in data


def test_health_check_invariants(test_client: TestClient):
    response = test_client.get("/health")
    data = response.json()
    invariants = data["invariants"]

    assert invariants["mass_balance_tolerance_kg"] == 20.0
    assert invariants["max_silt_density_t_m3"] == 1.90
    assert invariants["geodesic_speed_ceiling_kmh"] == 80.0
    assert invariants["sscd_similarity_threshold"] == 0.82
