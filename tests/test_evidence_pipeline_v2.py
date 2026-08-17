from pathlib import Path
from sage_map_builder.pipeline.evidence_pipeline import analyze_samples


def test_pipeline_includes_section_comparison(tmp_path: Path):
    a = tmp_path / "a.map"
    b = tmp_path / "b.map"
    a.write_bytes(b"EAR\x00" + b"a" * 8 + b"CkMp" + b"1")
    b.write_bytes(b"EAR\x00" + b"b" * 8 + b"CkMp" + b"2")
    result = analyze_samples([a, b])
    assert result["schema_version"] == 2
    assert result["section_comparison"]
    assert result["section_comparison"][0]["same_boundary_markers"]
    assert result["section_comparison"][0]["semantic_interpretation"] is None


def test_pipeline_rejects_empty_input():
    try:
        analyze_samples([])
    except ValueError:
        return
    raise AssertionError("empty sample list must be rejected")
