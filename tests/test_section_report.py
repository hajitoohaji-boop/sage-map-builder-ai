import json

from sage_map_builder.map.section_report import build_report, write_report


def test_build_report_contains_probe_and_marker_data(tmp_path):
    data = b"EAR\0" + b"x" * 8 + b"CkMp" + b"y" * 8
    report = build_report(data, "sample.map")
    assert report.size == len(data)
    assert report.magic_hex == "45 41 52 00"
    assert report.markers["CkMp"] == (12,)
    assert len(report.sha256) == 64

    output = tmp_path / "report.json"
    write_report(report, output)
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["file"] == "sample.map"
    assert payload["markers"]["CkMp"] == [12]


def test_build_report_records_common_sections():
    left = b"AAAA" + b"COMMON_SECTION" + b"LEFT"
    right = b"BBBB" + b"COMMON_SECTION" + b"RIGHT"
    report = build_report(left, "left.map", comparison=right)
    assert report.common_sections
    assert report.common_sections[0]["start"] == 4
