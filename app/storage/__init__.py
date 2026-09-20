"""Evidence Storage Interfaces & Implementations."""

from app.storage.interface import (
    LocalStorageAdapter,
    StorageAdapter,
    calculate_sha256,
    get_storage_adapter,
)

__all__ = [
    "LocalStorageAdapter",
    "StorageAdapter",
    "calculate_sha256",
    "get_storage_adapter",
]
