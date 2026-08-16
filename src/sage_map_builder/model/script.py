"""Neutral mission-script model for deterministic editing."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class ScriptAction:
    kind: str
    args: dict[str, Any] = field(default_factory=dict)

@dataclass
class MapScript:
    name: str
    enabled: bool = True
    conditions: list[ScriptAction] = field(default_factory=list)
    actions: list[ScriptAction] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("script name must not be empty")


def add_script(document, script: MapScript) -> None:
    if any(item.get("name") == script.name for item in document.scripts):
        raise ValueError(f"duplicate script name: {script.name}")
    document.scripts.append({
        "name": script.name,
        "enabled": script.enabled,
        "conditions": [{"kind": a.kind, "args": dict(a.args)} for a in script.conditions],
        "actions": [{"kind": a.kind, "args": dict(a.args)} for a in script.actions],
    })


def remove_script(document, name: str) -> None:
    before = len(document.scripts)
    document.scripts[:] = [s for s in document.scripts if s.get("name") != name]
    if len(document.scripts) == before:
        raise KeyError(name)
