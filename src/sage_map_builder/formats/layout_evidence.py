"""Evidence checks for a candidate byte layout."""
from __future__ import annotations

from dataclasses import dataclass

from .candidate_layout import CandidateLayout


@dataclass(frozen=True)
class LayoutEvidence:
    payload_size: int
    covered_bytes: int
    contiguous: bool

    @property
    def exact(self) -> bool:
        return self.contiguous and self.payload_size == self.covered_bytes


def evaluate(candidate: CandidateLayout, payload_size: int) -> LayoutEvidence:
    if payload_size < 0:
        raise ValueError("payload_size cannot be negative")
    return LayoutEvidence(payload_size, candidate.covered_bytes, candidate.contiguous)
