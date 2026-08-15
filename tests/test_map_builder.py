import pytest

from sage_map_builder.map.builder import add_asset_object, add_waypoint, build_document
from sage_map_builder.mods.asset_index import build_asset_index
from sage_map_builder.mods.registry import AssetEntry, ModRegistry
from sage_map_builder.planner.mission_plan import MissionPlan, PlayerPlan


def make_index():
    registry = ModRegistry()
    registry.add(AssetEntry("Object", "TankBoss", "test.ini", {"BuildCost": "500"}))
    return build_asset_index(registry)


def make_mission():
    return MissionPlan("Test", [PlayerPlan("Boss", "Boss")])


def test_builder_resolves_only_loaded_assets():
    document = build_document(title="Test", width=256, height=256, mission=make_mission(), asset_index=make_index())
    obj = add_asset_object(document, make_index(), "TankBoss", "Boss", 64, 64)
    assert obj.asset.name == "TankBoss"


def test_builder_rejects_unknown_asset():
    document = build_document(title="Test", width=256, height=256, mission=make_mission(), asset_index=make_index())
    with pytest.raises(KeyError):
        add_asset_object(document, make_index(), "Missing", "Boss", 64, 64)


def test_builder_rolls_back_out_of_bounds_object():
    document = build_document(title="Test", width=256, height=256, mission=make_mission(), asset_index=make_index())
    with pytest.raises(ValueError):
        add_asset_object(document, make_index(), "TankBoss", "Boss", 300, 64)
    assert document.objects == []


def test_waypoint_is_validated():
    document = build_document(title="Test", width=256, height=256, mission=make_mission(), asset_index=make_index())
    add_waypoint(document, "SPAWN", 64, 64)
    assert document.waypoints[0].name == "SPAWN"
