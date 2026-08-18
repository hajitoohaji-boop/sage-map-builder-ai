from sage_map_builder.formats.chunk_registry import ChunkCodec, ChunkCodecRegistry
from sage_map_builder.formats.opaque_codec import OpaqueCodec
from sage_map_builder.formats.source_chunk_validation import match_source_chunk, require_source_chunk
from sage_map_builder.formats.source_coverage import binary_verified_components, source_coverage
from sage_map_builder.formats.waypoints_chunk import WaypointLink, decode_waypoint_links, encode_waypoint_links


def test_unknown_source_chunk_is_not_accepted():
    assert match_source_chunk("NotARealChunk", 1) is None


def test_source_version_mismatch_is_rejected():
    match = match_source_chunk("WaypointsList", 99)
    assert match is not None
    assert match.verified is False
    try:
        require_source_chunk("WaypointsList", 99)
    except ValueError as exc:
        assert "version mismatch" in str(exc)
    else:
        raise AssertionError("version mismatch was accepted")


def test_registry_rejects_unknown_semantics():
    registry = ChunkCodecRegistry()
    try:
        registry.register(ChunkCodec("NotARealChunk", 1, lambda b: b, lambda v: bytes(v)))
    except ValueError as exc:
        assert "not explicitly supported" in str(exc)
    else:
        raise AssertionError("unknown chunk codec was registered")


def test_opaque_codec_is_lossless():
    codec = OpaqueCodec("WaypointsList", 1)
    payload = b"\x00\x01\x02\xff"
    value = codec.decode(payload)
    assert codec.encode(value) == payload


def test_waypoint_codec_round_trip():
    links = [WaypointLink(0, 2), WaypointLink(2, 5), WaypointLink(5, 0)]
    assert decode_waypoint_links(encode_waypoint_links(links)) == links


def test_coverage_does_not_overclaim_waypoints():
    coverage = source_coverage()
    assert coverage["waypoints"] == "source_backed_codec_not_binary_matched"
    assert binary_verified_components() == ("data_chunk",)
