"""Evidence report for comparing raw DataChunk sequences across map samples.

This layer intentionally assigns no semantic meaning to payload bytes. It only
records observations that are safe to compare before a source-backed codec is
registered.
"""
from __future__ import annotations

from dataclasses import dataclass
from collections import Counter

from .chunk_sequence_reader import RawChunk


@dataclass(frozen=True)
class ChunkEvidence:
    index: int
    version: int
    data_size: int
    payload_prefix: bytes


@dataclass(frozen=True)
class ChunkEvidenceReport:
    count: int
    versions: tuple[tuple[int, int], ...]
    sizes: tuple[tuple[int, int], ...]
    chunks: tuple[ChunkEvidence, ...]


def build_evidence_report(chunks: tuple[RawChunk, ...], prefix_size: int = 16) -> ChunkEvidenceReport:
    if prefix_size < 0:
        raise ValueError("prefix_size must be non-negative")
    versions = Counter(chunk.header.version for chunk in chunks)
    sizes = Counter(chunk.header.data_size for chunk in chunks)
    evidence = tuple(
        ChunkEvidence(
            index=index,
            version=chunk.header.version,
            data_size=chunk.header.data_size,
            payload_prefix=chunk.payload[:prefix_size],
        )
        for index, chunk in enumerate(chunks)
    )
    return ChunkEvidenceReport(
        count=len(chunks),
        versions=tuple(sorted(versions.items())),
        sizes=tuple(sorted(sizes.items())),
        chunks=evidence,
    )
