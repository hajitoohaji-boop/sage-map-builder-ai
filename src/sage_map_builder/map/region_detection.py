"""Deterministic discovery of candidate byte regions from markers and runs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ByteRegion:
    start: int
    end: int
    source: str

    @property
    def size(self) -> int:
        return self.end - self.start


def marker_regions(data: bytes, marker: bytes = b"CkMp") -> tuple[ByteRegion, ...]:
    if not marker:
        raise ValueError("marker must not be empty")
    offsets: list[int] = []
    cursor = 0
    while True:
        pos = data.find(marker, cursor)
        if pos < 0:
            break
        offsets.append(pos)
        cursor = pos + 1
    if not offsets:
        return ()
    boundaries = offsets + [len(data)]
    return tuple(
        ByteRegion(start, end, f"marker:{marker.decode(errors='replace')}")
        for start, end in zip(offsets, boundaries[1:])
        if end > start
    )


def bounded_regions(data: bytes, boundaries: list[int]) -> tuple[ByteRegion, ...]:
    points = sorted(set([0, len(data), *boundaries]))
    return tuple(
        ByteRegion(a, b, "boundary") for a, b in zip(points, points[1:]) if b > a
    )
