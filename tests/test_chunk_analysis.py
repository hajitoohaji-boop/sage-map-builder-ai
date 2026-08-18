import pytest
from sage_map_builder.formats.chunk_envelope import ChunkEnvelope
from sage_map_builder.map.chunk_analysis import analyze_region, identify_chunk


def test_analyze_region_is_bounded_and_lossless():
    data = ChunkEnvelope(1, b"abc").encode() + ChunkEnvelope(2, b"de").encode()
    result = analyze_region(data, 0, len(data))
    assert len(result.chunks) == 2
    assert result.payload_size == 5
    assert result.chunks[0].payload == b"abc"
    assert result.chunks[1].payload == b"de"


def test_identity_requires_explicit_label():
    data = ChunkEnvelope(1, b"x").encode()
    chunk = analyze_region(data, 0, len(data)).chunks[0]
    with pytest.raises(ValueError):
        identify_chunk(chunk, "")
