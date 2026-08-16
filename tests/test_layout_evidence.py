from sage_map_builder.map.layout_evidence import evaluate_layout


def test_layout_that_fits_is_only_a_candidate():
    result = evaluate_layout(128, 256, 4, 128 * 256 * 4)
    assert result.status == "candidate"
    assert result.cells == 32768
    assert result.expected_bytes == 131072


def test_layout_exceeding_region_is_rejected():
    result = evaluate_layout(128, 256, 4, 100)
    assert result.status == "rejected"


def test_invalid_layout_is_rejected():
    assert evaluate_layout(0, 256, 4, 1000).status == "rejected"
