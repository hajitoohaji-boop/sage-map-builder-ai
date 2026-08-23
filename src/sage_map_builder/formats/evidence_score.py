"""Deterministic score for codec evidence completeness."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceScore:
    source: bool
    samples: bool
    stable_range: bool
    round_trip: bool

    @property
    def points(self) -> int:
        return sum((self.source, self.samples, self.stable_range, self.round_trip))

    @property
    def complete(self) -> bool:
        return self.points == 4
