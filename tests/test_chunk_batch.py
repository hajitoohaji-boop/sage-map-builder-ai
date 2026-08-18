from sage_map_builder.formats.chunk_batch import IdentifiedChunk, decode_chunks, encode_chunks
from sage_map_builder.formats.chunk_registry import ChunkCodecRegistry, ChunkCodec


def test_batch_unknown_chunks_are_lossless():
    registry = ChunkCodecRegistry()
    chunks = (IdentifiedChunk("Unknown", 1, b"abc"), IdentifiedChunk("Other", 2, b"xyz"))
    decoded = decode_chunks(registry, chunks)
    assert [item.payload for item in decoded] == [b"abc", b"xyz"]
    assert encode_chunks(registry, decoded) == (b"abc", b"xyz")


def test_batch_uses_registered_codec():
    registry = ChunkCodecRegistry()
    registry.register(ChunkCodec("WaypointsList", 1, lambda b: b.decode(), lambda v: v.encode()))
    chunks = (IdentifiedChunk("WaypointsList", 1, b"ok"),)
    decoded = decode_chunks(registry, chunks)
    assert decoded[0].value == "ok"
    assert encode_chunks(registry, decoded) == (b"ok",)
