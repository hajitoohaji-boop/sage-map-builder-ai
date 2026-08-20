import pytest

from sage_map_builder.map.document import MapDocument
from sage_map_builder.planner.mission_plan import MissionPlan
from sage_map_builder.planning.map_plan import PlacementIntent
from sage_map_builder.planning.placement_to_document import apply_placements


class FakeIndex:
    def __init__(self, asset):
        self.asset = asset

    def find(self, name):
        return self.asset if name == self.asset.name else None


def test_waypoint_placement_is_applied_without_asset_resolution():
    document = MapDocument("Test", 256, 256, mission=MissionPlan("Test"))
    apply_placements(document, [PlacementIntent("waypoint", "SPAWN", 20, 30)])
    assert document.waypoints[0].name == "SPAWN"


def test_asset_placement_requires_owner():
    document = MapDocument("Test", 256, 256, mission=MissionPlan("Test"))
    with pytest.raises(ValueError, match="owner"):
        apply_placements(document, [PlacementIntent("object", "Tank", 20, 30)])
