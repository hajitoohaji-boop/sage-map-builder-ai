from sage_map_builder.analysis import scan_markers


def test_scanner_reports_known_markers_in_offset_order() -> None:
    data = b"xxCkMpyyGlobalLightingzz"
    hits = scan_markers(data)
    assert [(hit.marker, hit.offset) for hit in hits] == [
        (b"CkMp", 2),
        (b"GlobalLighting", 10),
    ]


def test_scanner_allows_multiple_occurrences() -> None:
    data = b"CkMp---CkMp"
    hits = scan_markers(data)
    assert [hit.offset for hit in hits if hit.marker == b"CkMp"] == [0, 7]
