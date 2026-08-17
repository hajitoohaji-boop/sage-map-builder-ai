"""Evidence model for observed mission/script records."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any

@dataclass(frozen=True)
class MissionEvidence:
    name: str
    enabled: bool | None = None
    team: str | None = None
    area: str | None = None
    conditions: tuple[str, ...] = ()
    actions: tuple[str, ...] = ()
    properties: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalize_observed_mission(record: dict[str, Any]) -> MissionEvidence:
    if not record.get("name"):
        raise ValueError("observed mission record requires a name")
    return MissionEvidence(
        name=str(record["name"]), enabled=record.get("enabled"),
        team=record.get("team"), area=record.get("area"),
        conditions=tuple(record.get("conditions") or ()),
        actions=tuple(record.get("actions") or ()),
        properties=dict(record.get("properties") or {}),
    )
