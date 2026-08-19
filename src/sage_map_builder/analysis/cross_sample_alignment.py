"""Position-independent comparison of source-backed marker sequences.

Offsets are intentionally not treated as stable identities across maps. The
comparison aligns the ordered (label, version) observations and reports their
relative order and offset deltas only as observations.
"""
from __future__ import annotations
from dataclasses import dataclass
from .source_chunk_markers import SourceChunkMarker

@dataclass(frozen=True)
class MarkerAlignment:
    left_index: int
    right_index: int
    label: str
    version: int
    left_offset: int
    right_offset: int
    offset_delta: int


def align_markers(
    left: tuple[SourceChunkMarker, ...],
    right: tuple[SourceChunkMarker, ...],
) -> tuple[MarkerAlignment, ...]:
    """Align equal label/version occurrences by occurrence order, not offset."""
    left_groups: dict[tuple[str, int], list[tuple[int, SourceChunkMarker]]] = {}
    right_groups: dict[tuple[str, int], list[tuple[int, SourceChunkMarker]]] = {}
    for index, marker in enumerate(left):
        left_groups.setdefault((marker.label, marker.version), []).append((index, marker))
    for index, marker in enumerate(right):
        right_groups.setdefault((marker.label, marker.version), []).append((index, marker))

    result: list[MarkerAlignment] = []
    for key in sorted(left_groups.keys() & right_groups.keys()):
        for (li, lm), (ri, rm) in zip(left_groups[key], right_groups[key]):
            result.append(MarkerAlignment(li, ri, lm.label, lm.version, lm.offset, rm.offset, rm.offset - lm.offset))
    return tuple(result)
