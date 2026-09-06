#!/usr/bin/env python3
"""Audit a retrieval-first math exercise summary note."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

IMAGE_RE = re.compile(r"!\[\[[^\]\n]+\]\]|!\[[^\]\n]*\]\([^\)\n]+\)")
H2_RE = re.compile(r"^## (?!#)", re.M)
H3_RE = re.compile(r"^### (?!#)", re.M)
SOURCE_RE = re.compile("^(?:> )?(?:Source:|\u6765\u6e90\uff1a)\\s*\\[\\[[^\\]\\n]+\\]\\]", re.M)
BAD_RE = re.compile(r"\\\\u[0-9A-Fa-f]{4}|\?\?\?\?|\[TODO")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--source", required=True, type=Path, action="append")
    parser.add_argument("--expected-items", type=int)
    args = parser.parse_args()

    errors: list[str] = []
    target = read(args.target)
    sources = [read(p) for p in args.source]
    target_images = len(IMAGE_RE.findall(target))
    source_images = sum(len(IMAGE_RE.findall(s)) for s in sources)
    h2 = len(H2_RE.findall(target))
    h3 = len(H3_RE.findall(target))
    source_lines = len(SOURCE_RE.findall(target))

    if h2 == 0:
        errors.append("No level-2 category headings found.")
    if h3 == 0:
        errors.append("No level-3 exercise cards found.")
    if h3 != source_lines:
        errors.append(f"Exercise-card/source-line mismatch: H3={h3}, source-lines={source_lines}.")
    if args.expected_items is not None and h3 != args.expected_items:
        errors.append(f"Expected {args.expected_items} exercise cards, found {h3}.")
    if target_images != source_images:
        errors.append(f"Image count mismatch: sources={source_images}, target={target_images}.")
    if BAD_RE.search(target):
        errors.append("Suspicious encoding artifact or unfinished TODO found in target.")
    for path in args.source:
        stem = path.stem
        if stem not in target:
            errors.append(f"Source note name not found in target: {stem}")

    report = {
        "target": str(args.target),
        "categories": h2,
        "exercise_cards": h3,
        "source_lines": source_lines,
        "source_images": source_images,
        "target_images": target_images,
        "status": "ok" if not errors else "failed",
        "errors": errors,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())