import pytest
from sage_map_builder.formats.chunk_registry import ChunkCodec, ChunkCodecRegistry


def test_registry_accepts_only_source_verified_codec():
    registry = ChunkCodecRegistry()
    registry.register(ChunkCodec("WaypointsList", 1, lambda b: b, lambda o: o))
    assert registry.require("WaypointsList", 1).label == "WaypointsList"


def test_registry_rejects_unknown_codec():
    registry = ChunkCodecRegistry()
    with pytest.raises(ValueError):
        registry.register(ChunkCodec("UnknownChunk", 1, lambda b: b, lambda o: o))


def test_registry_rejects_duplicate_codec():
    registry = ChunkCodecRegistry()
    codec = ChunkCodec("WaypointsList", 1, lambda b: b, lambda o: o)
    registry.register(codec)
    with pytest.raises(ValueError):
        registry.register(codec)
