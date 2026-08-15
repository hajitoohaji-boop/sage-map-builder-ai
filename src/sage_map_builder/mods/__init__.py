"""Mod inspection and asset-registry support."""

from .archive import ModArchive, scan_archives
from .big_reader import BigArchive, BigEntry, BigFormatError, read_big
from .csf import CsfEntry, CsfTable
from .ini_parser import IniBlock, build_registry, parse_ini
from .registry import AssetEntry, ModRegistry
from .scanner import scan_mod_directory

__all__ = [
    "AssetEntry",
    "BigArchive",
    "BigEntry",
    "BigFormatError",
    "CsfEntry",
    "CsfTable",
    "IniBlock",
    "ModArchive",
    "ModRegistry",
    "build_registry",
    "parse_ini",
    "read_big",
    "scan_archives",
    "scan_mod_directory",
]
