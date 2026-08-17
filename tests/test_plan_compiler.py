import pytest

from sage_map_builder.mods.asset_index import AssetIndex
from sage_map_builder.mods.assets import NormalizedAsset
from sage_map_builder.planner.mission_plan import MissionPlan, PlayerPlan
from sage_map_builder.planning.compiler import PlanCompileError, compile_plan
from sage_map_builder.planning.map_plan import MapGenerationPlan, MapIntent, PlacementIntent


def test_compile_plan_resolves_real_asset_and_waypoint():
    assets = AssetIndex((NormalizedAsset("TankBoss", "vehicle", "test.ini", {}),))
    mission = MissionPlan("Test", players=[PlayerPlan("Player", "USA")])
    plan = MapGenerationPlan(
        MapIntent(title="Test", width=128, height=128),
        placements=[
            PlacementIntent("vehicle", "TankBoss", 32, 32, owner="Player"),
            PlacementIntent("waypoint", "SPAWN", 64, 64),
        ],
    )
    document = compile_plan(plan, asset_index=assets, mission=mission)
    assert len(document.objects) == 1
    assert document.objects[0].asset.name == "TankBoss"
    assert document.waypoints[0].name == "SPAWN"


def test_compile_plan_rejects_missing_owner_instead_of_inventing_one():
    assets = AssetIndex((NormalizedAsset("TankBoss", "vehicle", "test.ini", {}),))
    mission = MissionPlan("Test", players=[PlayerPlan("Player", "USA")])
    plan = MapGenerationPlan(
        MapIntent(title="Test", width=128, height=128),
        placements=[PlacementIntent("vehicle", "TankBoss", 32, 32)],
    )
    with pytest.raises(PlanCompileError, match="owner is required"):
        compile_plan(plan, asset_index=assets, mission=mission)
