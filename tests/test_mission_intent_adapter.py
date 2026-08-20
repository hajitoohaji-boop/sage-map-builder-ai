from sage_map_builder.planning.map_plan import MissionIntent
from sage_map_builder.planning.mission_intent_adapter import mission_intent_to_plan


def test_adapter_preserves_explicit_objectives_and_players():
    intent = MissionIntent(
        objectives=["Destroy enemy bases"],
        players=[("USA", "America"), ("China", "China")],
    )
    plan = mission_intent_to_plan(intent, title="Test Mission")
    assert plan.title == "Test Mission"
    assert plan.objectives == ["Destroy enemy bases"]
    assert [(p.name, p.faction) for p in plan.players] == [("USA", "America"), ("China", "China")]
    assert plan.bases == []
    assert plan.waves == []
