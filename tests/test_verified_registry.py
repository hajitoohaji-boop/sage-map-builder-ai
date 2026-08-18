from sage_map_builder.formats.verified_registry import build_verified_registry


def test_verified_registry_contains_only_currently_verified_codec():
    registry = build_verified_registry()
    assert registry.require("WaypointsList", 1)
    assert registry.get("ObjectsList", 3) is None
    assert registry.get("HeightMapData", 4) is None
