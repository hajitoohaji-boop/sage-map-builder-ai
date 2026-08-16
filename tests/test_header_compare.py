from sage_map_builder.map.header_compare import compare_headers


def test_header_comparison_keeps_semantics_conservative():
    left = b"EAR\0" + b"x" * 8 + b"CkMp" + b"a" * 4
    right = b"EAR\0" + b"y" * 8 + b"CkMp" + b"b" * 12
    result = compare_headers(left, right)
    assert result.same_magic is True
    assert result.same_ckmp_offsets is True
    assert result.size_difference == 8
