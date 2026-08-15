"""Conservative scanner for named binary sections in SAGE map samples.

This scanner only records byte positions of known textual markers. It does not
interpret the bytes around a marker as a section header. That distinction is
important because the supplied files use a binary serialization format where
some names are embedded in encoded data.
"""

from __future__ import annotations

from dataclasses import dataclass


KNOWN_MARKERS: tuple[bytes, ...] = (
    b"CkMp",
    b"GlobalLighting",
    b"PolygonTriggers",
    b"WaypointsLi",
)


@dataclass(frozen=True)
class MarkerHit:
    marker: bytes
    offset: int


def scan_markers(data: bytes) -> tuple[MarkerHit, ...]:
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")

    hits: list[MarkerHit] = []
    for marker in KNOWN_MARKERS:
        start = 0
        while True:
            offset = data.find(marker, start)
            if offset < 0:
                break
            hits.append(MarkerHit(marker=marker, offset=offset))
            start = offset + 1

    return tuple(sorted(hits, key=lambda hit: hit.offset))
