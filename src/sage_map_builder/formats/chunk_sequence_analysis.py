"""Deterministic analysis of bounded DataChunk sequences.

This layer records what the binary reader can prove without assigning
semantic meanings to unknown payloads.
"""
from __future__ import annotations

from dataclasses import dataclass

from .chunk_sequence_reader import RawChunk, read_sequence


@dataclass(frozen=True)
class ChunkSequenceAnalysis:
    start: int
    end: int
    chunks: tuple[RawChunk, ...]
    versions: tuple[int, ...]
    payload_sizes: tuple[int, ...]


def analyze_sequence(data: bytes, start: int, end: int) -> ChunkSequenceAnalysis:
    chunks = read_sequence(data, start, end)
    return ChunkSequenceAnalysis(
        start=start,
        end=end,
        chunks=chunks,
        versions=tuple(chunk.header.version for chunk in chunks),
        payload_sizes=tuple(len(chunk.payload) for chunk in chunks),
    )
