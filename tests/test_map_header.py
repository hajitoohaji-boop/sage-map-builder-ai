from sage_map_builder.format.map_header import inspect_prefix


def test_inspect_prefix_records_only_observed_markers() -> None:
    data = b"EAR" + b"\x00" * 11 + b"CkMp" + b"\x00" * 10 + b"GlobalLighting" + b"x"
    result = inspect_prefix(data)

    assert result.signature == b"EAR"
    assert result.c_kmp_offset == 14
    assert result.global_lighting_offset == 28
    assert result.polygon_triggers_offset is None
    assert result.raw_prefix == data


def test_inspect_prefix_preserves_short_input() -> None:
    data = b"EAR"
    result = inspect_prefix(data)
    assert result.raw_prefix == data
    assert result.c_kmp_offset is None
