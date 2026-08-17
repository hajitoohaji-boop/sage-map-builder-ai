import pytest
from sage_map_builder.planning.map_plan import MapGenerationPlan, MapIntent, PlacementIntent


def test_plan_validates_dimensions():
    plan = MapGenerationPlan(MapIntent(width=256, height=256))
    plan.validate()


def test_plan_rejects_invalid_dimensions():
    with pytest.raises(ValueError):
        MapGenerationPlan(MapIntent(width=250, height=256)).validate()


def test_plan_rejects_unresolved_empty_entry():
    plan = MapGenerationPlan(MapIntent(), unresolved=["   "])
    with pytest.raises(ValueError):
        plan.validate()


def test_plan_contains_placement_and_mission():
    plan = MapGenerationPlan(
        MapIntent(title="Test"),
        placements=[PlacementIntent("object", "KnownTemplate", 10, 20, owner="Player_1")],
    )
    value = plan.to_dict()
    assert value["placements"][0]["template"] == "KnownTemplate"
    assert "mission" in value
