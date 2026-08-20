# SAGE Map Builder AI — Project Status

Last updated: 2026-08-20

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
- Batch source-evidence classification and deterministic evidence summaries.
- Position-independent cross-sample alignment of equal source-backed label/version occurrences.
- Golden-file integrity tests and a standalone validator for the two real map samples.
- Versioned natural-language request boundary and conservative Arabic/English request parsing for explicit dimensions only.
- Deterministic bridge from `MapRequest` to the existing `MapGenerationPlan`; it validates the plan and deliberately leaves non-explicit map details empty rather than inventing them.
- Deterministic extraction of an explicitly stated objective into `MapGenerationPlan.intent.objectives`; no placements, waves or scripts are invented.
- Explicit-fact extraction for labeled `factions`, `players`, `constraints`, and `objective`/`هدف` fields; prose such as “American and Chinese forces” is deliberately not converted into faction IDs.
- Mission-fact integration into `request_to_plan`: explicitly labeled factions/objectives now populate the existing plan intent and mission objective fields without inventing waves, scripts, placements, or asset IDs.

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

## AI request boundary (2026-08-20)
Added:
- `ai/request.py`: versioned `MapRequest` boundary. It keeps natural-language input outside the deterministic engine and validates only the request envelope.
- `ai/request_parser.py`: conservative parser that detects Arabic vs English and extracts only explicitly written `WIDTHxHEIGHT` dimensions. It deliberately does not invent factions, objects, terrain, scripts, or assets.
- `tests/test_request_parser.py`: verifies Arabic/English detection, explicit dimension extraction, and deterministic defaults.
- `ai/request_to_plan.py`: deterministic bridge from the request parser into the existing `MapGenerationPlan`. It validates the resulting plan and leaves placements/mission details empty unless another evidence-backed planner supplies them.
- `tests/test_request_to_plan.py`: verifies explicit dimensions, title hints, and the absence of invented placements/scripts/waves/objectives.
- `ai/plan_extraction.py`: conservative explicit-fact extraction layer; currently adds only an explicitly written `objective:` / `هدف:` to the existing plan intent while preserving unknown requirements as unresolved natural language.
- `tests/test_plan_extraction.py`: verifies Arabic dimensions/objective extraction and confirms that a vague request does not invent placements, scripts or waves.
- `ai/explicit_facts.py`: extracts only explicitly labeled factions/players/constraints/objective fields from the request text; it never maps natural-language faction names to mod IDs.
- `tests/test_explicit_facts.py`: verifies explicit faction/constraint extraction and the deliberate non-inference behavior for ordinary prose.
- `ai/mission_facts.py`: extracts explicitly labeled mission fields and safely applies complete player/faction pairs and objectives to a `MissionPlan`; it does not infer facts from ordinary prose.
- `tests/test_mission_facts.py`: verifies explicit mission extraction and non-inference.
- `tests/test_request_to_plan_mission_facts.py`: verifies that explicit faction/objective facts now flow through the request-to-plan bridge without creating waves or placements.

This is intentionally still a conservative AI boundary. It does **not** claim that arbitrary natural language can yet be converted into a complete map. The existing deterministic `MapGenerationPlan`/compiler remains the execution boundary.

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
2. Use position-independent marker alignment before interpreting any offset deltas.
3. Match source-backed labels/versions to real byte ranges using controlled binary evidence.
4. Audit remaining WorldBuilder save helpers, especially heightmap, world info, objects and helper-emitted chunks.
5. Decode the first newly verified semantic chunk.
6. Prove untouched-map lossless round trip, then verified editing/writing.
7. Expand mod/INI asset database.
8. Expand the AI request parser into structured intent extraction only when backed by deterministic schema/tests, then connect it to the existing `MapGenerationPlan`.
9. Build GUI only after binary core is reliable.

## Integrity note
GitHub Actions exists for pytest, but no completed CI run is currently exposed by the connector; CI is therefore not claimed as passing.
