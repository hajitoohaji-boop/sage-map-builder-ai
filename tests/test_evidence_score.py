from sage_map_builder.formats.evidence_score import EvidenceScore


def test_complete_score_has_four_points():
    score = EvidenceScore(True, True, True, True)
    assert score.points == 4
    assert score.complete


def test_partial_score_is_incomplete():
    score = EvidenceScore(True, True, False, True)
    assert score.points == 3
    assert not score.complete
