# AI controller boundary

The AI layer is intentionally isolated from the deterministic map engine.

## Language requirement

User-facing natural-language requests must support Arabic as a first-class input language, including Arabic text mixed with English game terms such as `USA`, `China`, `Waypoint`, `BOSS`, `Generals`, and unit/building names.

The AI layer must **not** write `.map` bytes directly. Its output will be a validated, versioned command/document model consumed by the deterministic engine.

## Safety pipeline

```text
Arabic / English user request
        -> language normalization
        -> structured intent extraction
        -> schema validation
        -> deterministic command planner
        -> deterministic engine
        -> map validation
        -> writer
```

An AI provider is optional. The project must remain usable without a remote AI service.
