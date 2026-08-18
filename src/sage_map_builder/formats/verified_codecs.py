"""Built-in codecs whose binary format is source-backed."""
from __future__ import annotations
from .chunk_registry import ChunkCodec, ChunkCodecRegistry
from .waypoints_chunk import WaypointLink, decode_waypoint_links, encode_waypoint_links


def build_verified_registry() -> ChunkCodecRegistry:
    registry = ChunkCodecRegistry()
    registry.register(
        ChunkCodec(
            label="WaypointsList",
            version=1,
            decoder=decode_waypoint_links,
            encoder=lambda value: encode_waypoint_links(list(value)),
        )
    )
    return registry
