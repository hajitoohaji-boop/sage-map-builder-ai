from sage_map_builder.formats.evidence_pairing import Observation, pair


def test_pair_matches_label_and_version():
    left = (Observation("a.map", "HeightMapData", 4, 10, 20), Observation("a.map", "WaypointsList", 1, 30, 40))
    right = (Observation("b.map", "HeightMapData", 4, 100, 200),)
    result = pair(left, right)
    assert len(result) == 1
    assert result[0].left.start == 10
    assert result[0].right.start == 100
