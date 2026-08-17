"""Track which map subsystems have direct World Builder source evidence."""
from __future__ import annotations

SOURCE_COMPONENTS = {
    "data_chunk": "confirmed",
    "waypoints": "confirmed",
    "height_map": "source_available",
    "objects": "source_available",
    "terrain": "source_available",
    "textures": "source_available",
    "scripts": "source_available",
    "players": "source_available",
    "water": "source_available",
    "roads": "source_available",
    "writer": "partial",
}


def source_coverage() -> dict[str, str]:
    return dict(SOURCE_COMPONENTS)
