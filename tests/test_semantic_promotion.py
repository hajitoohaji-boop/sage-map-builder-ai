from sage_map_builder.map.semantic_promotion import promote_dimension


def test_stable_dimension_is_only_a_candidate():
    samples = [b"EAR\0" + (128).to_bytes(4, "little")] * 3
    result = promote_dimension(samples, 4)
    assert result is not None
    assert result.value == 128
    assert result.status == "candidate"
    assert "semantic role remains unproven" in result.reason


def test_non_dimension_is_rejected():
    samples = [b"EAR\0" + (130).to_bytes(4, "little")] * 3
    result = promote_dimension(samples, 4)
    assert result is not None
    assert result.status == "rejected"


def test_insufficient_samples_do_not_promote():
    samples = [b"EAR\0" + (128).to_bytes(4, "little")] * 2
    assert promote_dimension(samples, 4) is None
