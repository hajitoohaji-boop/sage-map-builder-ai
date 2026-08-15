"""Normalized asset classification for Generals/Zero Hour mod data."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NormalizedAsset:
    name: str
    kind: str
    source: str
    properties: dict[str, str]


def classify_asset(kind: str, name: str, source: str, properties: dict[str, str]) -> NormalizedAsset:
    k = kind.casefold()
    if k in {"object", "unit", "building", "aircraft", "vehicle", "infantry", "weapon", "upgrade", "specialpower", "playertemplate"}:
        normalized_kind = k
    else:
        normalized_kind = "other"
    return NormalizedAsset(name=name, kind=normalized_kind, source=source, properties=dict(properties))
