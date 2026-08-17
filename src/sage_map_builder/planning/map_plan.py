"""Deterministic intermediate plan for description -> map generation.

An optional AI adapter may produce this schema, but validation and execution
remain deterministic and independent of any model.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any

@dataclass
class MapIntent:
    title: str = ""
    width: int = 256
    height: int = 256
    description: str = ""
    factions: list[str] = field(default_factory=list)
    objectives: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)

    def validate(self) -> None:
        if self.width < 64 or self.height < 64 or self.width > 512 or self.height > 512:
            raise ValueError("map dimensions must be between 64 and 512")
        if self.width % 64 or self.height % 64:
            raise ValueError("map dimensions must be multiples of 64")

@dataclass
class PlacementIntent:
    kind: str
    template: str
    x: float
    y: float
    z: float = 0.0
    owner: str | None = None
    properties: dict[str, Any] = field(default_factory=dict)

@dataclass
class MissionIntent:
    objectives: list[str] = field(default_factory=list)
    scripts: list[dict[str, Any]] = field(default_factory=list)
    waves: list[dict[str, Any]] = field(default_factory=list)

@dataclass
class MapGenerationPlan:
    intent: MapIntent
    placements: list[PlacementIntent] = field(default_factory=list)
    mission: MissionIntent = field(default_factory=MissionIntent)
    warnings: list[str] = field(default_factory=list)
    unresolved: list[str] = field(default_factory=list)

    def validate(self) -> None:
        self.intent.validate()
        for item in self.placements:
            if not item.template:
                raise ValueError("placement template cannot be empty")
        if any(not x.strip() for x in self.unresolved):
            raise ValueError("unresolved entries must be non-empty")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return asdict(self)
