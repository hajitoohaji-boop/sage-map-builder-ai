"""Queryable normalized asset index."""

from __future__ import annotations

from .assets import NormalizedAsset, classify_asset
from .registry import ModRegistry


class AssetIndex:
    def __init__(self, assets: tuple[NormalizedAsset, ...]) -> None:
        self._assets = assets

    def find(self, name: str) -> NormalizedAsset | None:
        wanted = name.casefold()
        return next((asset for asset in self._assets if asset.name.casefold() == wanted), None)

    def by_kind(self, kind: str) -> tuple[NormalizedAsset, ...]:
        wanted = kind.casefold()
        return tuple(asset for asset in self._assets if asset.kind == wanted)

    def all(self) -> tuple[NormalizedAsset, ...]:
        return self._assets


def build_asset_index(registry: ModRegistry) -> AssetIndex:
    assets = tuple(
        classify_asset(entry.kind, entry.name, entry.source, entry.properties)
        for entry in registry.all()
    )
    return AssetIndex(assets)
