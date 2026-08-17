from sage_map_builder.planning.map_plan import MapGenerationPlan, MapIntent, PlacementIntent
from sage_map_builder.planning.plan_validator import validate_plan


def test_validator_detects_duplicate_and_out_of_bounds():
    plan = MapGenerationPlan(MapIntent(width=64, height=64), [
        PlacementIntent("object", "A", 10, 10),
        PlacementIntent("object", "A", 10, 10),
        PlacementIntent("object", "B", 100, 10),
    ])
    issues = validate_plan(plan)
    codes = {issue.code for issue in issues}
    assert "DUPLICATE_PLACEMENT" in codes
    assert "OUT_OF_BOUNDS" in codes


def test_validator_reports_unresolved_as_warning():
    plan = MapGenerationPlan(MapIntent(width=64, height=64), unresolved=["unknown unit"])
    issues = validate_plan(plan)
    assert any(i.code == "UNRESOLVED" and i.level == "warning" for i in issues)
