"""Conservative scanner for candidate DataChunk streams.

This module does not identify chunk labels or table-of-contents entries. It only
answers a narrower binary question: starting at a supplied offset, can a region
be consumed as a sequence of source-backed four-byte DataChunk headers without
running past the region?
"""
from __future__ import annotations

from dataclasses import dataclass

from sage_map_builder.formats.chunk_sequence import OpaqueChunk, read_chunk_sequence


@dataclass(frozen=True)
class ChunkStreamProbe:
    start: int
    end: int
    chunk_count: int
    versions: tuple[int, ...]
    payload_sizes: tuple[int, ...]
    valid: bool
    error: str | None = None


def probe_chunk_stream(data: bytes, start: int, end: int) -> ChunkStreamProbe:
    if start < 0 or end < start or end > len(data):
        raise ValueError("invalid chunk stream range")
    region = data[start:end]
    if not region:
        return ChunkStreamProbe(start, end, 0, (), (), True)
    try:
        chunks: tuple[OpaqueChunk, ...] = read_chunk_sequence(region)
    except ValueError as exc:
        return ChunkStreamProbe(start, end, 0, (), (), False, str(exc))
    return ChunkStreamProbe(
        start=start,
        end=end,
        chunk_count=len(chunks),
        versions=tuple(chunk.header.version for chunk in chunks),
        payload_sizes=tuple(len(chunk.payload) for chunk in chunks),
        valid=True,
    )


def find_valid_chunk_streams(
    data: bytes,
    candidates: list[tuple[int, int]] | tuple[tuple[int, int], ...],
) -> tuple[ChunkStreamProbe, ...]:
    """Probe only caller-supplied ranges; never invent boundaries."""
    return tuple(probe_chunk_stream(data, start, end) for start, end in candidates)
