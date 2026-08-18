from sage_map_builder.analysis.chunk_stream_probe import probe_chunk_stream
from sage_map_builder.formats.data_chunk import DataChunkHeader


def test_probe_valid_contiguous_stream():
    raw = (
        DataChunkHeader(version=4, data_size=2).pack()
        + b"AB"
        + DataChunkHeader(version=7, data_size=0).pack()
    )
    result = probe_chunk_stream(raw, 0, len(raw))
    assert result.valid is True
    assert result.chunk_count == 2
    assert result.versions == (4, 7)
    assert result.payload_sizes == (2, 0)


def test_probe_rejects_truncated_region_without_throwing():
    raw = DataChunkHeader(version=4, data_size=10).pack() + b"x"
    result = probe_chunk_stream(raw, 0, len(raw))
    assert result.valid is False
    assert result.error


def test_probe_respects_caller_boundaries():
    raw = DataChunkHeader(version=1, data_size=2).pack() + b"AB" + b"TAIL"
    result = probe_chunk_stream(raw, 0, 6)
    assert result.valid is True
    assert result.chunk_count == 1
    assert result.payload_sizes == (2,)
