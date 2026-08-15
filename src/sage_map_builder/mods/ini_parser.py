"""Lexical parser for Generals-style INI definitions."""

from __future__ import annotations

from dataclasses import dataclass

from .registry import AssetEntry, ModRegistry


@dataclass(frozen=True)
class IniBlock:
    kind: str
    name: str
    properties: dict[str, str]
    source: str


def parse_ini(text: str, *, source: str = "<memory>") -> tuple[IniBlock, ...]:
    if not isinstance(text, str):
        raise TypeError("text must be str")
    blocks: list[IniBlock] = []
    kind: str | None = None
    name: str | None = None
    properties: dict[str, str] = {}

    def flush() -> None:
        nonlocal kind, name, properties
        if kind is not None and name is not None:
            blocks.append(IniBlock(kind, name, dict(properties), source))
        kind = name = None
        properties = {}

    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith(";") or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            flush()
            header = line[1:-1].strip()
            parts = header.split(None, 1)
            kind = parts[0]
            name = parts[1].strip() if len(parts) == 2 else parts[0]
            continue
        if "=" in line and kind is not None:
            key, value = line.split("=", 1)
            properties[key.strip()] = value.strip()
            continue
        parts = line.split(None, 1)
        if len(parts) == 2:
            flush()
            kind, name = parts[0], parts[1].strip()
        else:
            raise ValueError(f"unrecognized INI line: {raw!r}")
    flush()
    return tuple(blocks)


def build_registry(text: str, *, source: str = "<memory>") -> ModRegistry:
    registry = ModRegistry()
    for block in parse_ini(text, source=source):
        registry.add(AssetEntry(block.kind, block.name, block.source, block.properties))
    return registry
