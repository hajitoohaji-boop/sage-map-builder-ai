"""Conservative CSF text-table model.

CSF decoding is kept separate from INI parsing because CSF is a binary string
resource format, not an INI format.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CsfEntry:
    key: str
    value: str


class CsfTable:
    def __init__(self, entries: tuple[CsfEntry, ...] = ()) -> None:
        self._entries = {entry.key.casefold(): entry for entry in entries}

    def get(self, key: str) -> str | None:
        entry = self._entries.get(key.casefold())
        return entry.value if entry else None

    def all(self) -> tuple[CsfEntry, ...]:
        return tuple(self._entries.values())
