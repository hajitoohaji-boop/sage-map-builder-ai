"""Neutral waypoint model and validation."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Waypoint:
    name: str
    x: float
    y: float
    z: float = 0.0

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("waypoint name must not be empty")
        for value in (self.x, self.y, self.z):
            if not isinstance(value, (int, float)):
                raise TypeError("waypoint coordinates must be numeric")


def validate_waypoint(waypoint: Waypoint, width: int | None, height: int | None) -> None:
    if width is None or height is None:
        return
    if not 0 <= waypoint.x <= width or not 0 <= waypoint.y <= height:
        raise ValueError("waypoint is outside map bounds")
