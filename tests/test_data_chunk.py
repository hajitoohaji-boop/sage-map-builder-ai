import pytest

from sage_map_builder.formats.data_chunk import DataChunkHeader, read_chunk


def test_data_chunk_round_trip():
    header = DataChunkHeader(version=1, data_size=4)
    raw = header.pack() + b"TEST"
    parsed, payload, end = read_chunk(raw)
    assert parsed == header
    assert payload == b"TEST"
    assert end == len(raw)


def test_data_chunk_round_trip_max_uint16_values():
    header = DataChunkHeader(version=0xFFFF, data_size=0xFFFF)
    assert DataChunkHeader.unpack(header.pack()) == header


def test_data_chunk_rejects_truncated_header():
    with pytest.raises(ValueError):
        DataChunkHeader.unpack(b"123")


def test_data_chunk_rejects_truncated_payload():
    raw = DataChunkHeader(version=1, data_size=10).pack() + b"x"
    with pytest.raises(ValueError):
        read_chunk(raw)


def test_data_chunk_rejects_values_outside_uint16():
    with pytest.raises(ValueError):
        DataChunkHeader(version=0x10000, data_size=0).pack()
    with pytest.raises(ValueError):
        DataChunkHeader(version=0, data_size=0x10000).pack()
