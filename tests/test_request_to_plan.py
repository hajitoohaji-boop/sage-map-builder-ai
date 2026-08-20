from sage_map_builder.ai.request import MapRequest
from sage_map_builder.ai.request_to_plan import request_to_plan


def test_request_to_plan_preserves_only_explicit_facts():
    plan = request_to_plan(MapRequest("اصنع خريطة صحراوية 512x256"))
    assert plan.intent.width == 512
    assert plan.intent.height == 256
    assert plan.intent.description == "اصنع خريطة صحراوية 512x256"
    assert plan.placements == []
    assert plan.mission.objectives == []
    assert plan.mission.scripts == []
    assert plan.mission.waves == []
    assert plan.unresolved == []


def test_request_to_plan_uses_request_title_hint():
    plan = request_to_plan(MapRequest("Create a map 256x256", hints={"title": "Test"}))
    assert plan.intent.title == "Test"
