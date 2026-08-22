"""Safety gate between source facts and binary sample claims.

A WorldBuilder source fact alone is never sufficient to declare a byte range
semantic. A claim must also name a concrete sample and an observed range.
"""
from __future__ import annotations

from dataclasses import dataclass

from .source_chunk_catalog import find_source_chunk_version


@dataclass(frozen=True)
class SampleRangeClaim:
    sample: str
    label: str
    version: int
    start: int
    end: int

    def __post_init__(self) -> None:
        if self.start < 0 or self.end < self.start:
            raise ValueError("invalid sample byte range")
        if find_source_chunk_version(self.label, self.version) is None:
            raise ValueError("chunk label/version is not source-backed")


@dataclass(frozen=True)
class SampleGate:
    claims: tuple[SampleRangeClaim, ...] = ()

    def add(self, claim: SampleRangeClaim) -> "SampleGate":
        return SampleGate(self.claims + (claim,))

    def for_sample(self, sample: str) -> tuple[SampleRangeClaim, ...]:
        return tuple(c for c in self.claims if c.sample == sample)
