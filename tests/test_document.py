import pytest

from sage_map_builder.models import MapDocument, Vector3, Waypoint, WorldObject


def test_empty_document_is_independent_of_world_builder() -> None:
    document = MapDocument.empty("Independent Test", 256, 256)
    assert document.metadata.title == "Independent Test"
    assert document.waypoints == []
    assert document.objects == []


def test_duplicate_waypoint_names_are_rejected() -> None:
    document = MapDocument.empty("Test", 256, 256)
    waypoint = Waypoint(name="SPAWN", position=Vector3(x=0, y=0, z=0))
    document.add_waypoint(waypoint)

    with pytest.raises(ValueError, match="duplicate waypoint"):
        document.add_waypoint(waypoint)


def test_duplicate_object_ids_are_rejected() -> None:
    document = MapDocument.empty("Test", 256, 256)
    obj = WorldObject(
        id="object-1",
        template_name="TestTemplate",
        position=Vector3(x=10, y=20, z=0),
    )
    document.add_object(obj)

    with pytest.raises(ValueError, match="duplicate object"):
        document.add_object(obj)
