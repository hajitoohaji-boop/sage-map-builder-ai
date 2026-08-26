# SAGE MAP format completion status

This project must not claim full completion from source code alone.

## Completion contract

A subsystem is complete only when its source structure, real MAP sample evidence,
and lossless round-trip behavior agree. The completion gate is intentionally
fail-closed.

## Current verified surface

- `DataChunk`: source + binary verified.

## Remaining format work

- `WaypointsList`: source-backed, needs real-sample binary matching.
- `HeightMapData`: source available, binary layout not verified.
- `BlendTileData` / terrain: binary layout not verified.
- `WorldInfo`: binary layout not verified.
- `ObjectsList` and nested `Object`: binary layout not verified.
- `GlobalLighting`: binary layout not verified.
- Scripts / players / water / roads / textures: source available, binary verification pending.
- Full writer: partial until all required chunks can be emitted and round-tripped.

## Rule

Do not raise the completion percentage merely because helper modules were added.
The percentage should increase materially when a real chunk layout is decoded,
encoded, and round-tripped against real MAP samples.
