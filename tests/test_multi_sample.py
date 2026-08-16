from sage_map_builder.map.multi_sample import consensus_for_offset, stable_offsets


def test_three_samples_can_confirm_stability():
    samples = [b"EAR\0ABCD", b"EAR\0ABCD", b"EAR\0ABCD"]
    result = consensus_for_offset(samples, 4)
    assert result.samples == 3
    assert result.distinct_raw_values == 1
    assert result.status == "stable"


def test_variation_is_not_verified():
    samples = [b"EAR\0ABCD", b"EAR\0WXYZ", b"EAR\0ABCD"]
    result = consensus_for_offset(samples, 4)
    assert result.status == "variable"
    assert stable_offsets(samples, [4]) == ()
