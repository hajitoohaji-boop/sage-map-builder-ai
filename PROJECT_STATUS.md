# SAGE Map Builder AI — Project Status

Last updated: 2026-08-17

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
- `DataChunk` header corrected from an earlier incorrect 8-byte assumption to the EA-source-supported 4-byte header (`version` + `dataSize`).
- `chunk_sequence.py` preserves opaque payloads and supports lossless chunk-sequence round trip.
- `WaypointsList` codec is source-derived, but full map chunk identity/TOC is not yet verified.
- No semantic chunk name is promoted without both source and binary evidence.

## Mod/asset stack
- BIG archive reader, archive access, INI parser/scanner, asset classification/index and deterministic `ModRegistry` are present.
- `MapGenerationPlan` + validator + compiler are present and keep unknown assets from being silently invented.

## Architecture
```text
REAL .map samples
  -> binary discovery
  -> MapReader / evidence
     -> Header / words / regions / markers
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
Run the evidence/report pipeline against the two exact real samples and persist resulting JSON reports. Then use cross-sample evidence to isolate candidate sections. Do not assign semantic names yet.

### 2. Golden sample tests
Exact size/prefix/marker checks are now covered against the repository manifest; untouched preservation tests cover both real samples when checked out.

### 3. Real semantic decoding
Only after evidence supports it, identify header/dimensions, terrain/height, textures, objects, waypoints, players/teams, scripts/mission data and remaining sections.

### 4. Real binary writer
First prove exact read/write preservation for an untouched sample. Only then write verified sections while preserving unknown bytes byte-for-byte.

### 5. Mod/INI asset database
Read supplied mod files and build a registry of actual factions, units, buildings, upgrades, special powers, templates and PlayerTemplate/ownership data.

### 6. GUI
Build the independent World Builder interface around MapEditorService.

### 7. Mission/script system
Translate common World Builder concepts into validated commands and export only when the map representation is verified.

### 8. Arabic optional layer
Keep Arabic handling outside the deterministic core.

## Continuation rule
Read this file first in every new conversation. Do not restart or recreate implemented architecture. Continue from **REAL MAP FORMAT DECODING — CURRENT** and update this file after each major milestone.
