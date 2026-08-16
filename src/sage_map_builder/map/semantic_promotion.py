"""Gate semantic width/height candidates with raw and structural evidence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .multi_sample import consensus_for_offset
from .semantic_rules import check_dimension


@dataclass(frozen=True)
class DimensionCandidate:
    offset: int
    value: int
    samples: int
    status: str
    reason: str


def promote_dimension(samples: Sequence[bytes], offset: int, *, minimum_samples: int = 3) -> DimensionCandidate | None:
    if minimum_samples < 2:
        raise ValueError("minimum_samples must be at least 2")
    consensus = consensus_for_offset(samples, offset)
    if consensus.samples < minimum_samples or consensus.status != "stable":
        return None
    raw = bytes.fromhex(consensus.raw_values[0])
    value = int.from_bytes(raw, "little")
    check = check_dimension(value)
    if check.status != "supported":
        return DimensionCandidate(offset, value, consensus.samples, "rejected", check.reason)
    return DimensionCandidate(offset, value, consensus.samples, "candidate", "stable raw value is dimension-plausible; semantic role remains unproven")
