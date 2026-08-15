# SAGE `.map` format investigation

## Current verified observations

Two real Zero Hour `.map` samples were supplied for investigation.

- Sample A: 400,054 bytes.
- Sample B: 40,615 bytes.
- Both begin with the ASCII sequence `EAR` followed by binary data.
- Both contain early ASCII strings including `WaypointsList`, `GlobalLighting`, and `PolygonTriggers`.
- The samples are not the same size and do not have identical section contents.

## Important rule

These observations are **not** yet a complete format specification. The parser must not assign meanings to arbitrary offsets until those meanings are verified against multiple samples and, where possible, against known-good game behavior.

## Next investigation steps

1. Build a byte-level section scanner.
2. Compare the two samples and record common and divergent regions.
3. Determine whether the apparent strings are length-delimited, tagged, or part of a serialized object graph.
4. Identify the map header and dimensions using multiple samples.
5. Identify object, waypoint, terrain, lighting, trigger, and script structures independently.
6. Add golden-file tests using the supplied samples.
7. Only then implement a writer, initially with a read/write preservation test.

The project must preserve unknown bytes/sections rather than silently dropping them.
