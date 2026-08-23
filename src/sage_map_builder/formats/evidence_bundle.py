"""Deterministic evidence bundle for a candidate MAP chunk."""
from __future__ import annotations

from dataclasses import dataclass

from .chunk_fingerprint import ChunkFingerprint
from .chunk_identity_table import ChunkIdentity
from .chunk_index import IndexedChunk


@dataclass(frozen=True)
class CandidateEvidence:
    identity: ChunkIdentity
    occurrence: IndexedChunk
    fingerprint: ChunkFingerprint
    source_backed: bool
    order_match: bool
    sample_name: str

    @property
    def score(self) -> int:
        return int(self.source_backed) + int(self.order_match)

    @property
    def promotable(self) -> bool:
        return self.score == 2
