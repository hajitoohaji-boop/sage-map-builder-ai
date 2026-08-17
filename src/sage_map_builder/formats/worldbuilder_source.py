"""Facts directly extracted from EA's released WorldBuilder source.

These are deliberately metadata-only until binary layout details are independently
confirmed against real map samples. Do not treat names here as guessed semantics.
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


DATA_CHUNK_FACTS = DataChunkFacts()
WORLD_BUILDER_SAVE_FACTS = WorldBuilderSaveFacts()


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
    }
