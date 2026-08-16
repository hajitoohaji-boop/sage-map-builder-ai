import pytest
from sage_map_builder.model.map_document import MapDocument, MapDimensions
from sage_map_builder.model.waypoint import Waypoint
from sage_map_builder.model.waypoint_store import add_waypoint, remove_waypoint


def test_add_and_remove_waypoint():
    doc = MapDocument("x.map", 0, MapDimensions(128, 128))
    add_waypoint(doc, Waypoint("SPAWN", 20, 30, 5))
    assert doc.waypoints == [{"name": "SPAWN", "x": 20, "y": 30, "z": 5}]
    remove_waypoint(doc, "SPAWN")
    assert doc.waypoints == []


def test_duplicate_name_is_rejected():
    doc = MapDocument("x.map", 0, MapDimensions(128, 128))
    add_waypoint(doc, Waypoint("SPAWN", 20, 30))
    with pytest.raises(ValueError):
        add_waypoint(doc, Waypoint("SPAWN", 40, 50))


def test_out_of_bounds_waypoint_is_rejected():
    doc = MapDocument("x.map", 0, MapDimensions(128, 128))
    with pytest.raises(ValueError):
        add_waypoint(doc, Waypoint("SPAWN", 129, 50))
