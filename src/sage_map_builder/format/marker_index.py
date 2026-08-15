"""Deterministic index of textual markers found in a binary map sample."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MarkerLocation:
    name: str
    offset: int


class MarkerIndex:
    def __init__(self, locations: tuple[MarkerLocation, ...]) -> None:
        self._locations = locations

    @property
    def locations(self) -> tuple[MarkerLocation, ...]:
        return self._locations

    def first(self, name: str) -> MarkerLocation | None:
        for location in self._locations:
            if location.name == name:
                return location
        return None


def build_marker_index(data: bytes, markers: tuple[bytes, ...]) -> MarkerIndex:
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    locations: list[MarkerLocation] = []
    for marker in markers:
        if not marker:
            raise ValueError("markers cannot contain empty values")
        start = 0
        while True:
            offset = data.find(marker, start)
            if offset < 0:
                break
            locations.append(MarkerLocation(marker.decode("ascii"), offset))
            start = offset + 1
    locations.sort(key=lambda item: (item.offset, item.name))
    return MarkerIndex(tuple(locations))
