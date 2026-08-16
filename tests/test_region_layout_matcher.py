from sage_map_builder.map.region_detection import ByteRegion
from sage_map_builder.map.region_layout_matcher import match_region, rank_matches


def test_region_match_records_remaining_bytes():
    region = ByteRegion(10, 10 + 128 * 256 * 4, "test")
    result = match_region(region, 128, 256, 4)
    assert result.status == "candidate"
    assert result.expected_bytes == region.size
    assert result.remaining_bytes == 0


def test_rank_prefers_fitting_candidates():
    region = ByteRegion(0, 128 * 256 * 4, "test")
    matches = rank_matches((region,), ((64, 64), (128, 256)), 4)
    assert matches[0].width == 128
    assert matches[0].height == 256
