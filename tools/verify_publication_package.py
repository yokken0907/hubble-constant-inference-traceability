#!/usr/bin/env python3
"""Verify release integrity, manifest coverage, and frozen Table 2 traceability."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CHECKSUM_FILE = ROOT / "SHA256SUMS.txt"
MANIFEST_FILE = ROOT / "MANIFEST.tsv"
TABLE2_FILE = ROOT / "TABLES/TABLE2_NUMERICAL_RESULTS.tsv"
REGISTER_FILE = ROOT / "PROVENANCE/PRINCIPAL_NUMERICAL_RESULTS_VALIDATION.tsv"
DIRECT_FILE = ROOT / "PROVENANCE/DIRECT_NUMERICAL_VALIDATION_REPORT.tsv"
MAPPING_FILE = ROOT / "PROVENANCE/TABLE2_NUMBER_ID_VALIDATION.tsv"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def release_files() -> set[str]:
    return {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts
    }


def parse_checksums() -> dict[str, str]:
    records: dict[str, str] = {}
    for line_number, line in enumerate(CHECKSUM_FILE.read_text(encoding="utf-8").splitlines(), 1):
        text = line.strip()
        if not text:
            raise ValueError(f"blank checksum line {line_number}")
        expected, relative_path = text.split(maxsplit=1)
        relative_path = relative_path.lstrip("* ")
        if len(expected) != 64 or any(ch not in "0123456789abcdef" for ch in expected.lower()):
            raise ValueError(f"invalid SHA-256 at line {line_number}")
        if relative_path in records:
            raise ValueError(f"duplicate checksum path: {relative_path}")
        records[relative_path] = expected.lower()
    return records


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="	"))


def main() -> int:
    required = [CHECKSUM_FILE, MANIFEST_FILE, TABLE2_FILE, REGISTER_FILE, DIRECT_FILE, MAPPING_FILE]
    missing_required = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing_required:
        print("ERROR: missing required files: " + ", ".join(missing_required), file=sys.stderr)
        return 2

    try:
        checksums = parse_checksums()
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    files = release_files()
    expected_checksum_paths = files - {"SHA256SUMS.txt"}
    missing_checksum_members = sorted(expected_checksum_paths - set(checksums))
    extra_checksum_members = sorted(set(checksums) - expected_checksum_paths)

    hash_failures = []
    for relative_path, expected in checksums.items():
        target = ROOT / relative_path
        if not target.is_file():
            hash_failures.append((relative_path, "MISSING", expected, ""))
            continue
        actual = sha256(target)
        if actual != expected:
            hash_failures.append((relative_path, "MISMATCH", expected, actual))

    manifest_rows = read_tsv(MANIFEST_FILE)
    manifest_paths = [row.get("PATH", "") for row in manifest_rows]
    duplicate_manifest_paths = sorted({p for p in manifest_paths if p and manifest_paths.count(p) > 1})
    applicable_manifest_paths = files - {"MANIFEST.tsv", "SHA256SUMS.txt"}
    missing_manifest_members = sorted(applicable_manifest_paths - set(manifest_paths))
    extra_manifest_members = sorted(set(manifest_paths) - applicable_manifest_paths)
    manifest_failures = []
    for row in manifest_rows:
        rel = row.get("PATH", "")
        target = ROOT / rel
        if not rel or not target.is_file():
            manifest_failures.append((rel, "MISSING"))
            continue
        if row.get("BYTES") != str(target.stat().st_size) or row.get("SHA256") != sha256(target):
            manifest_failures.append((rel, "SIZE_OR_HASH_MISMATCH"))

    table = read_tsv(TABLE2_FILE)
    register = read_tsv(REGISTER_FILE)
    direct = read_tsv(DIRECT_FILE)
    mapping = read_tsv(MAPPING_FILE)
    expected_ids = [f"N{i:03d}" for i in range(1, 47)]
    table_ids = [row.get("NUMBER_ID", "") for row in table]
    register_ids = [row.get("NUMBER_ID", "") for row in register]
    publication_rows = [row.get("PUBLICATION_TABLE_ROW", "") for row in register]
    direct_ids = [row.get("NUMBER_ID", "") for row in direct]
    mapping_ids = [row.get("NUMBER_ID", "") for row in mapping]

    id_pass = (
        table_ids == expected_ids
        and register_ids == expected_ids
        and publication_rows == expected_ids
        and direct_ids == expected_ids
        and mapping_ids == expected_ids
        and len(set(table_ids)) == 46
    )
    frozen_validation_pass = (
        all(row.get("CHECK_1_MANUSCRIPT_TO_TABLE") == "PASS" for row in register)
        and all(row.get("CHECK_2_TABLE_TO_ARTIFACT") == "PASS" for row in register)
        and all(row.get("FINAL_RESULT") == "PASS" for row in direct)
        and all(row.get("NUMBER_ID_MAPPING_STATUS") == "PASS" for row in mapping)
        and all(row.get("SCIENTIFIC_VALUE_CHANGED") == "NO" for row in mapping)
    )

    print(f"RELEASE_FILE_COUNT = {len(files)}")
    print(f"CHECKSUM_RECORD_COUNT = {len(checksums)}")
    print(f"SHA256SUMS_MATCH = {'ALL' if not hash_failures else 'FAIL'}")
    print(f"MISSING_CHECKSUM_MEMBER = {len(missing_checksum_members)}")
    print(f"EXTRA_CHECKSUM_MEMBER = {len(extra_checksum_members)}")
    print(f"MANIFEST_RECORD_COUNT = {len(manifest_rows)}")
    print(f"MISSING_MANIFEST_MEMBER = {len(missing_manifest_members)}")
    print(f"EXTRA_MANIFEST_MEMBER = {len(extra_manifest_members)}")
    print(f"DUPLICATE_MANIFEST_PATH = {len(duplicate_manifest_paths)}")
    print(f"MANIFEST_CONTENT_FAILURE = {len(manifest_failures)}")
    print(f"NUMBER_ID_COUNT = {len(table_ids)}")
    print(f"NUMBER_ID_UNIQUE = {len(set(table_ids))}")
    print(f"NUMBER_ID_RANGE = {table_ids[0] if table_ids else 'NONE'}-{table_ids[-1] if table_ids else 'NONE'}")
    print(f"NUMBER_ID_MAPPING = {'PASS' if id_pass else 'FAIL'}")
    print(f"FROZEN_NUMERICAL_VALIDATION = {'PASS' if frozen_validation_pass else 'FAIL'}")

    failures = (
        hash_failures or missing_checksum_members or extra_checksum_members
        or missing_manifest_members or extra_manifest_members or duplicate_manifest_paths
        or manifest_failures or not id_pass or not frozen_validation_pass
    )
    if failures:
        for item in hash_failures:
            print("HASH_FAILURE", *item, sep="	")
        for item in missing_checksum_members:
            print("MISSING_CHECKSUM", item, sep="	")
        for item in extra_checksum_members:
            print("EXTRA_CHECKSUM", item, sep="	")
        for item in missing_manifest_members:
            print("MISSING_MANIFEST", item, sep="	")
        for item in extra_manifest_members:
            print("EXTRA_MANIFEST", item, sep="	")
        for item in duplicate_manifest_paths:
            print("DUPLICATE_MANIFEST", item, sep="	")
        for item in manifest_failures:
            print("MANIFEST_FAILURE", *item, sep="	")
        return 1

    print("PUBLICATION_PACKAGE_INTEGRITY = PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
