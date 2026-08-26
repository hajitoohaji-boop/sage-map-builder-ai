"""Deterministic collection of candidate layouts for one chunk identity."""
from __future__ import annotations

from dataclasses import dataclass

from .candidate_layout import CandidateLayout


@dataclass(frozen=True)
class LayoutCandidateSet:
    label: str
    version: int
    candidates: tuple[CandidateLayout, ...]

    def ranked(self) -> tuple[CandidateLayout, ...]:
        return tuple(sorted(
            self.candidates,
            key=lambda item: (-item.confidence, -item.covered_bytes, item.label),
        ))

    def complete(self, payload_size: int) -> tuple[CandidateLayout, ...]:
        return tuple(
            item for item in self.ranked()
            if item.contiguous and item.covered_bytes == payload_size
        )
