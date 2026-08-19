import pytest
from sage_map_builder.map.source_evidence import classify_observation


def test_classify_observation_keeps_bounds_and_source_fact():
    item = classify_observation(10, 30, "WaypointsList", 1)
    assert item.offset == 10
    assert item.end == 30
    assert item.source is not None
    assert item.source.source_verified is True


def test_classify_observation_unknown_remains_unverified():
    item = classify_observation(10, 30, "Unknown", 1)
    assert item.source is None


def test_classify_observation_rejects_bad_bounds():
    with pytest.raises(ValueError):
        classify_observation(30, 10, "WaypointsList", 1)
