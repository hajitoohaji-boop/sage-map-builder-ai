import pytest
from sage_map_builder.formats.waypoints_chunk import WaypointLink, encode_waypoint_links, decode_waypoint_links


def test_waypoint_links_round_trip():
    links = [WaypointLink(2, 7), WaypointLink(7, 9)]
    assert decode_waypoint_links(encode_waypoint_links(links)) == links


def test_waypoint_links_reject_bad_length():
    with pytest.raises(ValueError):
        decode_waypoint_links(b"\x01\x00\x00\x00\x01")
