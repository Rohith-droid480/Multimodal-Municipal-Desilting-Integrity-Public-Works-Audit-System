"""Integration tests for Benchmark Dossier Loader and Manifest Engine."""

from app.domain.epistemic import DossierStatus, EpistemicCategory, ProvenanceTag
from app.ingestion.benchmark_loader import BenchmarkDossierLoader, BenchmarkDossierType
from app.ingestion.manifest import DatasetManifestEngine
from app.storage.interface import LocalStorageAdapter


def test_build_clean_compliant_dossier(tmp_path):
    storage = LocalStorageAdapter(base_path=tmp_path)
    loader = BenchmarkDossierLoader(storage_adapter=storage)

    dossier = loader.build_benchmark_dossier(BenchmarkDossierType.CLEAN_COMPLIANT)
    assert dossier.status == DossierStatus.QUEUED
    assert len(dossier.evidence_items) == 3
    assert len(dossier.findings) == 0

    # Verify all artifacts are cryptographically intact in storage
    for item in dossier.evidence_items:
        assert storage.verify_integrity(item.storage_uri, item.sha256_digest) is True
        assert item.provenance_tag == ProvenanceTag.SYNTHETIC_DATA


def test_build_substantive_inconsistency_dossier(tmp_path):
    storage = LocalStorageAdapter(base_path=tmp_path)
    loader = BenchmarkDossierLoader(storage_adapter=storage)

    dossier = loader.build_benchmark_dossier(BenchmarkDossierType.SUBSTANTIVE_INCONSISTENCY)
    assert dossier.status == DossierStatus.COMPLETED
    assert len(dossier.evidence_items) == 1
    assert len(dossier.findings) == 1

    finding = dossier.findings[0]
    assert finding.epistemic_category == EpistemicCategory.RULE_RESULT
    assert finding.observed_value == "46,500 KG"
    assert len(finding.evidence_refs) == 1


def test_build_inconclusive_data_dossier(tmp_path):
    storage = LocalStorageAdapter(base_path=tmp_path)
    loader = BenchmarkDossierLoader(storage_adapter=storage)

    dossier = loader.build_benchmark_dossier(BenchmarkDossierType.INCONCLUSIVE_DATA)
    assert dossier.status == DossierStatus.INCONCLUSIVE
    assert len(dossier.findings) == 1
    assert "Illegible" in dossier.findings[0].title


def test_manifest_engine_registration_and_integrity(tmp_path):
    manifest_json = tmp_path / "dataset_manifest.json"
    provenance_csv = tmp_path / "provenance.csv"
    engine = DatasetManifestEngine(
        manifest_json_path=manifest_json,
        provenance_csv_path=provenance_csv,
    )

    sample_file = tmp_path / "sample_weighbridge_slip.png"
    sample_file.write_bytes(b"\x89PNG\r\n\x1a\nMockSlipDataBytes")

    entry = engine.register_asset(
        file_path=sample_file,
        provenance_tag=ProvenanceTag.SYNTHETIC_DATA,
        source_reference="ProceduralWeighbridgeGenerator(Seed=42)",
    )

    assert len(entry.sha256_hash) == 64
    assert entry.byte_size > 0

    audit = engine.verify_dataset_integrity()
    assert audit["total_assets"] == 1
    assert audit["verified_valid"] == 1
    assert audit["is_tamper_free"] is True

    # Tamper test
    sample_file.write_bytes(b"TamperedBytesAltered")
    tampered_audit = engine.verify_dataset_integrity()
    assert tampered_audit["is_tamper_free"] is False
    assert tampered_audit["corrupted_count"] == 1
