"""Byte-preserving map I/O primitives.

This module deliberately does not encode any unverified SAGE fields. It provides
an exact preservation path for files that have not yet been semantically decoded.
"""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path


@dataclass(frozen=True)
class PreservationResult:
    source_size: int
    output_size: int
    source_sha256: str
    output_sha256: str

    @property
    def identical(self) -> bool:
        return self.source_size == self.output_size and self.source_sha256 == self.output_sha256


def preserve_bytes(data: bytes) -> bytes:
    """Return an independent byte-for-byte copy."""
    return bytes(data)


def preserve_file(source: Path, output: Path) -> PreservationResult:
    data = source.read_bytes()
    preserved = preserve_bytes(data)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(preserved)
    return PreservationResult(
        len(data), len(preserved), sha256(data).hexdigest(), sha256(preserved).hexdigest()
    )
