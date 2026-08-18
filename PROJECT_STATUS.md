# SAGE Map Builder AI — Project Status

Last updated: 2026-08-18

## Goal
Build an independent World Builder-style editor for Command & Conquer: Generals – Zero Hour / SAGE maps.

Requirements: the core editor works without AI; Gemini/other AI is optional and separate; the core is deterministic and never guesses unknown binary structures; Arabic descriptions may later use a separate AI adapter; the two supplied map files remain separate reference samples; supplied mod/INI files must eventually drive the asset database; final goal is a usable independent World Builder, not only an analyzer.

## Implemented

### Analysis foundation
- Header evidence and header-word extraction.
- Byte-region detection and region layout matching.
- Evidence-preserving MapReader.
- Per-map Section Report JSON.
- Single-map and two-map analysis pipelines.
- Automatic `.map` discovery and discovery pipeline.
- Byte evidence primitives (`ByteEvidence`) with offset, length, SHA-256 and hex preview.
- Deterministic marker scanner.
- Conservative section-boundary evidence extractor.
- Deterministic cross-sample byte comparison.
- Unified evidence-only sample report.
- Unified evidence-only cross-sample comparison report.
- Section confidence and section-range validation.
- Evidence-only scanner for literal labels explicitly backed by the audited WorldBuilder source.
- `CkMp` evidence probe records every occurrence and the following little-endian u32 without assigning a semantic meaning.
- `ChunkStreamProbe` validates caller-supplied contiguous regions as four-byte DataChunk streams without inventing boundaries or labels.

### Verified real samples
The repository tree was checked directly. The two real maps are present in the repository root:
1. `MY MAP.map` — 28,712 bytes — blob SHA `7d4e1e0b21febd33a460f88a557c4a1e0b3fbb7c`.
2. `CONTRA Custom Campaign The Battle for Lake Town.map` — 147,237 bytes — blob SHA `b33c1ae19eea4c694bc8398571021e1cf1163e8c`.
Verified observations: both start with `45 41 52 00` (`EAR\\0`); `CkMp` occurs at the same relative header position; payload sizes differ substantially. Manifest: `research/map_samples/sample_manifest.json`.

### Internal model
`MapDocument` contains file name, raw size, optional dimensions, regions, waypoints, objects, scripts, and opaque sections. Unknown binary data is preserved rather than guessed.

### Serialization/edit safety
- Deterministic MapDocument JSON round trip.
- Lossless preservation writer.
- Explicit binary patches with bounds/overlap checks.
- Transactional EditSession with preview/commit/rollback.
- Real-sample preservation regression tests now cover both repository maps when present.

### World Builder data model
- Waypoints: validated coordinates/names, optional bounds, duplicate prevention, add/remove.
- Objects: ID, template, X/Y/Z, optional owner, duplicate prevention, add/remove.
- Scripts: enabled flag, conditions/actions and generic ScriptAction(kind,args), duplicate prevention, add/remove.
- `MapEditorService`: unified entity API plus snapshot undo/redo.
- Cross-reference validation for script -> waypoint/object references.

## Reporting layer
Added `sample_report.py` and `compare_report.py` plus tests. Reports intentionally keep `semantic_interpretation = null`; they record hashes, sizes, header evidence, markers, section evidence and byte-level comparisons without claiming unverified field meanings.

## Binary format work
- `DataChunk` header is the EA-source-supported 4-byte header (`version` + `dataSize`), encoded as two little-endian uint16 values.
- `chunk_sequence.py` preserves opaque payloads and supports lossless chunk-sequence round trip.
- `ChunkStreamProbe` now safely tests a caller-supplied byte range as a contiguous DataChunk sequence.
- `WaypointsList` codec is source-derived, but full map chunk identity/TOC is not yet verified.
- No semantic chunk name is promoted without both source and binary evidence.
- Source-backed chunk catalogue currently covers explicit World Builder save calls: `HeightMapData` v4, `BlendTileData` v7, `WorldInfo` v1, `ObjectsList` v3, nested `Object` v3, `GlobalLighting` v3, and `WaypointsList` v1.
- The catalogue deliberately leaves helper-emitted chunks such as `SidesList` and polygon-trigger data unresolved until their writers are audited.
- `source_chunk_markers.py` reports exact literal occurrences of source-backed labels as binary evidence only.
- `CkMp` evidence is recorded but its following integer is intentionally not called a size/count/offset/version until proven.

## Test integrity
- Found and corrected a stale `tests/test_data_chunk.py` that still used the obsolete three-field/8-byte header assumption. It now tests the verified two-field/4-byte header, uint16 boundaries, and truncation behavior.
- Added tests for `ChunkStreamProbe` valid streams, truncation and caller-specified boundaries.
- Added exports for the new evidence tools from `sage_map_builder.analysis`.
- GitHub Actions workflow exists for pytest, but no completed workflow run is currently exposed by the connector, so CI is not claimed as passing.

## Mod/asset stack
- BIG archive reader, archive access, INI parser/scanner, asset classification/index and deterministic `ModRegistry` are present.
- `MapGenerationPlan` + validator + compiler are present and keep unknown assets from being silently invented.

## Architecture
```text
REAL .map samples
  -> binary discovery
  -> MapReader / evidence
     -> Header / words / regions / markers
     -> CkMp evidence
     -> source-backed label evidence
     -> caller-bounded DataChunk probing
  -> evidence-only sample reports
  -> cross-sample comparison
  -> MapDocument (only for verified semantics)
     -> Waypoints / Objects / Scripts / Opaque Sections
  -> MapEditorService
     -> validation / undo / redo
  -> EditSession / Preservation Writer
  -> output .map
```

Separate future AI path: `Arabic description -> optional AI adapter -> validated commands`. AI is never required by the core editor.

## Next priorities

### 1. REAL MAP FORMAT DECODING — CURRENT
The EA source audit gives explicit chunk labels, versions, ordering, and payload-writing behavior for several major map sections. The next decisive task is to obtain/execute the evidence pipeline over the exact binary samples and use controlled evidence to match source-backed structures to byte ranges. Do not assign offsets or TOC identity until the binary evidence supports them.

### 2. Audit all remaining WorldBuilder save helpers
Continue through `WHeightMapEdit.cpp`, `WorldBuilderDoc.cpp`, object/side/trigger serializers and related `DataChunk` callers to enumerate every explicit chunk/version and payload format.

### 3. Golden sample tests
Exact size/prefix/marker checks are covered against the repository manifest; untouched preservation tests cover both real samples when checked out.

### 4. Real semantic decoding
Only after evidence supports it, identify header/dimensions, terrain/height, textures, objects, waypoints, players/teams, scripts/mission data and remaining sections.

### 5. Real binary writer
First prove exact read/write preservation for an untouched sample. Only then write verified sections while preserving unknown bytes byte-for-byte.

### 6. Mod/INI asset database
Read supplied mod files and build a registry of actual factions, units, buildings, upgrades, special powers, templates and PlayerTemplate/ownership data.

### 7. GUI
Build the independent World Builder interface around MapEditorService.

### 8. Mission/script system
Translate common World Builder concepts into validated commands and export only when the map representation is verified.

### 9. Arabic optional layer
Keep Arabic handling outside the deterministic core.

## Continuation rule
Read this file first in every new conversation. Do not restart or recreate implemented architecture. Continue from **REAL MAP FORMAT DECODING — CURRENT** and update this file after each major milestone.
