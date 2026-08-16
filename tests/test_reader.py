from sage_map_builder.map.reader import MapReader


def test_reader_preserves_bytes_and_exposes_evidence():
    data = b"EAR\0" + b"x" * 12 + b"CkMp" + b"region"
    result = MapReader().read_bytes(data, "sample.map")
    assert result.file_name == "sample.map"
    assert result.data == data
    assert result.header.magic == b"EAR\0"
    assert result.header.ckmP_offsets == (16,)
    assert result.header_words[0].raw_hex == "45 41 52 00"
    assert result.regions[0].start == 0
    assert result.regions[0].end == len(data)
