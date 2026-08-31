#!/usr/bin/env python3
"""Read-only local media inspection; JSON to stdout, never delete or choose keepers."""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import warnings


RASTER = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff"}
SUPPORTED = RASTER | {".svg", ".pdf"}


def linked(path: Path) -> bool:
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0)
        & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    )


def fingerprint(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect(root: Path, max_pixels: int) -> dict:
    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError("Pillow is required; use a runtime that already provides it.") from exc

    records = []
    exclusions = []
    issues = []
    buckets = defaultdict(list)

    def traversal_error(exc):
        try:
            label = Path(exc.filename).relative_to(root).as_posix()
        except (TypeError, ValueError):
            label = "."
        issues.append({"path": label, "problem": type(exc).__name__})

    for parent, dirs, names in os.walk(root, followlinks=False, onerror=traversal_error):
        directory = Path(parent)
        for name in sorted(dirs[:]):
            child = directory / name
            try:
                skip = linked(child)
            except OSError as exc:
                skip = True
                issues.append({"path": child.relative_to(root).as_posix(),
                               "problem": type(exc).__name__})
            if skip:
                dirs.remove(name)
                exclusions.append(child.relative_to(root).as_posix())
        for name in sorted(names):
            path = directory / name
            if path.suffix.lower() not in SUPPORTED:
                continue
            relative = path.relative_to(root).as_posix()
            try:
                if (linked(path) or not stat.S_ISREG(path.lstat().st_mode)
                        or not path.resolve().is_relative_to(root)):
                    exclusions.append(relative)
                    continue
                before = path.stat()
                record = {"path": relative, "size_bytes": before.st_size,
                          "digest": fingerprint(path), "inspection": "digest_only"}
                if path.suffix.lower() in RASTER:
                    with warnings.catch_warnings():
                        warnings.simplefilter("error", Image.DecompressionBombWarning)
                        with Image.open(path) as raster:
                            frames = getattr(raster, "n_frames", 1)
                            record.update(format=raster.format, width=raster.width,
                                          height=raster.height, frames=frames)
                            for frame in range(frames):
                                raster.seek(frame)
                                if raster.width * raster.height > max_pixels:
                                    raise ValueError("pixel_limit_exceeded")
                                raster.load()
                            record["inspection"] = "all_frames_decoded"
                after = path.stat()
                if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                    raise RuntimeError("file_changed_during_inspection")
                records.append(record)
                buckets[record["digest"]].append(relative)
            except Exception as exc:
                issue = {"path": relative, "problem": type(exc).__name__}
                if type(exc) in (ValueError, RuntimeError) and exc.args in (
                    ("pixel_limit_exceeded",), ("file_changed_during_inspection",)
                ):
                    issue["detail"] = exc.args[0]
                issues.append(issue)

    return {
        "files": sorted(records, key=lambda item: item["path"]),
        "byte_identical_groups": [sorted(paths) for _, paths in sorted(buckets.items()) if len(paths) > 1],
        "skipped_links": sorted(exclusions),
        "issues": issues,
        "scope_notes": [
            "No quality ranking or removal recommendation is made.",
            "Only known raster/PDF/SVG suffixes are inspected; source records must cover other media.",
            "PDF/SVG are hashed only; their contents are not decoded or compared.",
            "Document containers, remote assets, and references are not inspected.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="Exact local archive directory to inspect")
    parser.add_argument("--max-pixels", type=int, default=80_000_000,
                        help="Maximum pixels per raster frame (default: 80000000)")
    args = parser.parse_args()
    if args.max_pixels < 1:
        parser.error("--max-pixels must be positive")
    root = args.directory.expanduser().resolve()
    if not root.is_dir():
        parser.error("directory must exist")
    try:
        report = inspect(root, args.max_pixels)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["issues"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
