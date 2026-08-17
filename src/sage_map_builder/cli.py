"""Deterministic command-line entry point for map analysis and safe I/O."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .pipeline.discovery_pipeline import analyze_directory
from .report.sample_report import build_sample_report
from .report.compare_report import build_compare_report
from .map.preservation import preserve_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze Generals/Zero Hour map samples")
    sub = parser.add_subparsers(dest="command")

    analyze = sub.add_parser("analyze", help="Analyze all .map files in a directory")
    analyze.add_argument("root", type=Path)
    analyze.add_argument("-o", "--output", type=Path)

    report = sub.add_parser("report", help="Build evidence-only report for one map")
    report.add_argument("map", type=Path)
    report.add_argument("-o", "--output", type=Path, required=True)

    compare = sub.add_parser("compare", help="Compare two map samples without semantic interpretation")
    compare.add_argument("left", type=Path)
    compare.add_argument("right", type=Path)
    compare.add_argument("-o", "--output", type=Path, required=True)

    preserve = sub.add_parser("preserve", help="Write an exact byte-for-byte copy")
    preserve.add_argument("source", type=Path)
    preserve.add_argument("output", type=Path)

    # Backward-compatible invocation: `cli ROOT [-o OUTPUT]`.
    if argv and argv[0] not in {"analyze", "report", "compare", "preserve", "-h", "--help"}:
        argv = ["analyze", *argv]

    args = parser.parse_args(argv)
    command = args.command
    if command is None:
        parser.print_help()
        return 2

    if command == "analyze":
        report_data = analyze_directory(args.root)
        text = json.dumps(report_data, indent=2, ensure_ascii=False) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text, encoding="utf-8")
        else:
            print(text, end="")
    elif command == "report":
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(build_sample_report(args.map), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    elif command == "compare":
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(build_compare_report(args.left, args.right), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    elif command == "preserve":
        result = preserve_file(args.source, args.output)
        print(json.dumps({"identical": result.identical, "source_sha256": result.source_sha256, "output_sha256": result.output_sha256}))
        return 0 if result.identical else 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
