"""Stable fingerprints for scanned chunk payloads, without semantic claims."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib

from .chunk_stream import ChunkSpan


@dataclass(frozen=True)
class ChunkFingerprint:
    offset: int
    version: int
    data_size: int
    sha256: str


def fingerprint(data: bytes, span: ChunkSpan) -> ChunkFingerprint:
    payload = data[span.payload_start:span.payload_end]
    if len(payload) != span.header.data_size:
        raise ValueError("span payload does not match header size")
    return ChunkFingerprint(
        offset=span.offset,
        version=span.header.version,
        data_size=span.header.data_size,
        sha256=hashlib.sha256(payload).hexdigest(),
    )
