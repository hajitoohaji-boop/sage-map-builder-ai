from sage_map_builder.planning.map_plan import MapGenerationPlan, MapIntent, PlacementIntent
from sage_map_builder.planning.placement_resolver import resolve_plan_placements


def test_waypoints_do_not_require_mod_assets():
    plan = MapGenerationPlan(
        intent=MapIntent(),
        placements=[PlacementIntent(kind="waypoint", template="SPAWN", x=10, y=20)],
    )
    class EmptyIndex:
        def find(self, name):
            return None
    assert resolve_plan_placements(plan, EmptyIndex()) is plan


def test_unknown_asset_is_recorded_as_unresolved():
    plan = MapGenerationPlan(
        intent=MapIntent(),
        placements=[PlacementIntent(kind="building", template="UnknownBuilding", x=10, y=20, owner="USA")],
    )
    class EmptyIndex:
        def find(self, name):
            return None
    try:
        resolve_plan_placements(plan, EmptyIndex())
    except ValueError as exc:
        assert "UnknownBuilding" in str(exc)
    else:
        raise AssertionError("unknown placement must be rejected")
    assert plan.unresolved == ["placement[0].asset:UnknownBuilding"]
