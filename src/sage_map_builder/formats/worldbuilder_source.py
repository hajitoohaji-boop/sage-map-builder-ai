"""Facts directly extracted from EA's released WorldBuilder source.

These facts are intentionally split from binary observations. A source fact tells
us what WorldBuilder writes/reads; it does not by itself prove that a particular
byte range in one of our samples is that structure.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DataChunkFacts:
    header_bytes: int = 4
    version_type: str = "uint16"
    has_table_of_contents: bool = True
    has_label: bool = True
    has_version: bool = True
    has_data_size: bool = True


@dataclass(frozen=True)
class WorldBuilderSaveFacts:
    heightmap_serialized_first: bool = True
    waypoint_chunk_label: str = "WaypointsList"
    waypoint_chunk_version: int = 1
    waypoint_links_store_count: bool = True
    waypoint_link_record_ints: int = 2
    compression_selected_from_world_dict_when_present: bool = True


@dataclass(frozen=True)
class SourceChunkSpec:
    """A chunk whose label/version are explicit in released WB source.

    ``container_order`` is the order in which the save routine emits the
    top-level chunks when the surrounding subsystem is enabled. It is not a
    claim about byte offsets in any particular map sample.
    """

    label: str
    version: int
    container_order: int
    nested: bool = False
    parent: str | None = None


# Explicit openDataChunk() calls observed in WorldBuilder source. The entries
# below intentionally exclude chunks whose label/version is hidden behind a
# helper until that helper is audited separately (for example SidesList and
# PolygonTrigger output).
SOURCE_CHUNKS: tuple[SourceChunkSpec, ...] = (
    SourceChunkSpec("HeightMapData", 4, 1),
    SourceChunkSpec("BlendTileData", 7, 2),
    SourceChunkSpec("WorldInfo", 1, 3),
    SourceChunkSpec("ObjectsList", 3, 4),
    SourceChunkSpec("Object", 3, 5, nested=True, parent="ObjectsList"),
    SourceChunkSpec("GlobalLighting", 3, 6),
    SourceChunkSpec("WaypointsList", 1, 7),
)

DATA_CHUNK_FACTS = DataChunkFacts()
WORLD_BUILDER_SAVE_FACTS = WorldBuilderSaveFacts()


def source_chunk_specs() -> tuple[SourceChunkSpec, ...]:
    """Return the immutable source-backed chunk catalogue."""
    return SOURCE_CHUNKS


def find_source_chunk(label: str) -> SourceChunkSpec | None:
    """Find an exact source-backed chunk label without guessing aliases."""
    for spec in SOURCE_CHUNKS:
        if spec.label == label:
            return spec
    return None


def verified_source_facts() -> dict:
    return {
        "data_chunk": {
            "header_bytes": DATA_CHUNK_FACTS.header_bytes,
            "version_type": DATA_CHUNK_FACTS.version_type,
            "has_table_of_contents": DATA_CHUNK_FACTS.has_table_of_contents,
            "has_label": DATA_CHUNK_FACTS.has_label,
            "has_version": DATA_CHUNK_FACTS.has_version,
            "has_data_size": DATA_CHUNK_FACTS.has_data_size,
        },
        "worldbuilder_save": {
            "heightmap_serialized_first": WORLD_BUILDER_SAVE_FACTS.heightmap_serialized_first,
            "waypoint_chunk_label": WORLD_BUILDER_SAVE_FACTS.waypoint_chunk_label,
            "waypoint_chunk_version": WORLD_BUILDER_SAVE_FACTS.waypoint_chunk_version,
            "waypoint_links_store_count": WORLD_BUILDER_SAVE_FACTS.waypoint_links_store_count,
            "waypoint_link_record_ints": WORLD_BUILDER_SAVE_FACTS.waypoint_link_record_ints,
            "compression_selected_from_world_dict_when_present": WORLD_BUILDER_SAVE_FACTS.compression_selected_from_world_dict_when_present,
        },
        "explicit_chunks": [
            {
                "label": spec.label,
                "version": spec.version,
                "container_order": spec.container_order,
                "nested": spec.nested,
                "parent": spec.parent,
            }
            for spec in SOURCE_CHUNKS
        ],
    }
