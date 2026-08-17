"""Unified deterministic domain service for editing MapDocument."""
from __future__ import annotations
from dataclasses import dataclass
from copy import deepcopy

from .map_document import MapDocument
from .waypoint import Waypoint
from .waypoint_store import add_waypoint, remove_waypoint
from .game_object import GameObject
from .object_store import add_object, remove_object
from .script import MapScript, add_script, remove_script

@dataclass(frozen=True)
class EditorSnapshot:
    waypoints: list[dict]
    objects: list[dict]
    scripts: list[dict]

class MapEditorService:
    """Single API used by future GUI/CLI; it never edits raw lists directly."""
    def __init__(self, document: MapDocument) -> None:
        self.document = document
        self._history: list[EditorSnapshot] = []
        self._redo: list[EditorSnapshot] = []

    def _save(self) -> None:
        self._history.append(EditorSnapshot(deepcopy(self.document.waypoints), deepcopy(self.document.objects), deepcopy(self.document.scripts)))
        self._redo.clear()

    def _restore(self, snap: EditorSnapshot) -> None:
        self.document.waypoints = deepcopy(snap.waypoints)
        self.document.objects = deepcopy(snap.objects)
        self.document.scripts = deepcopy(snap.scripts)

    def add_waypoint(self, waypoint: Waypoint) -> None:
        self._save(); add_waypoint(self.document, waypoint)

    def remove_waypoint(self, name: str) -> None:
        self._save(); remove_waypoint(self.document, name)

    def add_object(self, obj: GameObject) -> None:
        self._save(); add_object(self.document, obj)

    def remove_object(self, object_id: str) -> None:
        self._save(); remove_object(self.document, object_id)

    def add_script(self, script: MapScript) -> None:
        self._save(); add_script(self.document, script)

    def remove_script(self, name: str) -> None:
        self._save(); remove_script(self.document, name)

    def undo(self) -> None:
        if not self._history:
            raise IndexError("nothing to undo")
        current = EditorSnapshot(deepcopy(self.document.waypoints), deepcopy(self.document.objects), deepcopy(self.document.scripts))
        self._redo.append(current)
        self._restore(self._history.pop())

    def redo(self) -> None:
        if not self._redo:
            raise IndexError("nothing to redo")
        current = EditorSnapshot(deepcopy(self.document.waypoints), deepcopy(self.document.objects), deepcopy(self.document.scripts))
        self._history.append(current)
        self._restore(self._redo.pop())
