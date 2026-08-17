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

### NEW: Unified editor domain service
Added:
- `src/sage_map_builder/model/editor_service.py`
- `tests/test_editor_service.py`

`MapEditorService` is now the single API for GUI/CLI code to modify Waypoints, Objects and Scripts. It provides add/remove operations plus snapshot-based undo/redo. GUI code must not manipulate raw lists directly.

Commits:
- `97af4d821ca02094da398a603c9cd4106d767ea5` — service
- `c5520bf7ff7aeb5b9a710d792154df4154491202` — tests

## Architecture
```text
.map / samples
  -> Sample Discovery
  -> MapReader
     -> Header Evidence / Header Words / Regions / Layout Matching
  -> MapDocument
     -> Waypoints / Objects / Scripts / Opaque Sections
  -> MapEditorService
     -> validation / undo / redo
  -> EditSession / Preservation Writer
  -> output .map

Separate: MapReader -> Section Report -> Research/Comparison Report
Separate future AI: Arabic description -> optional AI adapter -> validated commands
```

## Next priorities

### 1. REAL MAP FORMAT DECODING — NEXT
Use the actual Generals/Zero Hour `.map` samples in the repository/workspace and reliable format evidence to identify header/dimensions, terrain/height, textures, objects, waypoints, players/teams, scripts/mission data and remaining sections. Never label a section from a guess; preserve unknown bytes and attach evidence/confidence.

### 2. Real binary writer
Encode verified sections while preserving every unknown section byte-for-byte.

### 3. Mod/INI asset database
Read supplied mod files and build a registry of factions, units, buildings, upgrades, special powers, templates and PlayerTemplate/ownership data. Use actual definitions.

### 4. GUI
Build the independent World Builder interface around MapEditorService: open/save-as, map/terrain view, waypoint/object placement, owner/team selection, script editor, undo/redo, validation panel, mod asset browser, and separate reference-map workspace.

### 5. Mission/script system
Translate common World Builder concepts into validated internal commands and export only when the map representation is verified.

### 6. Arabic optional layer
Keep Arabic handling outside the deterministic core. The editor must work normally without AI.

### 7. Real sample integration
Automatically discover the two actual `.map` samples by extension and verified header; never hard-code filenames.

## Continuation rule
Read this file first in every new conversation. Do not restart or recreate implemented architecture. Continue from **REAL MAP FORMAT DECODING — NEXT** and update this file after each major milestone.
