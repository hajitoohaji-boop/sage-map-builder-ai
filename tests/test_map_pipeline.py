from sage_map_builder.map.pipeline import common_canonical_offsets, probe_bytes


def test_probe_detects_magic_and_marker():
    data = b"EAR\0" + b"x" * 8 + b"CkMp" + b"y" * 4
    result = probe_bytes(data)
    assert result.evidence.magic == b"EAR\0"
    assert result.evidence.ckmP_offsets == (12,)


def test_common_offsets_are_intersection():
    a = probe_bytes(b"CkMp" + b"a" * 4 + b"CkMp")
    b = probe_bytes(b"CkMp" + b"b" * 4 + b"CkMp")
    assert common_canonical_offsets(a, b) == (0, 8)


def test_empty_map_is_rejected():
    try:
        probe_bytes(b"")
    except ValueError:
        return
    raise AssertionError("empty map should be rejected")
