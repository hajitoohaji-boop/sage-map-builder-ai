"""Promotion gate from multi-sample evidence to verified fields."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .multi_sample import consensus_for_offset


@dataclass(frozen=True)
class VerifiedField:
    offset: int
    raw_hex: str
    sample_count: int
    confidence: str
    rule: str


def promote_stable_offset(samples: Sequence[bytes], offset: int, *, minimum_samples: int = 3) -> VerifiedField | None:
    if minimum_samples < 2:
        raise ValueError("minimum_samples must be at least 2")
    result = consensus_for_offset(samples, offset)
    if result.samples < minimum_samples or result.status != "stable":
        return None
    return VerifiedField(
        offset=offset,
        raw_hex=result.raw_values[0],
        sample_count=result.samples,
        confidence="stable_raw_value",
        rule=f"identical 4-byte value across >= {minimum_samples} samples",
    )
