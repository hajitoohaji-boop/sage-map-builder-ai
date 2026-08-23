"""Deterministic pairing of evidence observations from two golden samples."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Observation:
    sample: str
    label: str
    version: int
    start: int
    end: int


@dataclass(frozen=True)
class PairedObservation:
    left: Observation
    right: Observation


def pair(left: tuple[Observation, ...], right: tuple[Observation, ...]) -> tuple[PairedObservation, ...]:
    right_by_key = {(item.label, item.version): item for item in right}
    return tuple(
        PairedObservation(item, right_by_key[(item.label, item.version)])
        for item in left
        if (item.label, item.version) in right_by_key
    )
