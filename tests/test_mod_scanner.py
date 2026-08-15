from pathlib import Path

from sage_map_builder.mods.scanner import scan_mod_directory


def test_scan_mod_directory_reads_ini_files(tmp_path: Path) -> None:
    (tmp_path / "Data").mkdir()
    (tmp_path / "Data" / "objects.ini").write_text(
        "Object TankBoss\n  BuildCost = 500\n", encoding="utf-8"
    )
    (tmp_path / "ignore.bin").write_bytes(b"not ini")

    registry = scan_mod_directory(tmp_path)
    entry = registry.get("object", "tankboss")
    assert entry is not None
    assert entry.properties["BuildCost"] == "500"
