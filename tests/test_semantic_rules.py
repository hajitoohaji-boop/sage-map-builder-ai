from sage_map_builder.map.semantic_rules import check_dimension, check_dimension_pair


def test_supported_dimension_is_only_plausible():
    result = check_dimension(128)
    assert result.status == "supported"
    assert "plausibility" not in result.reason


def test_invalid_dimension_rejected():
    assert check_dimension(130).status == "rejected"
    assert check_dimension(1024).status == "rejected"


def test_dimension_pair():
    assert check_dimension_pair(128, 256).status == "supported"
    assert check_dimension_pair(128, 130).status == "rejected"
