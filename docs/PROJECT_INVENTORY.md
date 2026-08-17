# Project Inventory — verified against `main`

This inventory is intentionally factual. It records files observed in the current Git tree and known dependency gaps; it does not claim that a component is complete merely because a file exists.

## Current map research stack

- `map/reader.py` — evidence-preserving byte reader.
- `map/document.py` — engine-owned `MapDocument` with objects, waypoints and mission.
- `map/builder.py` — deterministic document construction helpers.
- `map/sections.py` — conservative byte-run and marker detection.
- `map/section_report.py` — JSON section report containing sample metadata, markers and common byte runs.
- `map/evidence.py`, `map/format_probe.py`, header/region helpers — binary evidence and probing.
- `analysis/*` — candidate sections, comparisons, fingerprints, controlled diffs and semantic evidence.
- `formats/data_chunk.py` — source-derived DataChunk primitive.
- `formats/waypoints_chunk.py` — source-derived WaypointsList codec.
- `formats/worldbuilder_source.py` — recorded World Builder source facts.

## Current mod stack

- `mods/big_reader.py` — bounded BIG archive reader.
- `mods/archive.py` — read-only directory/BIG archive access.
- `mods/ini_parser.py` — lexical INI block parser.
- `mods/scanner.py` — recursive INI-like source scanner.
- `mods/assets.py` — normalized asset classification.
- `mods/asset_index.py` — queryable normalized asset index.
- `mods/registry.py` — deterministic registry restored because the current scanner/parser imported it but the file was absent from `main`.

## Current mission/planning stack

- `planner/mission_plan.py` — deterministic players, bases, waves and objectives.
- `planning/*` — generation-plan validation and related planning models where present.
- `map/document.py` explicitly keeps the deterministic engine independent from AI.

## Current research inputs

- `CONTRA Custom Campaign The Battle for Lake Town.map`
- `MY MAP.map`
- matching `.tga` files
- `contra M.txt`
- `research/map_samples/*`
- `docs/research/worldbuilder-source-audit.md`

## Verification policy

1. Existing source is inspected before creating a replacement.
2. A missing dependency is fixed before adding a new feature that depends on it.
3. Observed binary values are not promoted to semantic fields without source or controlled-diff evidence.
4. New implementation files require tests.
5. A successful Python unit test is not treated as proof of Zero Hour compatibility; a real `.map` round-trip and in-game load are separate acceptance gates.

## Immediate engineering order

1. Keep the current tree importable and tested (`ModRegistry` gap fixed).
2. Connect the existing section/marker report to the existing evidence models without duplicating the older research pipeline.
3. Extract exact serialization behavior from the EA World Builder source for each map subsystem.
4. Implement a lossless reader before implementing a semantic writer.
5. Add round-trip tests against the repository's real `.map` samples.
6. Only after round-trip success, expand generation from `MapDocument` to binary `.map` output.
