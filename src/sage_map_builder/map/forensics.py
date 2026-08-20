"""Forensic structures extracted from real Generals/Zero Hour map dumps.

This module intentionally models only fields observed in supplied map dumps;
it does not claim to be the binary .map codec.
"""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(frozen=True)
class MapObjectRecord:
    unique_id: str
    original_owner: str = ""
    initial_health: int = 100
    enabled: bool = True
    indestructible: bool = False
    unsellable: bool = False
    powered: bool = True
    recruitable_ai: bool = True
    targetable: bool = False
    object_layer: str = ""
    veterancy: int | None = None
    object_name: str = ""

@dataclass(frozen=True)
class TeamRecord:
    name: str
    owner: str = ""
    singleton: bool = False
    production_priority: int = 0
    max_instances: int = 1
    initial_idle_frames: int = 0
    executes_actions_on_create: bool = False
    unit_min_max: tuple[tuple[int, int], ...] = field(default_factory=tuple)

@dataclass(frozen=True)
class PlayerRecord:
    name: str
    human: bool
    display_name: str
    faction: str = ""
    allies: tuple[str, ...] = field(default_factory=tuple)
    enemies: tuple[str, ...] = field(default_factory=tuple)

@dataclass(frozen=True)
class ForensicMapSummary:
    weather: int | None = None
    objects: tuple[MapObjectRecord, ...] = field(default_factory=tuple)
    teams: tuple[TeamRecord, ...] = field(default_factory=tuple)
    players: tuple[PlayerRecord, ...] = field(default_factory=tuple)
    script_blocks: tuple[str, ...] = field(default_factory=tuple)

    @property
    def object_count(self) -> int:
        return len(self.objects)

    @property
    def team_count(self) -> int:
        return len(self.teams)

    @property
    def player_count(self) -> int:
        return len(self.players)

    @property
    def script_count(self) -> int:
        return len(self.script_blocks)
