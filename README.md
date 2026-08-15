# SAGE Map Builder AI

A clean, deterministic foundation for working with Command & Conquer: Generals – Zero Hour SAGE maps and mission data.

## Project rules

- No generated code is accepted without validation.
- The deterministic engine is the source of truth; AI is only an optional controller.
- SAGE map data is represented with explicit typed models.
- Parsers must preserve unknown data instead of silently discarding it.
- Every new feature should include automated tests.
- Original game/mod files are treated as input data, never modified in place.

## Initial architecture

```text
sage_map_builder_ai/
├── src/
│   └── sage_map_builder/
│       ├── __init__.py
│       └── models/
│           ├── __init__.py
│           └── metadata.py
└── tests/
    └── test_metadata.py
```

This first revision intentionally does **not** attempt to parse `.map` files or generate missions yet. We establish a tested foundation first, then add one subsystem at a time.

## Development

Python 3.11+ is the baseline.

Install the project in editable mode:

```bash
python -m pip install -e .[dev]
```

Run tests:

```bash
python -m pytest
```
