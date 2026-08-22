from sage_map_builder.formats.chunk_identity_table import KNOWN_CHUNKS, identity


def test_known_chunk_versions_are_unique():
    keys = [(item.label, item.version) for item in KNOWN_CHUNKS]
    assert len(keys) == len(set(keys))


def test_object_is_nested_and_waypoints_verified():
    assert identity("Object", 3).nested
    assert identity("WaypointsList", 1).semantic_status == "verified"


def test_unknown_identity_returns_none():
    assert identity("NoSuchChunk", 99) is None
