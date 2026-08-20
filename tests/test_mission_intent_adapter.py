from sage_map_builder.planning.map_plan import MissionIntent
from sage_map_builder.planning.mission_intent_adapter import mission_intent_to_plan


def test_adapter_preserves_explicit_objectives():
    intent = MissionIntent(
        objectives=["Destroy enemy bases"],
        scripts=[{"name": "WAVE"}],
        waves=[{"owner": "Enemy", "units": ["Tank"]}],
    )
    plan = mission_intent_to_plan(intent, title="Test Mission")
    assert plan.title == "Test Mission"
    assert plan.objectives == ["Destroy enemy bases"]
    assert plan.bases == []
    assert plan.waves == []


def test_empty_intent_is_valid():
    plan = mission_intent_to_plan(MissionIntent())
    assert plan.objectives == []
