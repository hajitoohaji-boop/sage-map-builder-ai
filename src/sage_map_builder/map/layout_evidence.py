"""Check whether a dimension pair is compatible with a byte-region layout."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LayoutEvidence:
    width: int
    height: int
    cells: int
    bytes_per_cell: int
    expected_bytes: int
    available_bytes: int
    status: str
    reason: str


def evaluate_layout(width: int, height: int, bytes_per_cell: int, available_bytes: int) -> LayoutEvidence:
    if width <= 0 or height <= 0 or bytes_per_cell <= 0 or available_bytes < 0:
        return LayoutEvidence(width, height, 0, bytes_per_cell, 0, available_bytes, "rejected", "layout inputs must be positive")
    cells = width * height
    expected = cells * bytes_per_cell
    if expected > available_bytes:
        return LayoutEvidence(width, height, cells, bytes_per_cell, expected, available_bytes, "rejected", "expected region exceeds available bytes")
    return LayoutEvidence(width, height, cells, bytes_per_cell, expected, available_bytes, "candidate", "layout fits available bytes; region meaning is not proven")
