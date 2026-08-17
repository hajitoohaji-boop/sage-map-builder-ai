# SAGE `.map` format investigation

## Current repository samples

The current Git repository contains two binary Zero Hour map samples:

- `MY MAP.map`: 28,712 bytes; Git blob SHA `7d4e1e0b21febd33a460f88a557c4a1e0b3fbb7c`.
- `CONTRA Custom Campaign The Battle for Lake Town.map`: 147,237 bytes; Git blob SHA `b33c1ae19eea4c694bc8398571021e1cf1163e8c`.

These exact files are the golden references for the current investigation.

## Verified observations

- Both samples begin with `45 41 52 00` (`EAR\\0`).
- Both contain `CkMp` at the same relative header position.
- The samples have substantially different sizes and payloads.

## Important rule

These observations are **not** a complete format specification. The parser must not assign meanings to arbitrary offsets until those meanings are verified against multiple samples and, where possible, controlled map edits or known-good game behavior.

## Current investigation tools

- `research/map_samples/probe_map.py`: raw byte/u32 probing.
- `research/map_samples/analyze_probe.py`: comparison-oriented probe analysis.
- `research/map_samples/marker_scan.py`: deterministic marker discovery.
- `research/map_samples/section_evidence.py`: conservative section-boundary evidence.
- `research/map_samples/compare_samples.py`: cross-sample comparison.
- `research/map_samples/controlled_diff.py`: controlled-change byte diff.
- `src/sage_map_builder/format/map_header.py`: conservative prefix observation.
- `src/sage_map_builder/format/marker_index.py`: deterministic marker index.
- `src/sage_map_builder/analysis/controlled_diff.py`: reusable controlled-diff primitive.

## Next investigation steps

1. Run the report/scanner pipeline against the exact golden samples and persist its JSON output.
2. Compare common and divergent regions.
3. Use controlled one-change map pairs to identify fields without guessing.
4. Determine whether observed strings are length-delimited, tagged, or part of a serialized object graph.
5. Identify header/dimensions using multiple samples.
6. Identify object, waypoint, terrain, lighting, trigger, and script structures independently.
7. Add golden-file tests using the supplied samples.
8. Only then implement a production writer, initially with a byte-for-byte preservation round trip.

Unknown bytes/sections must always be preserved rather than silently dropped.
