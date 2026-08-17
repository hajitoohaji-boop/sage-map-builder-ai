"""Validate section candidates without assigning semantic meaning."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class SectionRange:
    start: int
    end: int

    def validate(self, size: int) -> None:
        if size < 0 or self.start < 0 or self.end <= self.start or self.end > size:
            raise ValueError("section range is outside binary input")


def validate_non_overlapping(sections: list[SectionRange], size: int) -> list[SectionRange]:
    ordered = sorted(sections, key=lambda item: (item.start, item.end))
    for section in ordered:
        section.validate(size)
    for previous, current in zip(ordered, ordered[1:]):
        if current.start < previous.end:
            raise ValueError("section ranges overlap")
    return ordered
