# WorldBuilder source audit

## Verified upstream source

EA officially released the Generals / Zero Hour source under GPL, and the public repository is `electronicarts/CnC_Generals_Zero_Hour`.

The repository contains the original WorldBuilder source under:

`Generals/Code/Tools/WorldBuilder/`

The WorldBuilder directory contains `include`, `res`, `src`, and `WorldBuilder.dsp`.

## High-value source areas verified

The `src` directory contains dedicated implementations for:

- `WorldBuilderDoc.cpp` — document/model integration.
- `OpenMap.cpp` — map opening workflow.
- `SaveMap.cpp` — map save workflow.
- `WBHeightMap.cpp` — height-map representation/editing.
- `WHeightMapEdit.cpp` — height-map editing UI/operations.
- `ObjectTool.cpp` / `ObjectOptions.cpp` / `ObjectPreview.cpp` — object placement and preview.
- `WaypointTool.cpp` / `WaypointOptions.cpp` — waypoint editing.
- `ScriptDialog.cpp`, `ScriptActionsTrue.cpp`, `ScriptActionsFalse.cpp`, `ScriptConditions.cpp`, `ScriptProperties.cpp` — mission scripting UI/model operations.
- `TerrainMaterial.cpp`, `TerrainModal.cpp`, `TerrainSwatches.cpp`, `TileTool.cpp`, `BlendEdgeTool.cpp` — terrain/material editing.
- `WaterTool.cpp` / `WaterOptions.cpp` — water editing.
- `RoadTool.cpp` / `RoadOptions.cpp` — road editing.
- `MapSettings.cpp` / `MapPreview.cpp` — map settings/preview.
- `playerlistdlg.cpp`, `addplayerdialog.cpp`, `teamsdialog.cpp`, `TeamGeneric.cpp`, `TeamBehavior.cpp`, `TeamIdentity.cpp`, `TeamReinforcement.cpp` — players/teams.

## Important implementation observation

`ObjectTool.cpp` is not merely UI glue: it obtains the current `MapObject`, uses its `ThingTemplate`, calculates placement angle/position, previews the object, and ultimately creates a new map object through the WorldBuilder document undo system. This gives us a direct reference for how the editor's object model is connected to placement operations.

`SaveMap.cpp` confirms that WorldBuilder saves maps into the conventional `Maps/<mapname>/<mapname>.map` layout for its normal map workflow.

## New project strategy

Do not reverse-engineer WorldBuilder.exe unless a source path is genuinely missing. The source itself is the primary behavioral reference.

The project should now maintain two separate evidence classes:

1. `EA_SOURCE_FACT` — behavior directly supported by released WorldBuilder source.
2. `MAP_BINARY_FACT` — behavior directly supported by real `.map` samples.

Only when both agree should a map-format rule be promoted to `VERIFIED_FORMAT_RULE`.

## Planned source-to-project mapping

| WorldBuilder source | sage-map-builder component |
|---|---|
| WorldBuilderDoc / OpenMap / SaveMap | map reader/writer + MapDocument |
| WBHeightMap / WHeightMapEdit | heightmap decoder/editor |
| ObjectTool / ObjectOptions | object decoder/editor |
| WaypointTool / WaypointOptions | waypoint decoder/editor |
| Script* files | mission/script model |
| Terrain* / TileTool | terrain/material model |
| Water* | water model |
| Road* | road model |
| player/team files | player/team model |
| MapSettings | map metadata/settings |

## External build reference

`TheSuperHackers/GeneralsModBuilder` is a separate useful reference for packaging/building Generals Zero Hour mods/addons. It should be integrated as a build/deployment reference, not confused with the map-format decoder.

## Rule

No semantic map-field implementation should be marked complete merely because a variable/class name sounds plausible. We must connect source behavior to binary evidence from the real maps and add a regression test before promoting it.
