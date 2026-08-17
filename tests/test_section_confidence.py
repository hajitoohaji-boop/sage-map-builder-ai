import pytest
from sage_map_builder.map.section_confidence import score_candidate


def test_confidence_is_evidence_only():
    result = score_candidate(10, 20, shared_offset=True, marker_nearby=True, source_supported=True)
    assert result.score == 1.0
    assert len(result.evidence) == 3


def test_invalid_range_rejected():
    with pytest.raises(ValueError):
        score_candidate(20, 20)
