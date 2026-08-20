from sage_map_builder.ai.request import MapRequest
from sage_map_builder.ai.request_to_plan import request_to_plan


def test_request_to_plan_applies_explicit_factions_and_objective():
    plan = request_to_plan(MapRequest(
        text="512x256\nfactions: USA, China\nobjective: Destroy bases"
    ))
    assert plan.intent.factions == ["USA", "China"]
    assert plan.intent.objectives == ["Destroy bases"]
    assert plan.mission.objectives == ["Destroy bases"]
    assert plan.placements == []
    assert plan.mission.waves == []


def test_request_to_plan_does_not_infer_mission_from_prose():
    plan = request_to_plan(MapRequest(
        text="American and Chinese forces defend the city with ten waves."
    ))
    assert plan.intent.factions == []
    assert plan.intent.objectives == []
    assert plan.mission.objectives == []
    assert plan.mission.waves == []
