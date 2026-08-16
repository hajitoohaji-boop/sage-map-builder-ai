import pytest
from sage_map_builder.model.game_object import GameObject
from sage_map_builder.model.map_document import MapDocument
from sage_map_builder.model.object_store import add_object, remove_object


def test_add_and_remove_object():
    doc = MapDocument("x.map", 0)
    add_object(doc, GameObject("obj-1", "AmericaVehicleHumvee", 10, 20, owner="Player_1"))
    assert doc.objects[0]["template"] == "AmericaVehicleHumvee"
    remove_object(doc, "obj-1")
    assert doc.objects == []


def test_duplicate_object_id_is_rejected():
    doc = MapDocument("x.map", 0)
    obj = GameObject("obj-1", "Building", 1, 2)
    add_object(doc, obj)
    with pytest.raises(ValueError):
        add_object(doc, obj)
