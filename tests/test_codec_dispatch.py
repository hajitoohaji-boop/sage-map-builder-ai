import pytest

from sage_map_builder.formats.codec_dispatch import dispatch


class DummyCodec:
    def decode(self, payload: bytes):
        return payload

    def encode(self, value):
        return value


def test_verified_waypoints_can_dispatch():
    result = dispatch(DummyCodec(), "WaypointsList", 1)
    assert result.label == "WaypointsList"


def test_unverified_chunk_cannot_dispatch():
    with pytest.raises(ValueError):
        dispatch(DummyCodec(), "HeightMapData", 4)


def test_unknown_chunk_cannot_dispatch():
    with pytest.raises(ValueError):
        dispatch(DummyCodec(), "Unknown", 1)
