"""Dataset Manifest and Provenance Tracking Engine for MuniAudit-AI."""

import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from app.domain.epistemic import ProvenanceTag
from app.storage.interface import calculate_sha256


class ManifestEntry(BaseModel):
    """An immutable metadata record tracking an evidentiary asset's provenance."""

    file_path: str
    sha256_hash: str
    byte_size: int
    provenance_tag: ProvenanceTag
    source_reference: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = Field(default_factory=dict)


class DatasetManifestEngine:
    """Manages dataset manifests and cryptographic provenance audit trails."""

    def __init__(
        self,
        manifest_json_path: Path | str = "data/manifests/dataset_manifest.json",
        provenance_csv_path: Path | str = "data/manifests/provenance.csv",
    ) -> None:
        self.manifest_json_path = Path(manifest_json_path)
        self.provenance_csv_path = Path(provenance_csv_path)
        self.manifest_json_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_files_if_missing()

    def _init_files_if_missing(self) -> None:
        if not self.manifest_json_path.exists():
            with open(self.manifest_json_path, "w", encoding="utf-8") as f:
                json.dump({"schema_version": "1.0", "assets": []}, f, indent=2)

        if not self.provenance_csv_path.exists():
            with open(self.provenance_csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "file_path",
                    "sha256_hash",
                    "byte_size",
                    "provenance_tag",
                    "source_reference",
                    "created_at",
                ])

    def register_asset(
        self,
        file_path: Path | str,
        provenance_tag: ProvenanceTag,
        source_reference: str,
        metadata: dict[str, Any] | None = None,
    ) -> ManifestEntry:
        """Computes SHA-256 hash and appends the asset to JSON and CSV manifests."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Cannot register non-existent file: {path}")

        raw_bytes = path.read_bytes()
        sha256_digest = calculate_sha256(raw_bytes)
        byte_size = len(raw_bytes)

        entry = ManifestEntry(
            file_path=str(path.as_posix()),
            sha256_hash=sha256_digest,
            byte_size=byte_size,
            provenance_tag=provenance_tag,
            source_reference=source_reference,
            metadata=metadata or {},
        )

        # Update JSON manifest
        with open(self.manifest_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Upsert by relative file_path
        data["assets"] = [a for a in data.get("assets", []) if a.get("file_path") != entry.file_path]
        data["assets"].append(entry.model_dump(mode="json"))

        with open(self.manifest_json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # Append to CSV provenance log
        with open(self.provenance_csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                entry.file_path,
                entry.sha256_hash,
                entry.byte_size,
                entry.provenance_tag.value,
                entry.source_reference,
                entry.created_at.isoformat(),
            ])

        return entry

    def load_manifest(self) -> list[ManifestEntry]:
        """Loads and returns all manifest entries."""
        if not self.manifest_json_path.exists():
            return []
        with open(self.manifest_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [ManifestEntry(**item) for item in data.get("assets", [])]

    def verify_dataset_integrity(self) -> dict[str, Any]:
        """Audits all registered files against their recorded cryptographic digests."""
        entries = self.load_manifest()
        verified_count = 0
        corrupted_files: list[str] = []
        missing_files: list[str] = []

        for entry in entries:
            path = Path(entry.file_path)
            if not path.exists():
                missing_files.append(entry.file_path)
                continue
            computed_hash = calculate_sha256(path.read_bytes())
            if computed_hash.lower() == entry.sha256_hash.lower():
                verified_count += 1
            else:
                corrupted_files.append(entry.file_path)

        return {
            "total_assets": len(entries),
            "verified_valid": verified_count,
            "corrupted_count": len(corrupted_files),
            "missing_count": len(missing_files),
            "is_tamper_free": len(corrupted_files) == 0 and len(missing_files) == 0,
            "corrupted_files": corrupted_files,
            "missing_files": missing_files,
        }
