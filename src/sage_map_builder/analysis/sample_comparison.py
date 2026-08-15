"""Byte-level comparison primitives for real map samples."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ByteDifference:
    offset: int
    left: int | None
    right: int | None


def compare_bytes(left: bytes, right: bytes, *, limit: int | None = None) -> tuple[ByteDifference, ...]:
    if not isinstance(left, bytes) or not isinstance(right, bytes):
        raise TypeError("both samples must be bytes")
    if limit is not None and limit < 0:
        raise ValueError("limit must be non-negative")

    differences: list[ByteDifference] = []
    size = max(len(left), len(right))
    for offset in range(size):
        left_byte = left[offset] if offset < len(left) else None
        right_byte = right[offset] if offset < len(right) else None
        if left_byte != right_byte:
            differences.append(ByteDifference(offset, left_byte, right_byte))
            if limit is not None and len(differences) >= limit:
                break
    return tuple(differences)
