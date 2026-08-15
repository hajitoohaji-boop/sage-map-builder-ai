"""Conservative representation of the currently verified map prefix.

Only the bytes we can verify are modeled. Unknown bytes remain available through
`raw_prefix`, so this layer cannot silently discard information.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MapHeaderObservation:
    """Observed prefix information, not yet a complete serialized header."""

    signature: bytes
    raw_prefix: bytes
    c_kmp_offset: int | None
    global_lighting_offset: int | None
    polygon_triggers_offset: int | None


def inspect_prefix(data: bytes, *, prefix_size: int = 128) -> MapHeaderObservation:
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    if prefix_size < 3:
        raise ValueError("prefix_size must be at least 3")

    prefix = data[:prefix_size]
    signature = prefix[:3]
    return MapHeaderObservation(
        signature=signature,
        raw_prefix=prefix,
        c_kmp_offset=_find(prefix, b"CkMp"),
        global_lighting_offset=_find(prefix, b"GlobalLighting"),
        polygon_triggers_offset=_find(prefix, b"PolygonTriggers"),
    )


def _find(data: bytes, marker: bytes) -> int | None:
    offset = data.find(marker)
    return offset if offset >= 0 else None
