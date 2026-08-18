import pytest
from sage_map_builder.formats.chunk_envelope import ChunkEnvelope


def test_chunk_envelope_round_trip():
    value = ChunkEnvelope(7, b"payload")
    assert ChunkEnvelope.decode(value.encode()) == value


def test_chunk_envelope_rejects_truncation():
    with pytest.raises(ValueError):
        ChunkEnvelope.decode(b"\x01\x00")


def test_chunk_envelope_respects_region_limit():
    data = ChunkEnvelope(1, b"1234").encode()
    with pytest.raises(ValueError):
        ChunkEnvelope.decode(data, limit=6)
