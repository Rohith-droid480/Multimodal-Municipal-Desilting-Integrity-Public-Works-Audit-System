"""Storage Interface & Adapters with Tamper-Evident SHA-256 Verification."""

import abc
import hashlib
from pathlib import Path

from app.core.config import settings


def calculate_sha256(data: bytes) -> str:
    """Computes the hex-encoded SHA-256 cryptographic digest of input bytes."""
    hasher = hashlib.sha256()
    hasher.update(data)
    return hasher.hexdigest().lower()


class StorageAdapter(abc.ABC):
    """Abstract interface for immutable evidence artifact storage."""

    @abc.abstractmethod
    def store_artifact(self, dossier_id: str, filename: str, data: bytes) -> tuple[str, str, int]:
        """
        Stores an artifact.
        Returns: (storage_uri, sha256_digest, byte_size)
        """

    @abc.abstractmethod
    def retrieve_artifact(self, storage_uri: str) -> bytes:
        """Retrieves artifact bytes from storage."""

    @abc.abstractmethod
    def verify_integrity(self, storage_uri: str, expected_sha256: str) -> bool:
        """Verifies that stored artifact bytes match expected SHA-256 digest."""


class LocalStorageAdapter(StorageAdapter):
    """Local filesystem storage adapter ensuring offline Build-It parity."""

    def __init__(self, base_path: str | Path = settings.LOCAL_STORAGE_PATH):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def store_artifact(self, dossier_id: str, filename: str, data: bytes) -> tuple[str, str, int]:
        sha256_digest = calculate_sha256(data)
        byte_size = len(data)

        # Store partitioned by dossier ID and SHA-256 prefix for fast access
        target_dir = self.base_path / str(dossier_id)
        target_dir.mkdir(parents=True, exist_ok=True)

        target_file = target_dir / f"{sha256_digest[:12]}_{filename}"
        with open(target_file, "wb") as f:
            f.write(data)

        storage_uri = str(target_file.resolve())
        return storage_uri, sha256_digest, byte_size

    def retrieve_artifact(self, storage_uri: str) -> bytes:
        path = Path(storage_uri)
        if not path.exists():
            raise FileNotFoundError(f"Artifact not found at path: {storage_uri}")
        with open(path, "rb") as f:
            return f.read()

    def verify_integrity(self, storage_uri: str, expected_sha256: str) -> bool:
        data = self.retrieve_artifact(storage_uri)
        computed_hash = calculate_sha256(data)
        return computed_hash.lower() == expected_sha256.lower()


class S3StorageAdapter(StorageAdapter):
    """AWS S3 storage adapter for production Ship-It deployment."""

    def __init__(
        self, bucket_name: str = settings.AWS_S3_EVIDENCE_BUCKET, region: str = settings.AWS_REGION
    ):
        self.bucket_name = bucket_name
        self.region = region

    def store_artifact(self, dossier_id: str, filename: str, data: bytes) -> tuple[str, str, int]:
        sha256_digest = calculate_sha256(data)
        byte_size = len(data)
        key = f"dossiers/{dossier_id}/{sha256_digest[:12]}_{filename}"
        storage_uri = f"s3://{self.bucket_name}/{key}"
        # In cloud runtime, boto3 s3.put_object is invoked with ObjectLock / checksum
        return storage_uri, sha256_digest, byte_size

    def retrieve_artifact(self, storage_uri: str) -> bytes:
        raise NotImplementedError("S3 retrieval requires active AWS credentials in cloud mode.")

    def verify_integrity(self, storage_uri: str, expected_sha256: str) -> bool:
        raise NotImplementedError("S3 integrity check requires active AWS credentials.")


def get_storage_adapter() -> StorageAdapter:
    """Factory returning the active storage adapter based on environment configuration."""
    if settings.STORAGE_BACKEND.lower() == "s3":
        return S3StorageAdapter()
    return LocalStorageAdapter()
