"""Multi-sample consensus checks for candidate map fields."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class Consensus:
    offset: int
    samples: int
    distinct_raw_values: int
    raw_values: tuple[str, ...]
    status: str


def consensus_for_offset(samples: Sequence[bytes], offset: int) -> Consensus:
    if offset < 0:
        raise ValueError("offset must be non-negative")
    values = tuple(
        data[offset:offset + 4].hex(" ")
        for data in samples
        if offset + 4 <= len(data)
    )
    distinct = tuple(dict.fromkeys(values))
    if not values:
        status = "insufficient_data"
    elif len(distinct) == 1:
        status = "stable"
    else:
        status = "variable"
    return Consensus(offset, len(values), len(distinct), distinct, status)


def stable_offsets(samples: Sequence[bytes], offsets: Sequence[int]) -> tuple[int, ...]:
    return tuple(
        offset for offset in offsets
        if consensus_for_offset(samples, offset).status == "stable"
    )
