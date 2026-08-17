# SAGE Map Builder AI — Project Status

Last updated: 2026-08-17

## Goal
Build an independent World Builder-style editor for Command & Conquer: Generals – Zero Hour / SAGE maps.

Requirements: the core editor works without AI; Gemini/other AI is optional and separate; the core is deterministic and never guesses unknown binary structures; Arabic descriptions may later use a separate AI adapter; the two supplied map files remain separate reference samples; supplied mod/INI files must eventually drive the asset database; final goal is a usable independent World Builder, not only an analyzer.

## Repository
`hajitoohaji-boop/sage-map-builder-ai`

## Implemented

### Analysis foundation
- Header evidence and header-word extraction.
- Byte-region detection and region layout matching.
- Evidence-preserving MapReader.
- Per-map Section Report JSON.
- Single-map and two-map analysis pipelines.
- Automatic `.map` discovery and discovery pipeline.
- Byte evidence primitives (`ByteEvidence`) with offset, length, SHA-256 and hex preview.

### Verified real samples
The repository tree was checked directly. The two real maps are present in the repository root:

1. `MY MAP.map` — 28,712 bytes — blob SHA `7d4e1e0b21febd33a460f88a557c4a1e0b3fbb7c`.
2. `CONTRA Custom Campaign The Battle for Lake Town.map` — 147,237 bytes — blob SHA `b33c1ae19eea4c694bc8398571021e1cf1163e8c`.

Repository research notes verify for both samples:
- first bytes are `45 41 52 00` (`EAR\\0`)
- marker `CkMp` occurs at the same relative header position
- the samples differ substantially in size and payload

A machine-readable manifest is stored at `research/map_samples/sample_manifest.json`.

Important: the binary blobs are not treated as UTF-8 source files. Analysis must use binary access. No semantic field meaning is assigned from one sample alone.

### Internal model
`MapDocument` contains file name, raw size, optional dimensions, regions, waypoints, objects, scripts, and opaque sections. Unknown binary data is preserved rather than guessed.

### Serialization/edit safety
- Deterministic MapDocument JSON round trip.
- Lossless preservation writer.
- Explicit binary patches with bounds/overlap checks.
- Transactional EditSession with preview/commit/rollback.

### World Builder data model
- Waypoints: validated names/coordinates, optional bounds, duplicate prevention, add/remove.
- Objects: ID, template, X/Y/Z, optional owner, duplicate prevention, add/remove.
- Scripts: MapScript with enabled flag, conditions/actions and generic ScriptAction(kind,args), duplicate prevention, add/remove.
- `MapEditorService`: unified API for these entities plus snapshot-based undo/redo.

## Architecture
```text
REAL .map samples
  -> binary discovery
  -> MapReader / evidence
     -> Header / words / regions / markers
  -> MapDocument
     -> Waypoints / Objects / Scripts / Opaque Sections
  -> MapEditorService
     -> validation / undo / redo
  -> EditSession / Preservation Writer
  -> output .map
```

Separate: MapReader -> Section Report -> Research/Comparison Report.
Separate future AI: Arabic description -> optional AI adapter -> validated commands.

## Next priorities

### 1. REAL MAP FORMAT DECODING — CURRENT
Now that the actual two samples are confirmed in GitHub, work from these exact files and their verified hashes. The next parser work must inspect binary sections/markers and compare both samples. Use controlled evidence and existing research scripts. Do not invent offsets, dimensions, object layouts, or terrain layouts.

### 2. Golden sample tests
Add tests that identify the exact two samples by size/hash and assert verified observations (`EAR\\0`, `CkMp`) without assuming unverified semantic meanings.

### 3. Real semantic decoding
Identify header/dimensions, terrain/height, textures, objects, waypoints, players/teams, scripts/mission data and remaining sections only after cross-sample verification.

### 4. Real binary writer
Encode verified sections while preserving every unknown section byte-for-byte. First goal is an exact read/write preservation test for an untouched sample.

### 5. Mod/INI asset database
Read supplied mod files and build a registry of factions, units, buildings, upgrades, special powers, templates and PlayerTemplate/ownership data. Use actual definitions.

### 6. GUI
Build the independent World Builder interface around MapEditorService: open/save-as, map/terrain view, waypoint/object placement, owner/team selection, script editor, undo/redo, validation panel, mod asset browser, and separate reference-map workspace.

### 7. Mission/script system
Translate common World Builder concepts into validated internal commands and export only when the map representation is verified.

### 8. Arabic optional layer
Keep Arabic handling outside the deterministic core. The editor must work normally without AI.

## Continuation rule
Read this file first in every new conversation. Do not restart or recreate implemented architecture. Continue from **REAL MAP FORMAT DECODING — CURRENT** and update this file after each major milestone.
