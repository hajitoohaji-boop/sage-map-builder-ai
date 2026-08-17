from pathlib import Path
from sage_map_builder.report.compare_report import build_compare_report


def test_compare_report_is_deterministic_and_nonsemantic(tmp_path: Path):
    a = tmp_path / "a.map"
    b = tmp_path / "b.map"
    a.write_bytes(b"EAR\x00abc")
    b.write_bytes(b"EAR\x00axcDEF")
    report = build_compare_report(a, b)
    assert report["comparison"]["common_length"] == 7
    assert report["comparison"]["different_byte_count"] == 1
    assert report["semantic_interpretation"] is None
