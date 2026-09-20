"""Pytest configuration and shared test fixtures for MuniAudit-AI."""

import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.api.main import app
from app.storage.interface import LocalStorageAdapter


@pytest.fixture
def test_client():
    """Returns a TestClient instance for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def temp_storage_adapter():
    """Provides an isolated LocalStorageAdapter backed by a temporary directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        adapter = LocalStorageAdapter(base_path=Path(tmpdir))
        yield adapter
