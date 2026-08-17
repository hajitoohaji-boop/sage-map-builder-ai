from sage_map_builder.analysis.section_compare import compare_candidate_sections


def test_section_compare_keeps_semantics_unknown():
    left = b"EAR\x00" + b"a" * 8 + b"CkMp" + b"z"
    right = b"EAR\x00" + b"b" * 8 + b"CkMp" + b"q"
    markers = {"EAR\u0000": [0], "CkMp": [12]}
    rows = compare_candidate_sections(left, markers, right, markers)
    assert rows
    assert rows[0]["same_length"]
    assert rows[0]["same_boundary_markers"]
    assert rows[0]["same_hash"] is False
    assert rows[0]["semantic_interpretation"] is None
