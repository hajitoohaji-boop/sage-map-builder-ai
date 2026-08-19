# SAGE Map Builder AI — Project Status

Last updated: 2026-08-19

## Goal
Build an independent World Builder-style editor for Command & Conquer: Generals – Zero Hour / SAGE maps. The core editor is deterministic and never guesses unknown binary structures; AI is optional and separate. Final goal: a usable independent World Builder that can eventually understand a user description, generate a complete valid map compatible with the game/mod, and provide an editor-like view.

## Current milestone
**REAL MAP FORMAT DECODING — CURRENT**

## Implemented
- Evidence-preserving MapReader and binary discovery.
- Header/word/marker/region evidence and cross-sample comparison.
- Section reports, confidence and range validation.
- Evidence-only source-backed label scanner.
- `CkMp` evidence probe without assigning semantic meaning to following integers.
- Caller-bounded DataChunk probing.
- `MapDocument`, preservation writer, explicit bounded patches, transactional editing.
- Waypoints/objects/scripts models and editor service.
- BIG/INI/mod asset stack and `ModRegistry`.
- `MapGenerationPlan` + validator + compiler.
- DataChunk primitive, sequence reader/writer, chunk envelope, batch dispatch/reporting.
- Verified/Opaque chunk result separation.
- Source chunk catalogue and exact label+version matching.
- Source evidence bridge for observed chunks.

## Verified real samples
1. `MY MAP.map` — 28,712 bytes — blob SHA `7d4e1e0b21febd33a460f88a557c4a1e0b3fbb7c`.
2. `CONTRA Custom Campaign The Battle for Lake Town.map` — 147,237 bytes — blob SHA `b33c1ae19eea4c694bc8398571021e1cf1163e8c`.
Both start with `45 41 52 00` (`EAR\\0`); `CkMp` occurs at the same relative header position.

## Source-backed chunk facts
Audited EA WorldBuilder source explicitly exposes these save calls:
- `HeightMapData` v4, top-level order 1
- `BlendTileData` v7, top-level order 2
- `WorldInfo` v1, top-level order 3
- `ObjectsList` v3, top-level order 4
- `Object` v3, nested under `ObjectsList`
- `GlobalLighting` v3, top-level order 6
- `WaypointsList` v1, top-level order 7

The source catalogue does **not** by itself prove byte offsets in either real sample. Helper-emitted chunks remain unresolved until their writers are audited.

## DataChunk caution
The verified binary primitive is a 4-byte header: little-endian uint16 `version` + uint16 `dataSize`. The source facts also mention a container/table-of-contents layer with labels; these must not be conflated with the four-byte DataChunk header. TOC identity/layout remains unverified.

## Verified semantic codec
`WaypointsList v1` is source-derived. Its payload stores a link count followed by two integers per link. Structural validation now checks truncation, negative counts and exact payload length.

All other source-backed chunks currently remain opaque until their payload structure is supported by source + binary evidence.

## New evidence bridge (2026-08-19)
Added:
- `formats/source_chunk_match.py`: exact label+version matching against the audited source catalogue.
- `map/source_evidence.py`: attaches that source fact to an observed offset/end/label/version without inferring unknown semantics.
- Tests for exact match, nested Object v3, unknown versions and bounds validation.

## Important rules
- Do not recreate existing files.
- Do not claim tests passed unless an actual test run/result is available.
- Do not invent TOC layouts, offsets, dimensions, terrain/object/player/script serialization.
- Do not promote a semantic chunk without source + binary evidence.
- Unknown bytes must remain lossless/opaque.
- Do not raise project percentage merely because file count increased.
- Continue from this status in every new conversation.

## Next priorities
1. Execute/obtain evidence reports for the exact binary samples.
2. Match source-backed labels/versions to real byte ranges using controlled binary evidence.
3. Audit remaining WorldBuilder save helpers, especially heightmap, world info, objects and helper-emitted chunks.
4. Decode the first newly verified semantic chunk.
5. Prove untouched-map lossless round trip, then verified editing/writing.
6. Expand mod/INI asset database.
7. Build GUI and optional Arabic AI adapter only after binary core is reliable.

## Integrity note
GitHub Actions exists for pytest, but no completed CI run is currently exposed by the connector; CI is therefore not claimed as passing.
