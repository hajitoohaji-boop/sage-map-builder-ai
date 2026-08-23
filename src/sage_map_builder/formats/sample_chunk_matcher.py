"""Match scanned chunk candidates to source-backed identities without guessing."""
from __future__ import annotations

from dataclasses import dataclass

from .chunk_identity_table import ChunkIdentity, KNOWN_CHUNKS
from .chunk_index import ChunkIndex, IndexedChunk


@dataclass(frozen=True)
class ChunkCandidate:
    identity: ChunkIdentity
    occurrences: tuple[IndexedChunk, ...]


def candidates(index: ChunkIndex) -> tuple[ChunkCandidate, ...]:
    result: list[ChunkCandidate] = []
    for spec in KNOWN_CHUNKS:
        occurrences = tuple(
            item for item in index.items if item.span.header.version == spec.version
        )
        if occurrences:
            result.append(ChunkCandidate(spec, occurrences))
    return tuple(result)
