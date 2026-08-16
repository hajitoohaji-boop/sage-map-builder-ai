from sage_map_builder.map.verified_fields import promote_stable_offset


def test_three_identical_samples_can_promote_raw_field():
    samples = [b"EAR\0ABCD", b"EAR\0ABCD", b"EAR\0ABCD"]
    field = promote_stable_offset(samples, 4)
    assert field is not None
    assert field.offset == 4
    assert field.raw_hex == "41 42 43 44"
    assert field.sample_count == 3
    assert field.confidence == "stable_raw_value"


def test_two_samples_are_not_enough_by_default():
    samples = [b"EAR\0ABCD", b"EAR\0ABCD"]
    assert promote_stable_offset(samples, 4) is None


def test_variable_values_are_not_promoted():
    samples = [b"EAR\0ABCD", b"EAR\0WXYZ", b"EAR\0ABCD"]
    assert promote_stable_offset(samples, 4) is None
