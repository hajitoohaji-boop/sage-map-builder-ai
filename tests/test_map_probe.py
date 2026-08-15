from sage_map_builder.analysis import probe_map


def test_probe_reports_size_and_prefix() -> None:
    data = b"EAR\x00\x01Waypoint"
    result = probe_map(data)
    assert result.file_size == len(data)
    assert result.prefix_hex.startswith("45 41 52 00")
    assert "EAR" in result.ascii_tokens
    assert "Waypoint" in result.ascii_tokens


def test_probe_does_not_require_a_known_map_signature() -> None:
    data = b"not a verified format"
    result = probe_map(data)
    assert result.file_size == len(data)
    assert "not a verified format" in result.ascii_tokens
