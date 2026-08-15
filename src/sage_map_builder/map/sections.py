"""Conservative binary section detection for SAGE map research."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SectionCandidate:
    start: int
    end: int
    reason: str


def common_byte_runs(left: bytes, right: bytes, min_length: int = 8) -> tuple[SectionCandidate, ...]:
    """Find equal runs at identical offsets; no semantic labels are inferred."""
    if min_length < 1:
        raise ValueError("min_length must be positive")
    limit = min(len(left), len(right))
    result: list[SectionCandidate] = []
    start: int | None = None
    for offset in range(limit):
        equal = left[offset] == right[offset]
        if equal and start is None:
            start = offset
        elif not equal and start is not None:
            if offset - start >= min_length:
                result.append(SectionCandidate(start, offset, "equal bytes at identical offsets"))
            start = None
    if start is not None and limit - start >= min_length:
        result.append(SectionCandidate(start, limit, "equal bytes at identical offsets"))
    return tuple(result)


def marker_ranges(data: bytes, marker: bytes) -> tuple[int, ...]:
    """Return every marker offset without interpreting the surrounding data."""
    if not marker:
        raise ValueError("marker cannot be empty")
    offsets: list[int] = []
    cursor = 0
    while True:
        found = data.find(marker, cursor)
        if found < 0:
            return tuple(offsets)
        offsets.append(found)
        cursor = found + 1
