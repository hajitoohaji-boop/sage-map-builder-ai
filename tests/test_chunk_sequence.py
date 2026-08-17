import pytest

from sage_map_builder.formats.chunk_sequence import read_chunk_sequence, write_chunk_sequence
from sage_map_builder.formats.data_chunk import DataChunkHeader


def test_opaque_chunk_sequence_round_trip():
    first = DataChunkHeader(0x11111111, 1, 3).pack() + b"abc"
    second = DataChunkHeader(0x22222222, 7, 0).pack()
    raw = first + second
    chunks = read_chunk_sequence(raw)
    assert len(chunks) == 2
    assert chunks[0].payload == b"abc"
    assert chunks[1].payload == b""
    assert write_chunk_sequence(chunks) == raw


def test_chunk_sequence_rejects_truncation():
    raw = DataChunkHeader(1, 1, 4).pack() + b"x"
    with pytest.raises(ValueError):
        read_chunk_sequence(raw)


def test_chunk_sequence_preserves_unknown_payload():
    raw = DataChunkHeader(9, 2, 5).pack() + b"\x00\xffabc"
    chunk = read_chunk_sequence(raw)[0]
    assert chunk.payload == b"\x00\xffabc"
    assert write_chunk_sequence((chunk,)) == raw
