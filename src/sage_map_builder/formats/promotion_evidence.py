"""Evidence bundle required before a MAP chunk can be promoted."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PromotionEvidence:
    source_reference: str
    sample_references: tuple[str, ...]
    stable_ranges: tuple[tuple[int, int], ...]
    round_trip_identical: bool

    @property
    def sufficient(self) -> bool:
        return bool(
            self.source_reference
            and self.sample_references
            and self.stable_ranges
            and self.round_trip_identical
        )

    def require(self) -> None:
        if not self.sufficient:
            raise ValueError("promotion evidence is incomplete")
