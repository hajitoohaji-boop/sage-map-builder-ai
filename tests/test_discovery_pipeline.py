from sage_map_builder.pipeline.discovery_pipeline import analyze_directory


def test_directory_pipeline_analyzes_valid_maps_and_skips_invalid(tmp_path):
    (tmp_path / "one.map").write_bytes(b"EAR\0" + b"a" * 20)
    (tmp_path / "two.map").write_bytes(b"EAR\0" + b"b" * 20)
    (tmp_path / "bad.map").write_bytes(b"NOPE" + b"c" * 20)
    result = analyze_directory(tmp_path)
    assert result["sample_count"] == 2
    assert len(result["reports"]) == 2
    assert len(result["skipped"]) == 1
    assert result["skipped"][0]["reason"] == "invalid_magic"
