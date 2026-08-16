from sage_map_builder.map.dimension_pair import evaluate_dimension_pair


def test_valid_pair_is_only_a_candidate():
    result = evaluate_dimension_pair(8, 12, 128, 256)
    assert result.status == "candidate"
    assert "not yet proven" in result.reason


def test_same_offset_is_rejected():
    assert evaluate_dimension_pair(8, 8, 128, 256).status == "rejected"


def test_invalid_pair_is_rejected():
    assert evaluate_dimension_pair(8, 12, 128, 130).status == "rejected"
