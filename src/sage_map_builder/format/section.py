"""Verified/unknown section primitives for loss-aware map parsing."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ByteRange:
    start: int
    end: int

    def __post_init__(self) -> None:
        if self.start < 0 or self.end < self.start:
            raise ValueError("invalid byte range")

    @property
    def size(self) -> int:
        return self.end - self.start


@dataclass(frozen=True)
class SectionObservation:
    """An observed region; it is not assumed to be a parsed structure."""

    name: str
    location: ByteRange
    evidence: str
    verified: bool = False

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("section name cannot be empty")
        if not self.evidence:
            raise ValueError("evidence cannot be empty")
