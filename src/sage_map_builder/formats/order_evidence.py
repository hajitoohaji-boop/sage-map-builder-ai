"""Order-based evidence for chunk candidates; never promotes semantics by itself."""
from __future__ import annotations

from dataclasses import dataclass

from .chunk_identity_table import ChunkIdentity
from .chunk_index import IndexedChunk


@dataclass(frozen=True)
class OrderEvidence:
    identity: ChunkIdentity
    occurrence: IndexedChunk
    expected_order: int
    distance: int

    @property
    def strong(self) -> bool:
        return self.distance == 0


def score(identity: ChunkIdentity, occurrence: IndexedChunk) -> OrderEvidence:
    distance = abs(occurrence.ordinal - identity.order)
    return OrderEvidence(identity, occurrence, identity.order, distance)
