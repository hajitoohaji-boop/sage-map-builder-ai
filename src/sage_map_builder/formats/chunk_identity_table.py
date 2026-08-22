"""Canonical source-backed identities for known MAP chunks."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChunkIdentity:
    label: str
    version: int
    order: int
    semantic_status: str
    nested: bool = False


KNOWN_CHUNKS: tuple[ChunkIdentity, ...] = (
    ChunkIdentity("HeightMapData", 4, 0, "opaque"),
    ChunkIdentity("BlendTileData", 7, 1, "opaque"),
    ChunkIdentity("WorldInfo", 1, 2, "opaque"),
    ChunkIdentity("ObjectsList", 3, 3, "opaque"),
    ChunkIdentity("Object", 3, 4, "opaque", True),
    ChunkIdentity("GlobalLighting", 3, 5, "opaque"),
    ChunkIdentity("WaypointsList", 1, 6, "verified"),
)


def identity(label: str, version: int) -> ChunkIdentity | None:
    return next((item for item in KNOWN_CHUNKS if item.label == label and item.version == version), None)
