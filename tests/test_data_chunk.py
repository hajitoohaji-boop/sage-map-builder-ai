import struct
import pytest
from sage_map_builder.formats.data_chunk import DataChunkHeader, read_chunk


def test_data_chunk_round_trip():
    header = DataChunkHeader(0x12345678, 1, 4)
    raw = header.pack() + b"TEST"
    parsed, payload, end = read_chunk(raw)
    assert parsed == header
    assert payload == b"TEST"
    assert end == len(raw)


def test_data_chunk_rejects_truncated_header():
    with pytest.raises(ValueError):
        DataChunkHeader.unpack(b"123")


def test_data_chunk_rejects_truncated_payload():
    raw = struct.pack("<IHH", 1, 1, 10) + b"x"
    with pytest.raises(ValueError):
        read_chunk(raw)
