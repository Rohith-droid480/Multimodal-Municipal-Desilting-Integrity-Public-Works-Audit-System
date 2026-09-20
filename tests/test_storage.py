"""Tests for evidence storage adapters and cryptographic integrity."""

import hashlib

from app.storage.interface import LocalStorageAdapter, calculate_sha256


def test_calculate_sha256():
    sample_data = b"MuniAudit-AI evidence verification payload"
    expected_hash = hashlib.sha256(sample_data).hexdigest().lower()
    computed = calculate_sha256(sample_data)
    assert computed == expected_hash


def test_local_storage_store_and_retrieve(temp_storage_adapter: LocalStorageAdapter):
    dossier_id = "test-dossier-001"
    filename = "weighbridge_slip_01.pdf"
    content = b"Mock PDF weighbridge content with gross=24500 tare=9200"

    uri, sha256_digest, byte_size = temp_storage_adapter.store_artifact(
        dossier_id=dossier_id, filename=filename, data=content
    )

    assert byte_size == len(content)
    assert sha256_digest == calculate_sha256(content)

    retrieved = temp_storage_adapter.retrieve_artifact(uri)
    assert retrieved == content

    is_valid = temp_storage_adapter.verify_integrity(uri, sha256_digest)
    assert is_valid is True

    tampered_check = temp_storage_adapter.verify_integrity(uri, "0" * 64)
    assert tampered_check is False
