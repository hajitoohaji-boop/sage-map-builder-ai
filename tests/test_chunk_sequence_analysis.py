import pytest

from sage_map_builder.formats.chunk_sequence_analysis import analyze_sequence
from sage_map_builder.formats.data_chunk import DataChunkHeader


def test_analyze_sequence_preserves_chunk_headers_and_sizes():
    data = DataChunkHeader(4, 3).pack() + b"abc" + DataChunkHeader(7, 2).pack() + b"xy"
    result = analyze_sequence(data, 0, len(data))
    assert result.versions == (4, 7)
    assert result.payload_sizes == (3, 2)
    assert len(result.chunks) == 2


def test_analyze_sequence_rejects_truncated_chunk():
    data = DataChunkHeader(4, 4).pack() + b"abc"
    with pytest.raises(ValueError):
        analyze_sequence(data, 0, len(data))
