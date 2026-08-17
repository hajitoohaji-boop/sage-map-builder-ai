from sage_map_builder.map.marker_scan import scan


def test_marker_scan_reports_only_observed_positions():
    data = b"EAR\x00xxxxCkMp\x00xxEAR\x00"
    result = scan(data)
    assert result["markers"]["EAR\u0000"] == [0, 13]
    assert result["markers"]["CkMp"] == [8]
    assert result["size"] == len(data)
    assert len(result["sha256"]) == 64
