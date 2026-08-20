from sage_map_builder.ai.explicit_facts import apply_explicit_facts
from sage_map_builder.ai.request import MapRequest
from sage_map_builder.ai.plan_extraction import request_to_plan


def test_explicit_factions_and_constraints_only():
    request = MapRequest(text="512x256\nfactions: USA, China\nconstraints: keep bases apart")
    plan = apply_explicit_facts(request_to_plan(request))
    assert plan.intent.factions == ["USA", "China"]
    assert plan.intent.constraints == ["language:en", "keep bases apart"]
    assert plan.placements == []
    assert plan.mission.waves == []


def test_plain_prose_does_not_infer_faction():
    request = MapRequest(text="desert map with American and Chinese forces")
    plan = apply_explicit_facts(request_to_plan(request))
    assert plan.intent.factions == []
