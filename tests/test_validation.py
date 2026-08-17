from sage_map_builder.model.map_document import MapDocument
from sage_map_builder.model.validation import validate_document


def test_validation_detects_dangling_script_references():
    doc = MapDocument("x.map", 0)
    doc.waypoints.append({"name": "SPAWN", "x": 1, "y": 2, "z": 0})
    doc.scripts.append({"name": "WAVE", "enabled": True, "conditions": [], "actions": [{"kind": "spawn_team", "args": {"waypoint": "MISSING"}}]})
    issues = validate_document(doc)
    assert any(i.code == "UNKNOWN_WAYPOINT" for i in issues)


def test_validation_accepts_existing_waypoint_reference():
    doc = MapDocument("x.map", 0)
    doc.waypoints.append({"name": "SPAWN", "x": 1, "y": 2, "z": 0})
    doc.scripts.append({"name": "WAVE", "enabled": True, "conditions": [], "actions": [{"kind": "spawn_team", "args": {"waypoint": "SPAWN"}}]})
    assert validate_document(doc) == ()
