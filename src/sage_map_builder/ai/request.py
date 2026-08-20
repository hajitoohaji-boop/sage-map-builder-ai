"""Versioned boundary object for natural-language map requests."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(frozen=True)
class MapRequest:
    text: str
    language: str = "auto"
    hints: dict[str, str] = field(default_factory=dict)
    version: int = 1

    def validate(self) -> None:
        if self.version != 1:
            raise ValueError("unsupported map request version")
        if not self.text.strip():
            raise ValueError("map request text cannot be empty")
        if self.language not in {"auto", "ar", "en"}:
            raise ValueError("language must be auto, ar, or en")
