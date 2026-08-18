import pytest

from sage_map_builder.formats.chunk_identity import ChunkIdentity


def test_chunk_identity_valid():
    assert ChunkIdentity("WaypointsList", 1).label == "WaypointsList"


def test_chunk_identity_rejects_invalid_values():
    with pytest.raises(ValueError):
        ChunkIdentity("", 1)
    with pytest.raises(ValueError):
        ChunkIdentity("X", 65536)
