"""Track evidence strength for map-format subsystems.

``source_available`` means EA WorldBuilder contains relevant read/write code.
It does NOT mean the repository's real map samples have been matched to that
structure yet. ``binary_verified`` is reserved for source + sample agreement.
"""
from __future__ import annotations

SOURCE_COMPONENTS = {
    "data_chunk": "source_and_binary_verified",
    "waypoints": "source_backed_codec_not_binary_matched",
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


def binary_verified_components() -> tuple[str, ...]:
    """Return only components whose source and real-sample evidence agree."""
    return tuple(name for name, status in SOURCE_COMPONENTS.items() if status == "source_and_binary_verified")
