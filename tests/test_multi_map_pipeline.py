from sage_map_builder.pipeline.multi_map_pipeline import analyze_two_maps


def test_two_map_pipeline_returns_both_reports(tmp_path):
    left = tmp_path / "left.map"
    right = tmp_path / "right.map"
    left.write_bytes(b"EAR\0" + b"x" * 12 + b"CkMp" + b"left")
    right.write_bytes(b"EAR\0" + b"y" * 12 + b"CkMp" + b"right")
    result = analyze_two_maps(left, right)
    assert result["schema_version"] == 1
    assert result["left_section_report"]["file"] == "left.map"
    assert result["right_section_report"]["file"] == "right.map"
    assert "research_report" in result
