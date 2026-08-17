import pytest
from sage_map_builder.model.editor_service import MapEditorService
from sage_map_builder.model.game_object import GameObject
from sage_map_builder.model.map_document import MapDocument, MapDimensions
from sage_map_builder.model.script import MapScript
from sage_map_builder.model.waypoint import Waypoint


def test_editor_service_unifies_entities_and_undo_redo():
    doc = MapDocument("mission.map", 0, MapDimensions(128, 128))
    editor = MapEditorService(doc)
    editor.add_waypoint(Waypoint("SPAWN", 10, 20))
    editor.add_object(GameObject("tank1", "TankTemplate", 10, 20))
    editor.add_script(MapScript("WAVE_1"))
    assert len(doc.waypoints) == len(doc.objects) == len(doc.scripts) == 1
    editor.undo(); assert doc.scripts == []
    editor.undo(); assert doc.objects == []
    editor.redo(); assert len(doc.objects) == 1
    editor.undo(); editor.undo(); assert doc.waypoints == []


def test_undo_empty_is_rejected():
    with pytest.raises(IndexError):
        MapEditorService(MapDocument("x.map", 0)).undo()
