# Reference map samples

These two binary maps are reference material for reverse-engineering the SAGE/Zero Hour map format. They are **not application assets** and must not be loaded by the production map generator automatically.

## Samples currently stored in the repository root

1. `MY MAP.map` — user's map sample, 28,712 bytes.
2. `CONTRA Custom Campaign The Battle for Lake Town.map` — reference mission map, 147,237 bytes.

Their paired `.tga` files are also present at the repository root and are reference images only.

## Analysis rule

Do not infer field meanings from one sample alone. Every map-format field must be confirmed by comparison between both samples and, where possible, additional controlled map edits. The binary writer must not be implemented from guesses.

## Initial verified observation

Both samples begin with the same `EAR\x00` prefix and contain the ASCII marker `CkMp` at the same relative header position. Their following bytes differ, so dimensions/metadata must be decoded from controlled comparisons rather than assumed.

## Separation note

The current GitHub connector can create UTF-8 files but does not provide a binary move operation. Therefore the original binary samples remain untouched in the repository root for now; this directory is the isolated research manifest and analysis area. They must not be imported by the production package.
