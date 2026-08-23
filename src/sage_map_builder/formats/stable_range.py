"""Stable byte-range representation for comparative MAP evidence."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class StableRange:
    start: int
    end: int

    def __post_init__(self) -> None:
        if self.start < 0 or self.end < self.start:
            raise ValueError("invalid stable byte range")

    @property
    def size(self) -> int:
        return self.end - self.start

    def overlaps(self, other: "StableRange") -> bool:
        return self.start < other.end and other.start < self.end
