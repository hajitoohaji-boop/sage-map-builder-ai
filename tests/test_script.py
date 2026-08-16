import pytest
from sage_map_builder.model.map_document import MapDocument
from sage_map_builder.model.script import MapScript, ScriptAction, add_script, remove_script


def test_add_script_with_conditions_and_actions():
    doc = MapDocument("mission.map", 0)
    script = MapScript(
        "WAVE_1",
        conditions=[ScriptAction("timer_expired", {"timer": "WAVE", "seconds": 90})],
        actions=[ScriptAction("spawn_team", {"team": "team0001", "waypoint": "SPAWN"})],
    )
    add_script(doc, script)
    assert doc.scripts[0]["name"] == "WAVE_1"
    assert doc.scripts[0]["actions"][0]["kind"] == "spawn_team"


def test_duplicate_script_is_rejected():
    doc = MapDocument("mission.map", 0)
    add_script(doc, MapScript("WAVE_1"))
    with pytest.raises(ValueError):
        add_script(doc, MapScript("WAVE_1"))


def test_remove_script():
    doc = MapDocument("mission.map", 0)
    add_script(doc, MapScript("WAVE_1"))
    remove_script(doc, "WAVE_1")
    assert doc.scripts == []
