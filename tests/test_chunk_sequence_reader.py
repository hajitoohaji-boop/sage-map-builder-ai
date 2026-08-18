import pytest
from sage_map_builder.formats.chunk_sequence_reader import read_sequence
from sage_map_builder.formats.chunk_envelope import ChunkEnvelope


def test_read_sequence_reads_multiple_chunks():
    data = ChunkEnvelope(1, b"a").encode() + ChunkEnvelope(2, b"bc").encode()
    chunks = read_sequence(data)
    assert [(c.header.version, c.payload) for c in chunks] == [(1, b"a"), (2, b"bc")]
    assert chunks[-1].end == len(data)


def test_read_sequence_is_bounded():
    data = ChunkEnvelope(1, b"abcd").encode()
    with pytest.raises(ValueError):
        read_sequence(data, end=6)


def test_read_sequence_rejects_trailing_partial_header():
    data = ChunkEnvelope(1, b"a").encode() + b"\x01\x00"
    with pytest.raises(ValueError):
        read_sequence(data)
