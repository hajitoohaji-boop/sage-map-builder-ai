# SAGE Map Builder AI — Project Status

Last updated: 2026-08-16

## Project goal

Build an independent World Builder-style editor for Command & Conquer: Generals – Zero Hour / SAGE maps.

Core requirements agreed with the project owner:

- The main program must work **without AI**.
- Gemini/other AI is optional and must remain separate from the core application.
- The program must be deterministic and avoid guessing unknown binary structures.
- Arabic descriptions should eventually be supported by a separate AI/translation layer, without making the editor dependent on AI.
- Two map files supplied by the owner are samples/reference data and must remain separate from source code and from each other.
- Mod/INI files must eventually be read so the editor can build maps using the actual mod assets and rules.
- The project should become a usable independent World Builder, not only a map analyzer.

## Repository

GitHub repository: `hajitoohaji-boop/sage-map-builder-ai`

## What has been implemented

### Binary/map analysis foundation

- Header evidence extraction.
- Header word extraction.
- Byte-region detection.
- Region layout matching using width/height/bytes-per-cell candidates.
- Evidence-preserving `MapReader`.
- Unified per-map Section Report JSON.
- Single-map deterministic analysis pipeline.
- Two-map analysis pipeline.
- Automatic `.map` sample discovery.
- Discovery pipeline that analyzes discovered valid maps and reports skipped files.

### Internal map model

`MapDocument` currently contains:

- file name
- raw byte size
- optional dimensions
- regions
- waypoints
- objects
- scripts
- opaque sections

Unknown binary data is intentionally preserved as opaque data rather than guessed.

### Serialization and safe editing

- Deterministic JSON serialization/deserialization for `MapDocument`.
- Lossless preservation writer.
- Explicit binary patches.
- Bounds checking for patches.
- Overlap checking for patches.
- Transactional `EditSession` with preview, commit, and rollback.

### World Builder data model started

#### Waypoints

- `Waypoint` model.
- Numeric coordinates.
- Optional map-bound validation.
- Duplicate-name prevention.
- Add/remove operations.

#### Objects

- `GameObject` model.
- Object ID.
- Template name.
- X/Y/Z coordinates.
- Optional owner.
- Duplicate-object-ID prevention.
- Add/remove operations.

#### Scripts

- `MapScript` model.
- Enabled flag.
- Conditions.
- Actions.
- Generic `ScriptAction(kind, args)` representation.
- Duplicate-script-name prevention.
- Add/remove operations.

Example already covered by tests:

```text
WAVE_1
  Condition: timer_expired(timer=WAVE, seconds=90)
  Action: spawn_team(team=team0001, waypoint=SPAWN)
```

## Important design decision

Do NOT assume that fields such as map dimensions, terrain sections, object records, or script records are understood merely because a pattern looks plausible.

The reader should record evidence and preserve unknown bytes. Semantic decoding is added only after verification against real Generals/Zero Hour map samples or reliable format evidence.

## Current architecture

```text
.map / sample data
       |
       v
 Sample Discovery
       |
       v
    MapReader
       |
       +--> Header Evidence
       +--> Header Words
       +--> Region Detection
       +--> Layout Matching
       |
       v
   MapDocument
       |
       +--> Waypoints
       +--> Objects
       +--> Scripts
       +--> Opaque Sections
       |
       v
   EditSession
       |
       v
 Preservation Writer
       |
       v
   output .map

Separate reporting path:

MapReader -> Section Report -> Research/Comparison Report

Separate future AI path:

Arabic/user description -> optional AI adapter -> validated project commands
                                      |
                                      X  (must NOT be required by core editor)
```

## Files added during the current build

- `src/sage_map_builder/map/region_layout_matcher.py`
- `src/sage_map_builder/map/reader.py`
- `src/sage_map_builder/report/section_report.py`
- `src/sage_map_builder/pipeline/map_pipeline.py`
- `src/sage_map_builder/pipeline/multi_map_pipeline.py`
- `src/sage_map_builder/pipeline/sample_discovery.py`
- `src/sage_map_builder/model/map_document.py`
- `src/sage_map_builder/model/from_reader.py`
- `src/sage_map_builder/model/serialization.py`
- `src/sage_map_builder/map/preservation_writer.py`
- `src/sage_map_builder/model/edit_session.py`
- `src/sage_map_builder/model/waypoint.py`
- `src/sage_map_builder/model/waypoint_store.py`
- `src/sage_map_builder/model/game_object.py`
- `src/sage_map_builder/model/object_store.py`
- `src/sage_map_builder/model/script.py`

Associated tests were added for each implemented area.

## What remains — priority order

### 1. Connect model objects to one editor/domain API

Create a single map-editing service so GUI code does not manipulate raw lists directly.

### 2. Real `.map` semantic decoding

Use the actual supplied Generals/Zero Hour maps and reliable format evidence to identify:

- map header/dimensions
- terrain/height data
- texture information
- object records
- waypoint records
- player/team data
- script/mission data
- remaining sections

Do not guess. Record confidence/evidence for every decoded section.

### 3. Real binary writer

Extend the current preservation writer into a format-aware writer for verified sections while preserving all unknown sections.

### 4. Mod/INI asset database

Read the supplied mod files, including relevant INI structures, and create a local registry/database of:

- factions
- units
- buildings
- upgrades
- weapons/special powers where needed
- object templates
- ownership/player templates

The editor must use the actual mod definitions rather than invented unit names.

### 5. Independent World Builder GUI

Target capabilities:

- Open map
- Save As
- map/terrain view
- waypoint placement/editing
- object placement/editing
- owner/team selection
- script editor
- undo/redo
- validation/errors panel
- mod asset browser
- separate sample/reference-map workspace

### 6. Mission/script system

Translate common World Builder concepts into validated internal commands, then export only when the corresponding binary/script representation is verified.

### 7. Arabic description layer (optional and separate)

Eventually accept Arabic descriptions such as mission/wave/objective descriptions. The AI adapter should produce structured commands that are validated by the deterministic core. If AI is unavailable, the editor must still function normally.

### 8. Real sample-map integration

Automatically discover the two real `.map` files in the repository/workspace, identify them by their actual filenames, and run the full analysis pipeline on them. Never hard-code assumed filenames.

## Current stopping point

The latest completed feature is the neutral mission-script model (`MapScript` / `ScriptAction`) and its tests.

**Next task:** create the unified domain/editor service that manages Waypoints + Objects + Scripts in one `MapDocument`, with validation and undo/redo-ready operations. Then move immediately into real map-format decoding using the actual samples.

## Working rule for future conversations

When continuing this project, read this file first. Do not restart the architecture or recreate already implemented modules. Continue from the "Current stopping point" and update this file whenever a major milestone is completed.
