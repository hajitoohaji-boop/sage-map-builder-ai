from sage_map_builder.formats.codec_matrix import build_codec_matrix


def test_waypoints_can_be_marked_verified_without_promoting_other_chunks():
    matrix = build_codec_matrix(("WaypointsList",))
    waypoint = [x for x in matrix if x.label == "WaypointsList"]
    assert waypoint
    assert all(x.status == "verified" for x in waypoint)
    assert any(x.status == "opaque" for x in matrix if x.label != "WaypointsList")
