#!/usr/bin/env python3
"""Simple file-organization automation for a project folder."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import List, Dict

EXTENSION_MAP = {
    ".pdf": "documents",
    ".doc": "documents",
    ".docx": "documents",
    ".txt": "documents",
    ".md": "documents",
    ".csv": "data",
    ".xlsx": "data",
    ".xls": "data",
    ".json": "data",
    ".xml": "data",
    ".png": "images",
    ".jpg": "images",
    ".jpeg": "images",
    ".gif": "images",
    ".webp": "images",
    ".svg": "images",
    ".py": "code",
    ".js": "code",
    ".ts": "code",
    ".html": "code",
    ".css": "code",
    ".zip": "archives",
    ".tar": "archives",
    ".gz": "archives",
    ".rar": "archives",
}

IGNORE_DIRECTORIES = {".git", ".venv"}


def get_target_folder(extension: str) -> str:
    return EXTENSION_MAP.get(extension.lower(), "misc")


def make_unique_path(destination: Path) -> Path:
    if not destination.exists():
        return destination

    counter = 1
    stem = destination.stem
    suffix = destination.suffix
    while True:
        candidate = destination.with_name(f"{stem}_{counter}{suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def organize_folder(source: Path, apply: bool = False) -> List[Dict[str, str]]:
    source = source.resolve()
    report: List[Dict[str, str]] = []

    for item in sorted(source.iterdir()):
        if item.name in IGNORE_DIRECTORIES:
            continue
        if item.is_dir():
            continue
        if not item.is_file():
            continue
        if item.resolve() == Path(__file__).resolve():
            continue

        target_folder = get_target_folder(item.suffix)
        target_dir = source / target_folder
        target_dir.mkdir(exist_ok=True)

        destination = target_dir / item.name
        destination = make_unique_path(destination)

        if apply:
            shutil.move(str(item), str(destination))
            action = "moved"
        else:
            action = "would_move"

        report.append(
            {
                "source": item.name,
                "destination": str(destination.relative_to(source)),
                "action": action,
            }
        )

    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Organize files in a folder by type")
    parser.add_argument(
        "--source",
        default=".",
        help="Folder to scan (defaults to the current directory)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually move files. Without this flag, the script only previews changes.",
    )
    args = parser.parse_args()

    source = Path(args.source).resolve()
    if not source.exists() or not source.is_dir():
        raise SystemExit(f"Folder not found: {source}")

    report = organize_folder(source, apply=args.apply)

    if args.apply:
        print("Automation applied successfully.")
    else:
        print("Preview mode: no files were moved.")

    print(f"Processed {len(report)} files.")
    for entry in report:
        print(f"- {entry['action']}: {entry['source']} -> {entry['destination']}")

    report_path = source / "automation_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Report saved to {report_path}")


if __name__ == "__main__":
    main()
