import pytest

from sage_map_builder.format import build_marker_index


def test_marker_index_is_sorted_by_offset() -> None:
    data = b"AAAAWaypointsListBBBBGlobalLightingCCCC"
    index = build_marker_index(data, (b"GlobalLighting", b"WaypointsList"))
    assert [item.name for item in index.locations] == ["WaypointsList", "GlobalLighting"]
    assert index.first("GlobalLighting") is not None


def test_marker_index_records_multiple_occurrences() -> None:
    data = b"ABCABC"
    index = build_marker_index(data, (b"ABC",))
    assert [item.offset for item in index.locations] == [0, 3]


def test_marker_index_rejects_empty_marker() -> None:
    with pytest.raises(ValueError):
        build_marker_index(b"abc", (b"",))
