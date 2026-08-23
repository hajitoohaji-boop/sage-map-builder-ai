"""Manifest tying a codec identity to its promotion evidence."""
from __future__ import annotations

from dataclasses import dataclass

from .promotion_evidence import PromotionEvidence
from .evidence_score import EvidenceScore


@dataclass(frozen=True)
class PromotionManifest:
    label: str
    version: int
    evidence: PromotionEvidence

    @property
    def score(self) -> EvidenceScore:
        return EvidenceScore(
            bool(self.evidence.source_reference),
            bool(self.evidence.sample_references),
            bool(self.evidence.stable_ranges),
            self.evidence.round_trip_identical,
        )

    @property
    def promotable(self) -> bool:
        return self.score.complete
