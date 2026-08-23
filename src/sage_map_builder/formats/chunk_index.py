"""Index of scanned DataChunk spans for later source-label matching."""
from __future__ import annotations

from dataclasses import dataclass

from .chunk_stream import ChunkSpan


@dataclass(frozen=True)
class IndexedChunk:
    ordinal: int
    span: ChunkSpan


@dataclass(frozen=True)
class ChunkIndex:
    items: tuple[IndexedChunk, ...]

    @classmethod
    def from_spans(cls, spans: tuple[ChunkSpan, ...]) -> "ChunkIndex":
        return cls(tuple(IndexedChunk(i, span) for i, span in enumerate(spans)))

    def by_version(self, version: int) -> tuple[IndexedChunk, ...]:
        return tuple(item for item in self.items if item.span.header.version == version)
