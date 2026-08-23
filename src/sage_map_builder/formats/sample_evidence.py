"""Cross-sample evidence aggregation without semantic guessing."""
from __future__ import annotations

from dataclasses import dataclass

from .evidence_bundle import CandidateEvidence


@dataclass(frozen=True)
class SampleEvidence:
    sample: str
    candidates: tuple[CandidateEvidence, ...]

    def for_identity(self, label: str, version: int) -> tuple[CandidateEvidence, ...]:
        return tuple(
            item for item in self.candidates
            if item.identity.label == label and item.identity.version == version
        )

    def best(self) -> CandidateEvidence | None:
        if not self.candidates:
            return None
        return max(self.candidates, key=lambda item: (item.score, -item.occurrence.ordinal))
