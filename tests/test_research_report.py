from sage_map_builder.map.research_report import build_research_report


def test_research_report_combines_evidence():
    left = b"EAR\0" + b"A" * 8 + b"CkMp" + b"COMMON-SECTION" + b"L"
    right = b"EAR\0" + b"B" * 8 + b"CkMp" + b"COMMON-SECTION" + b"R"
    report = build_research_report(left, right, "left.map", "right.map")
    assert report.left["file"] == "left.map"
    assert report.right["file"] == "right.map"
    assert report.header["same_magic"] is True
    assert report.header["left_ckmp_offsets"] == [12]
    assert report.header["right_ckmp_offsets"] == [12]
    assert report.header["word_comparison"]
    assert report.common_sections
