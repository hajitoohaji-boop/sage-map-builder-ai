from sage_map_builder.formats.chunk_envelope import ChunkEnvelope
from sage_map_builder.formats.chunk_sequence_reader import read_sequence
from sage_map_builder.formats.chunk_sequence_writer import write_sequence


def test_sequence_writer_round_trip():
    original = ChunkEnvelope(3, b"abc") .encode() + ChunkEnvelope(7, b"xyz").encode()
    chunks = read_sequence(original)
    assert write_sequence(chunks) == original
