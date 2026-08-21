"""Small, immutable manifest for binary-format evidence."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceClaim:
    label: str
    version: int
    source_reference: str
    sample_reference: str
    confidence: str = "observed"


@dataclass(frozen=True)
class EvidenceManifest:
    claims: tuple[EvidenceClaim, ...] = ()

    def add(self, claim: EvidenceClaim) -> "EvidenceManifest":
        return EvidenceManifest(self.claims + (claim,))

    def for_chunk(self, label: str, version: int) -> tuple[EvidenceClaim, ...]:
        return tuple(c for c in self.claims if c.label == label and c.version == version)
