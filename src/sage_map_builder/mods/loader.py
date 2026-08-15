"""Unified deterministic loader for loose and BIG-contained INI assets."""

from __future__ import annotations

from pathlib import Path

from .archive import scan_archives
from .ini_parser import build_registry
from .registry import ModRegistry


def load_mod(root: str | Path) -> ModRegistry:
    root_path = Path(root)
    if not root_path.is_dir():
        raise NotADirectoryError(root_path)

    registry = ModRegistry()

    for path in sorted(root_path.rglob("*")):
        if not path.is_file() or path.suffix.casefold() not in {".ini", ".inc"}:
            continue
        for entry in build_registry(
            path.read_text(encoding="utf-8-sig", errors="replace"),
            source=str(path),
        ).all():
            registry.add(entry)

    archives = scan_archives(root_path)
    for archive_path, archive in archives.big_archives:
        raw = archive_path.read_bytes()
        for entry in archive.entries:
            if Path(entry.name).suffix.casefold() not in {".ini", ".inc"}:
                continue
            payload = raw[entry.offset : entry.offset + entry.size]
            text = payload.decode("utf-8-sig", errors="replace")
            for asset in build_registry(text, source=f"{archive_path}!{entry.name}").all():
                registry.add(asset)

    return registry
