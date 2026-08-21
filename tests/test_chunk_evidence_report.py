from sage_map_builder.formats.chunk_sequence_reader import RawChunk
from sage_map_builder.formats.data_chunk import DataChunkHeader
from sage_map_builder.formats.chunk_evidence_report import build_evidence_report


def test_evidence_report_is_lossless_for_observed_metadata():
    chunks = (
        RawChunk(DataChunkHeader(4, 3), b"abc"),
        RawChunk(DataChunkHeader(7, 2), b"xy"),
        RawChunk(DataChunkHeader(4, 3), b"def"),
    )
    report = build_evidence_report(chunks, prefix_size=2)
    assert report.count == 3
    assert report.versions == ((4, 2), (7, 1))
    assert report.sizes == ((2, 1), (3, 2))
    assert report.chunks[0].payload_prefix == b"ab"
    assert report.chunks[2].payload_prefix == b"de"
