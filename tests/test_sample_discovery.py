from sage_map_builder.pipeline.sample_discovery import discover_maps


def test_discovery_finds_and_validates_maps(tmp_path):
    (tmp_path / "good.map").write_bytes(b"EAR\0data")
    (tmp_path / "bad.map").write_bytes(b"NOPEdata")
    (tmp_path / "ignore.txt").write_bytes(b"EAR\0data")
    result = discover_maps(tmp_path)
    assert [item.path.split('/')[-1] for item in result] == ["bad.map", "good.map"]
    assert result[0].valid_magic is False
    assert result[1].valid_magic is True
