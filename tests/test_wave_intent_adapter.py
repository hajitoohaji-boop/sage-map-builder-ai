import pytest

from sage_map_builder.planner.mission_plan import MissionPlan, PlayerPlan
from sage_map_builder.planning.wave_intent_adapter import wave_intent_to_plan


def mission() -> MissionPlan:
    return MissionPlan(title="Test", players=[PlayerPlan("USA", "America")])


def test_converts_only_explicit_wave_fields():
    plan = wave_intent_to_plan(
        mission(),
        [{"owner": "USA", "units": ["Tank_A"], "delay_seconds": 90}],
    )
    assert plan.waves[0].owner == "USA"
    assert plan.waves[0].units == ("Tank_A",)
    assert plan.waves[0].delay_seconds == 90


def test_missing_delay_is_rejected():
    with pytest.raises(ValueError, match="delay_seconds"):
        wave_intent_to_plan(mission(), [{"owner": "USA", "units": ["Tank_A"]}])


def test_unknown_owner_is_rejected_by_mission_validation():
    with pytest.raises(ValueError, match="unknown wave owner"):
        wave_intent_to_plan(
            mission(),
            [{"owner": "China", "units": ["Tank_A"], "delay_seconds": 90}],
        )
