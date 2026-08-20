from sage_map_builder.ai.plan_extraction import request_to_plan
from sage_map_builder.ai.request import MapRequest


def test_explicit_dimensions_and_objective():
    plan = request_to_plan(MapRequest("اصنع خريطة 512x256 هدف: الدفاع عن القاعدة"))
    assert plan.intent.width == 512
    assert plan.intent.height == 256
    assert plan.intent.objectives == ["الدفاع عن القاعدة"]


def test_does_not_invent_placements_or_mission_scripts():
    plan = request_to_plan(MapRequest("اصنع خريطة صحراوية"))
    assert plan.placements == []
    assert plan.mission.scripts == []
    assert plan.mission.waves == []
