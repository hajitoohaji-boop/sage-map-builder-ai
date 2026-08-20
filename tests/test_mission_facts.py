from sage_map_builder.ai.mission_facts import extract_mission_facts, apply_explicit_mission_facts
from sage_map_builder.planner.mission_plan import MissionPlan


def test_extracts_only_explicit_labeled_mission_fields():
    facts = extract_mission_facts(
        "players: USA, China\nfactions: America, China\nobjective: Destroy bases\n"
    )
    assert facts["players"] == ("USA", "China")
    assert facts["factions"] == ("America", "China")
    assert facts["objectives"] == ("Destroy bases",)
    assert "bases" not in facts


def test_does_not_infer_from_prose():
    facts = extract_mission_facts("American and Chinese forces defend the city with ten waves.")
    assert facts == {}


def test_applies_players_only_when_pairing_is_explicit_and_complete():
    plan = MissionPlan(title="Test")
    apply_explicit_mission_facts(
        plan,
        {"players": ("USA", "China"), "factions": ("America", "China")},
    )
    assert [(p.name, p.faction) for p in plan.players] == [("USA", "America"), ("China", "China")]
