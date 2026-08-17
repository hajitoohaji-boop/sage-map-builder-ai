# SAGE Map Builder AI — Continuation Checkpoint

Date: 2026-08-17

## Purpose
This checkpoint prevents repeating work in a future conversation. Read `PROJECT_STATUS.md` first; this file records the exact working state and the rules for continuing.

## Final goal
Build an independent World Builder-style editor for Command & Conquer: Generals – Zero Hour / SAGE maps. The deterministic core must work without AI. AI is optional and must never guess unknown binary structures. The final product must eventually understand a user description, create a complete valid map compatible with the game/mod, and provide an editor-like view.

## Repository
`hajitoohaji-boop/sage-map-builder-ai`, default branch `main`.

## Confirmed architecture already implemented
- Analysis/evidence pipeline: header evidence, byte regions, markers, section evidence, cross-sample comparison, confidence and range validation.
- `MapReader` and preservation-oriented binary handling.
- `MapDocument` internal model with objects, waypoints, scripts and opaque sections.
- `MapEditorService` and EditSession/transactional editing.
- Preservation writer and explicit bounded binary patches.
- BIG/INI/mod asset stack and `ModRegistry`.
- `MapGenerationPlan`, validator and compiler.
- `DataChunk` primitive and `chunk_sequence`.
- Source-derived `WaypointsList` codec.

## Critical correction already made
An earlier implementation incorrectly assumed an 8-byte DataChunk header containing an ID. EA source evidence established the DataChunk header as 4 bytes: version + dataSize. Chunk identity/IDs must NOT be inferred from those four bytes; TOC/identity mapping remains unverified.

## Real samples
According to `PROJECT_STATUS.md`:
- `MY MAP.map`: 28,712 bytes; blob SHA `7d4e1e0b21febd33a460f88a557c4a1e0b3fbb7c`.
- `CONTRA Custom Campaign The Battle for Lake Town.map`: 147,237 bytes; blob SHA `b33c1ae19eea4c694bc8398571021e1cf1163e8c`.
- Both begin with `45 41 52 00` (`EAR\\0`).
- `CkMp` occurs at the same relative header position.
- `research/map_samples/sample_manifest.json` is the manifest source.

## Current exact priority
**REAL MAP FORMAT DECODING.**
1. Run the existing evidence/report pipeline against both exact samples.
2. Persist the resulting JSON reports.
3. Compare the samples to isolate candidate section/chunk boundaries.
4. Do NOT assign semantic names to candidate chunks until source + binary evidence support them.
5. Verify chunk identity/TOC before building semantic decoders.
6. Then decode verified structures into `MapDocument`.
7. Then prove lossless read/write round-trip.
8. Only after that build a verified binary writer for edited sections.

## Current useful binary path
`.map -> MapReader -> ByteRegions -> ChunkProbe -> ChunkPipelineResult -> cross-sample evidence -> verified chunk -> codec -> MapDocument`

## Important existing files (do not recreate blindly)
- `src/sage_map_builder/map/reader.py`
- `src/sage_map_builder/map/pipeline.py`
- `src/sage_map_builder/map/sections.py`
- `src/sage_map_builder/map/section_report.py`
- `src/sage_map_builder/map/section_confidence.py`
- `src/sage_map_builder/map/section_validation.py`
- `src/sage_map_builder/map/chunk_pipeline.py`
- `src/sage_map_builder/formats/data_chunk.py`
- `src/sage_map_builder/formats/chunk_sequence.py`
- `src/sage_map_builder/formats/chunk_probe.py`
- `src/sage_map_builder/formats/waypoints_chunk.py`
- `src/sage_map_builder/formats/worldbuilder_source.py`
- `src/sage_map_builder/map/document.py`
- `src/sage_map_builder/map/document_report.py`
- `src/sage_map_builder/planning/compiler.py`
- `src/sage_map_builder/planning/plan.py`
- `src/sage_map_builder/planning/validator.py`
- `src/sage_map_builder/mods/registry.py`
- `PROJECT_STATUS.md`

## Recent commits mentioned during work
- `d3334c00` — DataChunk header correction.
- `9e80d953` — chunk sequence correction.
- `3acbb9a5` — updated chunk tests.
- `be0c4bc4` — connect map regions to DataChunk probing.
- `801ee56f` — integrated chunk pipeline test.
- `e7e95aa4` — corrected real-sample manifest test.
- `b5d7b023` — real-sample preservation regression test.
- `2ddacd54` — project status update.

Exact commit ancestry should be checked from GitHub before relying on these SHAs; do not assume a SHA is on `main` without verification.

## What must NOT happen again
- Do not recreate files that already exist.
- Do not claim a file was created unless GitHub confirms the write.
- Do not claim tests passed unless an actual test run/result is available.
- Do not invent TOC layouts, chunk IDs, offsets, dimensions, terrain structures, object serialization, player/team layouts or script structures.
- Do not infer semantic section names merely from repeated bytes.
- Do not increase the project percentage merely because more files exist.
- Do not replace opaque bytes when their meaning is unknown.
- Do not start GUI/AI work ahead of verified map decoding.

## Progress estimate
Use the functional milestone, not file count. The project is approximately 42% toward the complete product as previously estimated, but the key missing milestone is still: verified `.map` semantic decoding and a real editable binary writer that produces a map the game can open. Do not raise the percentage until that milestone moves.

## Next session
Start by reading `PROJECT_STATUS.md` and this checkpoint. Then inspect the current `main` tree and recent commits. Execute/verify the real-sample evidence pipeline. If sample files cannot be fetched through GitHub in the current tool session, do not fabricate results; report the limitation and continue with source-backed code only.
