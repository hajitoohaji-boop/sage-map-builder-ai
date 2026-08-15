"""Deterministic mission-plan model; no AI dependency."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PlayerPlan:
    name: str
    faction: str


@dataclass(frozen=True)
class BasePlan:
    owner: str
    name: str
    x: float
    y: float


@dataclass(frozen=True)
class WavePlan:
    owner: str
    units: tuple[str, ...]
    delay_seconds: int


@dataclass
class MissionPlan:
    title: str
    players: list[PlayerPlan] = field(default_factory=list)
    bases: list[BasePlan] = field(default_factory=list)
    waves: list[WavePlan] = field(default_factory=list)
    objectives: list[str] = field(default_factory=list)

    def validate(self) -> None:
        if not self.title.strip():
            raise ValueError("mission title cannot be empty")
        names = {player.name.casefold() for player in self.players}
        if len(names) != len(self.players):
            raise ValueError("duplicate player name")
        for base in self.bases:
            if base.owner.casefold() not in names:
                raise ValueError(f"unknown base owner: {base.owner}")
        for wave in self.waves:
            if wave.owner.casefold() not in names:
                raise ValueError(f"unknown wave owner: {wave.owner}")
            if wave.delay_seconds < 0:
                raise ValueError("wave delay cannot be negative")
