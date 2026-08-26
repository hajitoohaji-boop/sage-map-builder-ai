"""Immutable snapshot of the currently verified format surface."""
from __future__ import annotations

from dataclasses import dataclass

from .source_coverage import binary_verified_components


@dataclass(frozen=True)
class CoverageSnapshot:
    verified_components: tuple[str, ...]
    total_catalogued_components: int

    @property
    def verified_count(self) -> int:
        return len(self.verified_components)


def current_snapshot(total_catalogued_components: int) -> CoverageSnapshot:
    if total_catalogued_components < 0:
        raise ValueError("total_catalogued_components cannot be negative")
    return CoverageSnapshot(binary_verified_components(), total_catalogued_components)
