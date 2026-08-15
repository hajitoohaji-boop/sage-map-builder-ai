"""Recursive scanner for mod source files."""

from __future__ import annotations

from pathlib import Path

from .ini_parser import build_registry
from .registry import ModRegistry


INI_SUFFIXES = {".ini", ".inc", ".txt"}


def scan_mod_directory(root: str | Path) -> ModRegistry:
    """Scan readable INI-like files without modifying the source tree."""
    root_path = Path(root)
    if not root_path.is_dir():
        raise NotADirectoryError(root_path)

    registry = ModRegistry()
    for path in sorted(root_path.rglob("*")):
        if not path.is_file() or path.suffix.casefold() not in INI_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        parsed = build_registry(text, source=str(path))
        for entry in parsed.all():
            registry.add(entry)
    return registry
