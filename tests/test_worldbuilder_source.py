from sage_map_builder.formats.worldbuilder_source import (
    find_source_chunk,
    source_chunk_specs,
    verified_source_facts,
)


def test_worldbuilder_source_facts():
    facts = verified_source_facts()
    assert facts["data_chunk"]["header_bytes"] == 4
    assert facts["data_chunk"]["version_type"] == "uint16"
    assert facts["worldbuilder_save"]["waypoint_chunk_label"] == "WaypointsList"
    assert facts["worldbuilder_save"]["waypoint_chunk_version"] == 1
    assert facts["worldbuilder_save"]["waypoint_link_record_ints"] == 2


def test_source_chunk_catalog_contains_only_explicit_specs():
    specs = source_chunk_specs()
    assert [spec.label for spec in specs] == [
        "HeightMapData",
        "BlendTileData",
        "WorldInfo",
        "ObjectsList",
        "Object",
        "GlobalLighting",
        "WaypointsList",
    ]
    assert [spec.version for spec in specs] == [4, 7, 1, 3, 3, 3, 1]


def test_nested_object_chunk_is_explicitly_parented():
    spec = find_source_chunk("Object")
    assert spec is not None
    assert spec.nested is True
    assert spec.parent == "ObjectsList"


def test_unknown_chunk_is_not_guessed():
    assert find_source_chunk("ScriptsList") is None


def test_verified_facts_expose_catalog():
    facts = verified_source_facts()
    assert facts["explicit_chunks"][0]["label"] == "HeightMapData"
    assert facts["explicit_chunks"][-1]["label"] == "WaypointsList"
