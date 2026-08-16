from sage_map_builder.pipeline.map_pipeline import analyze_bytes


def test_analyze_bytes_runs_reader_to_report():
    data = b"EAR\0" + b"x" * 12 + b"CkMp" + b"region"
    report = analyze_bytes(data, "sample.map")
    assert report["schema_version"] == 1
    assert report["file"] == "sample.map"
    assert report["file_size"] == len(data)
    assert report["header"]["ckmp_offsets"] == [16]
