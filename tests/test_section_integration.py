from sage_map_builder.map.sections import common_byte_runs, marker_ranges


def test_common_byte_runs_ignores_short_runs():
    assert common_byte_runs(b"ABxxCCCC", b"AByyCCCC", min_length=4) == ()


def test_common_byte_runs_reports_long_run():
    runs = common_byte_runs(b"1234ABCD", b"9999ABCD", min_length=4)
    assert len(runs) == 1
    assert runs[0].start == 4
    assert runs[0].end == 8


def test_marker_ranges():
    assert marker_ranges(b"CkMp--CkMp", b"CkMp") == (0, 6)
