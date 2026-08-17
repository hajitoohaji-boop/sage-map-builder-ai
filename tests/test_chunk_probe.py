from sage_map_builder.formats.chunk_probe import probe_region, probe_regions


def test_probe_valid_region():
    data = b"\x01\x00\x03\x00abcTAIL"
    p = probe_region(data, 0, 7)
    assert p.version == 1
    assert p.data_size == 3
    assert p.payload_end == 7
    assert p.valid is True


def test_probe_does_not_cross_region_boundary():
    data = b"\x01\x00\x05\x00abc"
    p = probe_region(data, 0, len(data))
    assert p.valid is False


def test_probe_multiple_regions():
    data = b"\x01\x00\x00\x00\x02\x00\x01\x00x"
    result = probe_regions(data, [(0, 4), (4, 9)])
    assert len(result) == 2
    assert result[1].valid is True
