"""Rank chunk candidates using only explicit, non-semantic evidence."""
from __future__ import annotations

from dataclasses import dataclass

from .chunk_identity_table import ChunkIdentity
from .chunk_index import IndexedChunk
from .order_evidence import score


@dataclass(frozen=True)
class RankedCandidate:
    identity: ChunkIdentity
    occurrence: IndexedChunk
    distance: int


def rank(identity: ChunkIdentity, occurrences: tuple[IndexedChunk, ...]) -> tuple[RankedCandidate, ...]:
    ranked = [
        RankedCandidate(identity, item, score(identity, item).distance)
        for item in occurrences
    ]
    ranked.sort(key=lambda item: (item.distance, item.occurrence.ordinal))
    return tuple(ranked)
