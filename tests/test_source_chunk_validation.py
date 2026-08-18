import pytest
from sage_map_builder.formats.source_chunk_validation import match_source_chunk, require_source_chunk


def test_source_catalog_matches_waypoints_version_one():
    match = match_source_chunk("WaypointsList", 1)
    assert match is not None
    assert match.verified is True
    assert match.spec.container_order == 7


def test_source_catalog_rejects_version_mismatch():
    with pytest.raises(ValueError):
        require_source_chunk("WaypointsList", 2)


def test_unknown_chunk_is_not_guessed():
    assert match_source_chunk("UnknownChunk", 1) is None
