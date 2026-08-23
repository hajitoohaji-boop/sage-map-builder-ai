"""Cross-sample evidence matrix for known MAP chunk identities."""
from __future__ import annotations

from dataclasses import dataclass

from .chunk_identity_table import KNOWN_CHUNKS, ChunkIdentity
from .sample_evidence import SampleEvidence


@dataclass(frozen=True)
class EvidenceCell:
    identity: ChunkIdentity
    left_count: int
    right_count: int
    left_best_score: int
    right_best_score: int

    @property
    def comparable(self) -> bool:
        return self.left_count > 0 and self.right_count > 0

    @property
    def score(self) -> int:
        return self.left_best_score + self.right_best_score


def build_matrix(left: SampleEvidence, right: SampleEvidence) -> tuple[EvidenceCell, ...]:
    cells: list[EvidenceCell] = []
    for spec in KNOWN_CHUNKS:
        la = left.for_identity(spec.label, spec.version)
        ra = right.for_identity(spec.label, spec.version)
        cells.append(EvidenceCell(
            identity=spec,
            left_count=len(la),
            right_count=len(ra),
            left_best_score=la[0].score if la else 0,
            right_best_score=ra[0].score if ra else 0,
        ))
    return tuple(cells)
