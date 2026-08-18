import pytest

from sage_map_builder.formats.chunk_dispatch import decode_chunk, encode_chunk
from sage_map_builder.formats.codec_result import DecodedChunk, OpaqueChunk
from sage_map_builder.formats.verified_registry import build_verified_registry


def test_verified_waypoints_dispatch_round_trip():
    registry = build_verified_registry()
    payload = b"\x01\x00\x00\x00\x00\x00"
    decoded = decode_chunk(registry, "WaypointsList", 1, payload)
    assert isinstance(decoded, DecodedChunk)
    assert encode_chunk(registry, decoded) == payload


def test_unknown_chunk_is_opaque_by_default():
    registry = build_verified_registry()
    decoded = decode_chunk(registry, "WorldInfo", 1, b"raw")
    assert isinstance(decoded, OpaqueChunk)
    assert encode_chunk(registry, decoded) == b"raw"


def test_unknown_chunk_can_be_required_as_verified():
    registry = build_verified_registry()
    with pytest.raises(KeyError):
        decode_chunk(registry, "WorldInfo", 1, b"raw", allow_opaque=False)
