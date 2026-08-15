# SAGE map format observations

## Reference samples

- `MY MAP.map`: 28,712 bytes
- `CONTRA Custom Campaign The Battle for Lake Town.map`: 147,237 bytes

## Verified observations

1. Both files begin with the byte sequence `45 41 52 00` (`EAR\\0`).
2. Both contain the ASCII marker `CkMp` at the same relative header position.
3. The files have substantially different sizes and payloads.
4. A field is not assigned a semantic meaning from a single sample.

## Rules for the reverse-engineering process

- Preserve the original binary samples unchanged.
- Separate observed facts from hypotheses.
- Confirm offsets against both samples before encoding them in `MapSchema`.
- Prefer controlled map edits (one change at a time) to infer dimensions, terrain, objects, waypoints, and scripts.
- Do not implement a production writer until a reader can round-trip a known sample without unexplained data loss.

## Current status

The samples are available in the repository root. The `research/map_samples` directory contains analysis documentation only; production code must never auto-load these files.
