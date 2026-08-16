"""Structural evidence gate for width/height hypotheses."""

from __future__ import annotations

from dataclasses import dataclass

from .semantic_rules import check_dimension_pair


@dataclass(frozen=True)
class DimensionPairEvidence:
    width_offset: int
    height_offset: int
    width: int
    height: int
    status: str
    reason: str


def evaluate_dimension_pair(width_offset: int, height_offset: int, width: int, height: int) -> DimensionPairEvidence:
    if width_offset == height_offset:
        return DimensionPairEvidence(width_offset, height_offset, width, height, "rejected", "width and height cannot use the same offset")
    check = check_dimension_pair(width, height)
    if check.status != "supported":
        return DimensionPairEvidence(width_offset, height_offset, width, height, "rejected", check.reason)
    if width * height > 512 * 512:
        return DimensionPairEvidence(width_offset, height_offset, width, height, "rejected", "dimension product exceeds supported map area")
    return DimensionPairEvidence(width_offset, height_offset, width, height, "candidate", "both dimensions are plausible; structural role is not yet proven")
