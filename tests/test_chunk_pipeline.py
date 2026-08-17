from sage_map_builder.map.chunk_pipeline import probe_map_bytes


def test_chunk_pipeline_preserves_reader_and_probes():
    data = b"CkMp" + b"\x00" * 12
    result = probe_map_bytes(data)
    assert result.reader.data == data
    assert isinstance(result.probes, tuple)
