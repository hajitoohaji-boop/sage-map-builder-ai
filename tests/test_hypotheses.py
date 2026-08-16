from sage_map_builder.map.hypotheses import generate_candidates


def test_candidates_are_not_auto_verified():
    left = [{"offset": 0, "raw_hex": "45 41 52 00", "little_u32": 0x00524145}]
    right = [{"offset": 0, "raw_hex": "45 41 52 00", "little_u32": 0x00524145}]
    result = generate_candidates(left, right)
    assert len(result) == 1
    assert result[0].status == "candidate"
    assert "same raw bytes" in result[0].reason
