from sage_map_builder.analysis.candidate_sections import build_candidates


def test_candidates_use_observed_boundaries_only():
    data = b"AAAAEAR\x00BBBBCCCCKkMpDDDD"
    markers = {"EAR\u0000": [4], "KkMp": [17]}
    sections = build_candidates(data, markers)
    assert sections[0].start == 4
    assert sections[0].end == 17
    assert sections[0].length == 13
    assert sections[0].start_marker == "EAR\u0000"
    assert sections[0].end_marker == "KkMp"
    assert sections[0].confidence == "observed_boundary"
