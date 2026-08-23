"""Compare candidate chunk fingerprints between two samples."""
from __future__ import annotations

from dataclasses import dataclass

from .chunk_fingerprint import ChunkFingerprint


@dataclass(frozen=True)
class FingerprintComparison:
    left: ChunkFingerprint
    right: ChunkFingerprint

    @property
    def same_payload(self) -> bool:
        return self.left.sha256 == self.right.sha256

    @property
    def same_size(self) -> bool:
        return self.left.data_size == self.right.data_size


def compare(left: ChunkFingerprint, right: ChunkFingerprint) -> FingerprintComparison:
    if left.version != right.version:
        raise ValueError("cannot compare fingerprints with different chunk versions")
    return FingerprintComparison(left, right)
