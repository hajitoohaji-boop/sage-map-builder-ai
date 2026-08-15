from pathlib import Path

from sage_map_builder.mods.loader import load_mod


def test_load_mod_reads_loose_ini(tmp_path: Path) -> None:
    (tmp_path / "a.ini").write_text(
        "Object LooseTank\n  BuildCost = 100\n", encoding="utf-8"
    )
    registry = load_mod(tmp_path)
    assert registry.get("object", "loosetank") is not None
