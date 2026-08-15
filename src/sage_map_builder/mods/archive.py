"""Unified read-only access to files stored in a mod directory or BIG archive."""

from __future__ import annotations

from pathlib import Path

from .big_reader import BigArchive, BigEntry, read_big


class ModArchive:
    def __init__(self, directory: Path, big_archives: tuple[tuple[Path, BigArchive], ...]) -> None:
        self.directory = directory
        self.big_archives = big_archives

    def find_big_entry(self, name: str) -> tuple[Path, BigEntry] | None:
        wanted = name.replace("\\", "/").casefold()
        for archive_path, archive in self.big_archives:
            for entry in archive.entries:
                if entry.name.replace("\\", "/").casefold() == wanted:
                    return archive_path, entry
        return None


def scan_archives(root: str | Path) -> ModArchive:
    root_path = Path(root)
    if not root_path.is_dir():
        raise NotADirectoryError(root_path)

    archives: list[tuple[Path, BigArchive]] = []
    for path in sorted(root_path.rglob("*.big")):
        data = path.read_bytes()
        archives.append((path, read_big(data)))
    return ModArchive(root_path, tuple(archives))
