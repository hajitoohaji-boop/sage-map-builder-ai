"""Deterministic map geometry validation and placement helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Bounds:
    width: int
    height: int

    def contains(self, x: float, y: float) -> bool:
        return 0.0 <= x <= self.width and 0.0 <= y <= self.height


def clamp_point(bounds: Bounds, x: float, y: float, margin: float = 0.0) -> tuple[float, float]:
    if margin < 0 or margin * 2 > min(bounds.width, bounds.height):
        raise ValueError("invalid margin")
    return (
        min(max(x, margin), bounds.width - margin),
        min(max(y, margin), bounds.height - margin),
    )


def evenly_spaced(count: int, start: float, end: float) -> tuple[float, ...]:
    if count < 1:
        return ()
    if count == 1:
        return ((start + end) / 2,)
    step = (end - start) / (count - 1)
    return tuple(start + step * i for i in range(count))
