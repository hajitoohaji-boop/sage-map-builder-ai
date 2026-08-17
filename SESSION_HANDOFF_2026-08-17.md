# Session Handoff — 2026-08-17

## Purpose
Continue the SAGE Map Builder AI project without repeating work or guessing binary structures.

## Current project goal
Build an independent World Builder-style editor for Generals / Zero Hour that can eventually read, edit, and create real `.map` files, with optional AI only translating natural-language descriptions into validated deterministic commands. The core must never guess unknown binary structures.

## Verified repository facts
- `PROJECT_STATUS.md` is the canonical continuation document.
- Current priority is **REAL MAP FORMAT DECODING**.
- Two real reference maps are recorded in `research/map_samples/sample_manifest.json`:
  - `MY MAP.map`: 28,712 bytes, blob SHA `7d4e1e0b21febd33a460f88a557c4a1e0b3fbb7c`.
  - `CONTRA Custom Campaign The Battle for Lake Town.map`: 147,237 bytes, blob SHA `b33c1ae19eea4c694bc8398571021e1cf1163e8c`.
  - Both verified prefix `45 41 52 00` (`EAR\\0`) and marker `CkMp`.
- Manifest rules: these are repository facts; do not hard-code semantic offsets; do not modify originals; cross-validate both samples before assigning field meanings.

## Architecture already implemented — DO NOT RECREATE
- Evidence/analysis: header evidence, marker scanning, byte regions, section evidence, cross-sample comparison, section confidence and validation.
- Map model: `MapDocument`, waypoints, objects, scripts, opaque sections, validation.
- Editing: `MapEditorService`, undo/redo, `EditSession` preview/commit/rollback.
- Serialization safety: JSON round-trip, preservation writer, bounded non-overlapping binary patches, real-sample preservation tests.
- Mod/asset stack: BIG reader/archive access, INI parser/scanner, asset index/classification, deterministic `ModRegistry`.
- Planning: `MapGenerationPlan`, validator, compiler.
- Binary primitives: corrected `DataChunk` 4-byte header (`version` + `dataSize`), opaque `chunk_sequence` round-trip, source-derived `WaypointsList` codec.
- Integration: `MapReader -> ByteRegions -> ChunkProbe -> ChunkPipelineResult`.

## Critical correction made
An earlier implementation incorrectly assumed an 8-byte DataChunk header containing a 32-bit ID. EA source evidence supports a 4-byte chunk header: two shorts, version and dataSize. Chunk identity/ID is associated with the table-of-contents mapping, not embedded in those four header bytes. Do not reintroduce the 8-byte assumption.

## Current technical boundary
The missing bridge is:

`.map bytes -> verified chunk identity/TOC -> verified codecs -> MapDocument -> real writer`

Do **not** create a guessed `ChunkTOC` implementation. The source search for `DataChunkTableOfContents`/`DataChunkTable` did not provide a directly usable implementation in the checked source index during this session. Treat TOC as unresolved until source and binary evidence agree.

## Last useful implementation step
`chunk_pipeline.py` connects existing `MapReader` regions to `ChunkProbe`. It intentionally preserves the reader result and returns probe results rather than assigning semantic names.

## What was NOT completed today
The integrated chunk pipeline was not yet executed against the two real repository samples and its resulting probe JSON was not persisted. Do this next if the files can be accessed reliably.

## Next session — exact order
1. Read this file and `PROJECT_STATUS.md` first.
2. Inspect the current `main` tree before creating anything.
3. Run/inspect the existing real-sample pipeline against both exact samples.
4. Persist deterministic probe/report output only from actual bytes; never invent values.
5. Compare both samples to identify repeated chunk boundaries and candidate identity metadata.
6. Cross-check candidate structures against EA World Builder source.
7. Promote a structure to a verified codec only when source + binary evidence agree.
8. Add tests for every new codec, including round-trip and malformed/truncated input.
9. Only after verified codecs exist, connect them to `MapDocument` and then the writer.
10. Update this handoff and `PROJECT_STATUS.md` after each major milestone.

## Anti-regression rules
- Search/fetch the repository before creating any file.
- Never recreate an existing architecture component.
- Never claim a file was created unless the GitHub write succeeded.
- Never claim a real sample was analyzed unless the actual bytes were accessed.
- Never infer semantic field names from offsets alone.
- Preserve unknown bytes.
- Keep original sample files immutable.
- Do not inflate the project percentage based on file count; percentage must reflect working end-to-end capability.

## Current realistic status
The project has a strong analysis/evidence/model/planning foundation, but the final product is not yet a verified real `.map` reader/writer. The decisive milestone remains a successful read/modify/write round-trip on a real Zero Hour map with verified structures and byte-preservation of unknown data.
