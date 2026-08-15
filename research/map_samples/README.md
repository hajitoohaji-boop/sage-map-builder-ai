# Reference map samples

These binary maps are research references only. They are not production assets.

Expected repository-root samples:

- `MY MAP.map` — user's map sample.
- `CONTRA Custom Campaign The Battle for Lake Town.map` — reference mission.

The paired `.tga` files are also reference material.

## Safe analysis workflow

`probe_map.py` reads samples without modifying them and reports file size, SHA-256, initial bytes, known markers, and raw 32-bit interpretations from the first 512 bytes. It intentionally assigns **no semantic field names**.

Example:

```text
python research/map_samples/probe_map.py "MY MAP.map" "CONTRA Custom Campaign The Battle for Lake Town.map" --output map_probe.json
```

The production package must never automatically load files from this research directory or the repository-root samples.
