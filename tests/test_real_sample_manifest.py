import json
from pathlib import Path


def test_manifest_contains_two_verified_samples_and_observations():
    manifest = json.loads(Path("research/map_samples/sample_manifest.json").read_text(encoding="utf-8"))
    samples = manifest["samples"]
    assert len(samples) == 2
    names = {s["path"] for s in samples}
    assert names == {"MY MAP.map", "CONTRA Custom Campaign The Battle for Lake Town.map"}
    for sample in samples:
        assert sample["size"] > 0
        assert len(sample["blob_sha"]) == 40
        assert sample["verified_prefix_hex"].lower() == "45 41 52 00"
        assert sample["verified_marker"] == "CkMp"


def test_binary_samples_match_manifest_if_present_in_checkout():
    manifest = json.loads(Path("research/map_samples/sample_manifest.json").read_text(encoding="utf-8"))
    root = Path(".")
    for sample in manifest["samples"]:
        path = root / sample["path"]
        if not path.exists():
            continue
        data = path.read_bytes()
        assert len(data) == sample["size"]
        assert data[:4] == bytes.fromhex(sample["verified_prefix_hex"])
        assert sample["verified_marker"].encode("ascii") in data
