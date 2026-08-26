"""Fail-closed gate for claiming the MAP format is complete."""
from __future__ import annotations

from .source_coverage import source_coverage

REQUIRED_FOR_COMPLETE = {
    "data_chunk": "source_and_binary_verified",
    "waypoints": "source_and_binary_verified",
    "height_map": "source_and_binary_verified",
    "objects": "source_and_binary_verified",
    "terrain": "source_and_binary_verified",
    "textures": "source_and_binary_verified",
    "scripts": "source_and_binary_verified",
    "players": "source_and_binary_verified",
    "water": "source_and_binary_verified",
    "roads": "source_and_binary_verified",
    "writer": "complete",
}


def completion_gaps() -> tuple[str, ...]:
    current = source_coverage()
    return tuple(
        name for name, required in REQUIRED_FOR_COMPLETE.items()
        if current.get(name) != required
    )


def require_complete() -> None:
    gaps = completion_gaps()
    if gaps:
        raise RuntimeError("MAP format is not complete; remaining: " + ", ".join(gaps))
