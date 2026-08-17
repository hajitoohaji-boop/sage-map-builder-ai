"""Deterministic in-memory registry for assets discovered from mod sources."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class AssetEntry:
    kind: str
    name: str
    source: str
    properties: dict[str, str]

    @property
    def key(self) -> tuple[str, str]:
        return self.kind.casefold(), self.name.casefold()


class ModRegistry:
    def __init__(self) -> None:
        self._entries: dict[tuple[str, str], AssetEntry] = {}

    def add(self, entry: AssetEntry) -> None:
        if not isinstance(entry, AssetEntry):
            raise TypeError("entry must be AssetEntry")
        self._entries[entry.key] = entry

    def get(self, kind: str, name: str) -> AssetEntry | None:
        return self._entries.get((kind.casefold(), name.casefold()))

    def all(self) -> tuple[AssetEntry, ...]:
        return tuple(self._entries.values())

    def by_kind(self, kind: str) -> tuple[AssetEntry, ...]:
        wanted = kind.casefold()
        return tuple(e for e in self._entries.values() if e.kind.casefold() == wanted)

    def __len__(self) -> int:
        return len(self._entries)
