# Autonomous Build Rules

## Purpose
Continue implementation in verified batches without waiting for a user message between every small step.

## Rules
1. Read `PROJECT_STATUS.md` and the latest continuation checkpoint before changing architecture.
2. Inspect existing files before creating a new one; never duplicate an existing responsibility.
3. Prefer several small, connected files in one verified batch over one speculative large subsystem.
4. A new semantic binary codec requires explicit EA World Builder source evidence plus binary evidence. Source class names alone are insufficient.
5. Unknown or unsupported payloads must remain opaque and byte-preserving.
6. Never claim tests passed unless an actual test runner produced a result. GitHub file creation success is not test success.
7. Do not change the project percentage merely because file count increased.
8. After each batch, update the continuation checkpoint/status with exact files and commits when useful.
9. The current priority remains verified `.map` decoding, then lossless semantic editing, then a game-compatible writer, then editor/AI integration.

## Current verified dispatch model
`IdentifiedChunk -> ChunkCodecRegistry -> verified codec OR OpaqueCodec`.
Semantic identity must come from the evidence layer; dispatch never guesses it from payload bytes.
