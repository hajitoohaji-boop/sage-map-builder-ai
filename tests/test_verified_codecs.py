from sage_map_builder.formats.verified_codecs import build_verified_registry
from sage_map_builder.formats.waypoints_chunk import WaypointLink


def test_verified_registry_contains_waypoints_codec():
    registry = build_verified_registry()
    codec = registry.require("WaypointsList", 1)
    value = [WaypointLink(1, 2), WaypointLink(4, 7)]
    payload = codec.encoder(value)
    assert codec.decoder(payload) == value
