#!/usr/bin/env python3
"""Regenerate the complete v1.7.1 release inventory and checksum closure.

The manifest lists every repository file except the two root inventory files.
The checksum file lists every repository file except itself, so it also seals
the newly written manifest. Git metadata, symbolic links, and cache bytecode
are rejected.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.tsv"
CHECKSUMS = ROOT / "SHA256SUMS.txt"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inventory() -> list[Path]:
    result: list[Path] = []
    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        rel = path.relative_to(ROOT)
        if path.is_symlink():
            raise RuntimeError(f"symbolic links are not permitted: {rel.as_posix()}")
        if path.is_file():
            if "__pycache__" in rel.parts or path.suffix == ".pyc":
                raise RuntimeError(f"cache bytecode is not permitted: {rel.as_posix()}")
            result.append(path)
    return sorted(result, key=lambda item: item.relative_to(ROOT).as_posix())


def category(rel: Path) -> str:
    first = rel.parts[0]
    categories = {
        "ANALYSIS_OUTPUTS": "ANALYSIS_OUTPUT",
        "FIGURE_SOURCE_DATA": "FIGURE_SOURCE_DATA",
        "MANUSCRIPT": "MANUSCRIPT",
        "POST_SYNTHESIS_VALIDATION": "POST_SYNTHESIS_VALIDATION",
        "PROVENANCE": "PROVENANCE",
        "REPRODUCTION": "REPRODUCTION",
        "TABLES": "PUBLICATION_TABLE",
        "tools": "TOOL",
        ".github": "GITHUB_CONFIGURATION",
    }
    return categories.get(first, "ROOT_DOCUMENTATION")


def atomic_write(path: Path, text: str) -> None:
    encoded = text.encode("utf-8")
    with tempfile.NamedTemporaryFile(
        mode="wb", prefix=f".{path.name}.", dir=path.parent, delete=False
    ) as handle:
        temp_path = Path(handle.name)
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())
    try:
        os.replace(temp_path, path)
    finally:
        temp_path.unlink(missing_ok=True)
    path.chmod(0o644)


def expected_manifest(files: list[Path]) -> str:
    excluded = {MANIFEST.resolve(), CHECKSUMS.resolve()}
    lines = ["PATH\tBYTES\tSHA256\tCATEGORY"]
    for path in files:
        if path.resolve() in excluded:
            continue
        rel = path.relative_to(ROOT)
        lines.append(
            f"{rel.as_posix()}\t{path.stat().st_size}\t{sha256(path)}\t{category(rel)}"
        )
    return "\n".join(lines) + "\n"


def expected_checksums(files: list[Path]) -> str:
    lines: list[str] = []
    for path in files:
        if path.resolve() == CHECKSUMS.resolve():
            continue
        rel = path.relative_to(ROOT).as_posix()
        lines.append(f"{sha256(path)}  {rel}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare the existing inventory files instead of rewriting them",
    )
    args = parser.parse_args()

    files = inventory()
    manifest_text = expected_manifest(files)
    if args.check:
        manifest_ok = MANIFEST.is_file() and MANIFEST.read_text(encoding="utf-8") == manifest_text
        checksum_text = expected_checksums(inventory())
        checksums_ok = (
            CHECKSUMS.is_file()
            and CHECKSUMS.read_text(encoding="utf-8") == checksum_text
        )
        print(f"MANIFEST_CURRENT = {'PASS' if manifest_ok else 'FAIL'}")
        print(f"SHA256SUMS_CURRENT = {'PASS' if checksums_ok else 'FAIL'}")
        return 0 if manifest_ok and checksums_ok else 1

    atomic_write(MANIFEST, manifest_text)
    atomic_write(CHECKSUMS, expected_checksums(inventory()))
    final_files = inventory()
    manifest_records = len(final_files) - 2
    checksum_records = len(final_files) - 1
    print(f"REPOSITORY_RELEASE_FILES = {len(final_files)}")
    print(f"MANIFEST_RECORDS = {manifest_records}")
    print(f"SHA256SUMS_RECORDS = {checksum_records}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
