from sage_map_builder.map.region_detection import bounded_regions, marker_regions


def test_marker_regions_are_bounded_by_next_marker_or_eof():
    data = b"AAAA" + b"CkMp" + b"1234" + b"CkMp" + b"5678"
    regions = marker_regions(data)
    assert [(r.start, r.end) for r in regions] == [(4, 12), (12, len(data))]


def test_no_marker_returns_no_marker_regions():
    assert marker_regions(b"AAAA") == ()


def test_bounded_regions_are_sorted_and_deduplicated():
    regions = bounded_regions(b"abcdefghij", [8, 4, 4])
    assert [(r.start, r.end) for r in regions] == [(0, 4), (4, 8), (8, 10)]
