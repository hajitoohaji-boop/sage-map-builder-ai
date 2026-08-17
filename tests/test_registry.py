from sage_map_builder.mods.registry import AssetEntry, ModRegistry


def test_registry_is_case_insensitive_and_replaces_same_key():
    registry = ModRegistry()
    registry.add(AssetEntry("Object", "TankBoss", "a.ini", {"BuildCost": "500"}))
    registry.add(AssetEntry("object", "tankboss", "b.ini", {"BuildCost": "600"}))

    entry = registry.get("OBJECT", "TANKBOSS")
    assert entry is not None
    assert entry.source == "b.ini"
    assert entry.properties["BuildCost"] == "600"
    assert len(registry) == 1


def test_registry_by_kind():
    registry = ModRegistry()
    registry.add(AssetEntry("Object", "Tank", "a.ini", {}))
    registry.add(AssetEntry("Building", "Factory", "b.ini", {}))
    assert [e.name for e in registry.by_kind("object")] == ["Tank"]
