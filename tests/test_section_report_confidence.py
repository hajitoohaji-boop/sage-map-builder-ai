from sage_map_builder.map.section_report import build_report


def test_report_contains_confidence_for_common_sections():
    data = b"AAAA" + b"shared-section" + b"BBBB"
    other = b"AAAA" + b"shared-section" + b"CCCC"
    report = build_report(data, "sample.map", comparison=other)
    assert len(report.common_sections) == len(report.section_confidence)
    assert report.section_confidence
    assert report.section_confidence[0]["score"] == 0.35
