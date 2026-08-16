"""Match dimension candidates against discovered byte regions.

The matcher ranks structural fits only. It never assigns a semantic section name.
"""

from __future__ import annotations

from dataclasses import dataclass

from .layout_evidence import evaluate_layout
from .region_detection import ByteRegion


@dataclass(frozen=True)
class LayoutMatch:
    region_start: int
    region_end: int
    width: int
    height: int
    bytes_per_cell: int
    expected_bytes: int
    remaining_bytes: int
    status: str


def match_region(region: ByteRegion, width: int, height: int, bytes_per_cell: int) -> LayoutMatch:
    evidence = evaluate_layout(width, height, bytes_per_cell, region.size)
    remaining = region.size - evidence.expected_bytes
    return LayoutMatch(
        region_start=region.start,
        region_end=region.end,
        width=width,
        height=height,
        bytes_per_cell=bytes_per_cell,
        expected_bytes=evidence.expected_bytes,
        remaining_bytes=remaining,
        status=evidence.status,
    )


def rank_matches(regions: tuple[ByteRegion, ...], candidates: tuple[tuple[int, int], ...], bytes_per_cell: int) -> tuple[LayoutMatch, ...]:
    matches = [match_region(region, w, h, bytes_per_cell) for region in regions for w, h in candidates]
    return tuple(sorted(matches, key=lambda item: (item.status != "candidate", abs(item.remaining_bytes), item.region_start)))
