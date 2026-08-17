"""Conservative section-boundary extraction from observed binary markers.

This module records boundaries; it deliberately does not assign semantic names.
"""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256

@dataclass(frozen=True)
class SectionEvidence:
    start: int
    end: int
    length: int
    sha256: str
    preview_hex: str


def boundaries(data: bytes, markers: tuple[bytes, ...]) -> tuple[int, ...]:
    points = {0, len(data)}
    for marker in markers:
        start = 0
        while True:
            pos = data.find(marker, start)
            if pos < 0:
                break
            points.add(pos)
            start = pos + 1
    return tuple(sorted(points))


def section_evidence(data: bytes, markers: tuple[bytes, ...] = (b"EAR\x00", b"CkMp")) -> tuple[SectionEvidence, ...]:
    points = boundaries(data, markers)
    out = []
    for start, end in zip(points, points[1:]):
        chunk = data[start:end]
        out.append(SectionEvidence(start, end, len(chunk), sha256(chunk).hexdigest(), chunk[:32].hex(" ")))
    return tuple(out)
