from sage_map_builder.map.sections import common_byte_runs, marker_ranges


def test_common_byte_runs_finds_only_identical_offset_runs():
    left = b"AAAA12345678BBBB"
    right = b"AAAA12345678CCCC"
    runs = common_byte_runs(left, right, min_length=4)
    assert [(r.start, r.end) for r in runs] == [(0, 12)]


def test_marker_ranges_finds_overlapping_occurrences():
    assert marker_ranges(b"CkMp--CkMp", b"CkMp") == (0, 6)
