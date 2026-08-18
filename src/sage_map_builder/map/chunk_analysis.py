"""Combine bounded raw DataChunk parsing with externally supplied identities.

This module deliberately does not infer semantic labels from binary payloads.
The caller must supply an evidence-backed identity for each region.
"""
from __future__ import annotations
from dataclasses import dataclass
from sage_map_builder.formats.chunk_sequence_reader import RawChunk, read_sequence
from sage_map_builder.formats.chunk_batch import IdentifiedChunk

@dataclass(frozen=True)
class RegionChunkAnalysis:
    start: int
    end: int
    chunks: tuple[RawChunk, ...]

    @property
    def payload_size(self) -> int:
        return sum(len(c.payload) for c in self.chunks)


def analyze_region(data: bytes, start: int, end: int) -> RegionChunkAnalysis:
    chunks = read_sequence(data, start, end)
    return RegionChunkAnalysis(start, end, chunks)


def identify_chunk(chunk: RawChunk, label: str) -> IdentifiedChunk:
    if not label:
        raise ValueError("chunk label cannot be empty")
    return IdentifiedChunk(label, chunk.header.version, chunk.payload)
