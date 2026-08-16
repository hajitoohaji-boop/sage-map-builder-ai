"""Collection operations for placed GameObjects."""
from __future__ import annotations
from .game_object import GameObject
from .map_document import MapDocument


def add_object(document: MapDocument, obj: GameObject) -> None:
    if any(item.get("object_id") == obj.object_id for item in document.objects):
        raise ValueError(f"duplicate object id: {obj.object_id}")
    document.objects.append({"object_id": obj.object_id, "template": obj.template, "x": obj.x, "y": obj.y, "z": obj.z, "owner": obj.owner})


def remove_object(document: MapDocument, object_id: str) -> None:
    before = len(document.objects)
    document.objects[:] = [item for item in document.objects if item.get("object_id") != object_id]
    if len(document.objects) == before:
        raise KeyError(object_id)
