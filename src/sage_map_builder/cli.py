"""Command-line entry point for deterministic map analysis."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .pipeline.discovery_pipeline import analyze_directory


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze Generals/Zero Hour map samples")
    parser.add_argument("root", type=Path, help="Directory containing .map files")
    parser.add_argument("-o", "--output", type=Path, default=None, help="Write JSON report to this file")
    args = parser.parse_args(argv)
    report = analyze_directory(args.root)
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
