#!/usr/bin/env python3
"""Verify release integrity, frozen v1.5.5 content, and post-synthesis V001 evidence."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CHECKSUM_FILE = ROOT / "SHA256SUMS.txt"
MANIFEST_FILE = ROOT / "MANIFEST.tsv"
TABLE2_FILE = ROOT / "TABLES/TABLE2_NUMERICAL_RESULTS.tsv"
NUMBER_REGISTER_FILE = ROOT / "PROVENANCE/PRINCIPAL_NUMERICAL_RESULTS_VALIDATION.tsv"
DIRECT_FILE = ROOT / "PROVENANCE/DIRECT_NUMERICAL_VALIDATION_REPORT.tsv"
MAPPING_FILE = ROOT / "PROVENANCE/TABLE2_NUMBER_ID_VALIDATION.tsv"
STATEMENT_FILE = ROOT / "PROVENANCE/STATEMENT_TO_EVIDENCE_REGISTER.tsv"
VALIDATION_REGISTER_FILE = ROOT / "PROVENANCE/POST_SYNTHESIS_VALIDATION_REGISTER.tsv"
PRESERVATION_FILE = ROOT / "PROVENANCE/V1_5_5_PRESERVATION_RECORD.tsv"
V001_EVIDENCE_FILE = ROOT / "PROVENANCE/V001_EVIDENCE_PATHS.tsv"
V001_DIR = ROOT / "POST_SYNTHESIS_VALIDATION/tdcosmo_second_implementation"
V001_LOCAL_SUMS = V001_DIR / "SHA256SUMS.txt"
V001_FINAL_SUMMARY = V001_DIR / "FINAL_RESULT_SUMMARY.tsv"
V001_STRUCTURAL = V001_DIR / "STRUCTURAL_COMPARISON_13_CHAINS.tsv"
V001_NUMERICAL = V001_DIR / "NUMERICAL_COMPARISON_13_CHAINS.tsv"
V001_TABLE6 = V001_DIR / "TABLE6_PUBLISHED_PRECISION_COMPARISON.tsv"
V001_FREEZE = V001_DIR / "METHOD_FREEZE_RECORD.json"
V001_CODE = V001_DIR / "run_audit.py"

EXPECTED_IMPLEMENTATION_SHA256 = "6360c803c584cc29e939445001fa6508cd875d16b4cdba5caba8be8b031368f7"


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


def parse_checksums(path: Path) -> dict[str, str]:
    records: dict[str, str] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        text = line.strip()
        if not text:
            raise ValueError(f"blank checksum line {line_number} in {path}")
        expected, relative_path = text.split(maxsplit=1)
        relative_path = relative_path.lstrip("* ")
        if len(expected) != 64 or any(ch not in "0123456789abcdef" for ch in expected.lower()):
            raise ValueError(f"invalid SHA-256 at line {line_number} in {path}")
        if relative_path in records:
            raise ValueError(f"duplicate checksum path in {path}: {relative_path}")
        records[relative_path] = expected.lower()
    return records


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def truth(value: str) -> bool:
    return value.strip().lower() in {"true", "pass", "yes", "1"}


def main() -> int:
    required = [
        CHECKSUM_FILE, MANIFEST_FILE, TABLE2_FILE, NUMBER_REGISTER_FILE,
        DIRECT_FILE, MAPPING_FILE, STATEMENT_FILE, VALIDATION_REGISTER_FILE,
        PRESERVATION_FILE, V001_EVIDENCE_FILE, V001_LOCAL_SUMS, V001_FINAL_SUMMARY,
        V001_STRUCTURAL, V001_NUMERICAL, V001_TABLE6, V001_FREEZE, V001_CODE,
    ]
    missing_required = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing_required:
        print("ERROR: missing required files: " + ", ".join(missing_required), file=sys.stderr)
        return 2

    try:
        checksums = parse_checksums(CHECKSUM_FILE)
        local_checksums = parse_checksums(V001_LOCAL_SUMS)
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
        else:
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
        elif row.get("BYTES") != str(target.stat().st_size) or row.get("SHA256") != sha256(target):
            manifest_failures.append((rel, "SIZE_OR_HASH_MISMATCH"))

    # Local V001 checksums use paths relative to V001_DIR.
    local_files = {
        path.relative_to(V001_DIR).as_posix()
        for path in V001_DIR.rglob("*")
        if path.is_file()
    }
    expected_local_paths = local_files - {"SHA256SUMS.txt"}
    missing_local = sorted(expected_local_paths - set(local_checksums))
    extra_local = sorted(set(local_checksums) - expected_local_paths)
    local_failures = []
    for rel, expected in local_checksums.items():
        target = V001_DIR / rel
        if not target.is_file():
            local_failures.append((rel, "MISSING"))
        elif sha256(target) != expected:
            local_failures.append((rel, "MISMATCH"))

    table = read_tsv(TABLE2_FILE)
    number_register = read_tsv(NUMBER_REGISTER_FILE)
    direct = read_tsv(DIRECT_FILE)
    mapping = read_tsv(MAPPING_FILE)
    statements = read_tsv(STATEMENT_FILE)
    validations = read_tsv(VALIDATION_REGISTER_FILE)
    preservation = read_tsv(PRESERVATION_FILE)
    v001_evidence = read_tsv(V001_EVIDENCE_FILE)

    expected_ids = [f"N{i:03d}" for i in range(1, 47)]
    table_ids = [row.get("NUMBER_ID", "") for row in table]
    register_ids = [row.get("NUMBER_ID", "") for row in number_register]
    publication_rows = [row.get("PUBLICATION_TABLE_ROW", "") for row in number_register]
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
        all(row.get("CHECK_1_MANUSCRIPT_TO_TABLE") == "PASS" for row in number_register)
        and all(row.get("CHECK_2_TABLE_TO_ARTIFACT") == "PASS" for row in number_register)
        and all(row.get("FINAL_RESULT") == "PASS" for row in direct)
        and all(row.get("NUMBER_ID_MAPPING_STATUS") == "PASS" for row in mapping)
        and all(row.get("SCIENTIFIC_VALUE_CHANGED") == "NO" for row in mapping)
    )

    statement_ids = [row.get("STATEMENT_ID", "") for row in statements]
    c026 = next((r for r in statements if r.get("STATEMENT_ID") == "C026"), {})
    c027 = next((r for r in statements if r.get("STATEMENT_ID") == "C027"), {})
    historical_pass = (
        statement_ids == [f"C{i:03d}" for i in range(1, 31)]
        and c026.get("NUMERICAL_ANCHOR") == "alternate_implementation=NOT_DONE"
        and c026.get("INDEPENDENCE_CLASS") == "ALTERNATE_IMPLEMENTATION_NOT_DONE"
        and c027.get("NUMERICAL_ANCHOR") == "current=HOLD_G0_AND_PAPER_VERSION_INCOMPLETE"
        and c027.get("INDEPENDENCE_CLASS") == "PATCH_VALIDATION_ONLY_NO_SCIENCE_RERUN"
    )

    preservation_failures = []
    for row in preservation:
        rel = row.get("PATH", "")
        target = ROOT / rel
        actual = sha256(target) if target.is_file() else ""
        if (
            not target.is_file()
            or row.get("STATUS") != "UNCHANGED"
            or row.get("V1_5_5_SHA256") != row.get("V1_6_0_SHA256")
            or row.get("V1_6_0_SHA256") != actual
        ):
            preservation_failures.append(rel)


    evidence_failures = []
    for row in v001_evidence:
        rel = row.get("EVIDENCE_PATH", "")
        target = ROOT / rel
        if (
            row.get("VALIDATION_ID") != "V001"
            or not target.is_file()
            or row.get("SHA256") != sha256(target)
        ):
            evidence_failures.append(rel)
    v001_evidence_pass = len(v001_evidence) >= 1 and not evidence_failures

    v001 = next((r for r in validations if r.get("VALIDATION_ID") == "V001"), {})
    v001_register_pass = (
        len(validations) == 1
        and bool(v001)
        and "13/13 structural comparisons passed" in v001.get("RESULT", "")
        and "39/39 q16/q50/q84 comparisons passed" in v001.get("RESULT", "")
        and "12/12 Table 6 rows matched" in v001.get("RESULT", "")
        and "Not external independent replication" in v001.get("INTERPRETATION_LIMIT", "")
        and "C026 and C027" in v001.get("HISTORICAL_PREDECESSOR_RECORD", "")
    )

    summary = {r.get("metric", ""): r for r in read_tsv(V001_FINAL_SUMMARY)}
    summary_pass = (
        summary.get("extension_structural_comparisons", {}).get("value") == "13/13"
        and summary.get("extension_structural_comparisons", {}).get("status") == "PASS"
        and summary.get("extension_quantiles_within_preregistered_tolerance", {}).get("value") == "39/39"
        and summary.get("extension_quantiles_within_preregistered_tolerance", {}).get("status") == "PASS"
        and summary.get("table6_rows_at_published_precision", {}).get("value") == "12/12"
        and summary.get("table6_rows_at_published_precision", {}).get("status") == "PASS"
        and summary.get("branch_status", {}).get("value") == "COMPLETE_WITH_SCOPE"
    )

    structural = read_tsv(V001_STRUCTURAL)
    structural_pass = (
        len(structural) == 13
        and all(r.get("structural_status") == "PASS" for r in structural)
        and all(truth(r.get("all_structural_checks_pass", "")) for r in structural)
    )

    numerical = read_tsv(V001_NUMERICAL)
    tolerance_fields = [
        "q16_within_preregistered_tolerance",
        "q50_within_preregistered_tolerance",
        "q84_within_preregistered_tolerance",
    ]
    quantile_pass_count = sum(truth(r.get(field, "")) for r in numerical for field in tolerance_fields)
    numerical_pass = len(numerical) == 13 and quantile_pass_count == 39

    table6 = read_tsv(V001_TABLE6)
    table6_pass = len(table6) == 12 and all(truth(r.get("all_published_values_match", "")) for r in table6)

    code_hash_pass = sha256(V001_CODE) == EXPECTED_IMPLEMENTATION_SHA256

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
    print(f"V001_LOCAL_SHA256SUMS_MATCH = {'ALL' if not local_failures else 'FAIL'}")
    print(f"V001_LOCAL_MISSING_MEMBER = {len(missing_local)}")
    print(f"V001_LOCAL_EXTRA_MEMBER = {len(extra_local)}")
    print(f"ORIGINAL_CLAIM_COUNT = {len(statement_ids)}")
    print(f"HISTORICAL_NOT_DONE_PRESERVED = {'PASS' if historical_pass else 'FAIL'}")
    print(f"NUMBER_ID_COUNT = {len(table_ids)}")
    print(f"NUMBER_ID_UNIQUE = {len(set(table_ids))}")
    print(f"NUMBER_ID_RANGE = {table_ids[0] if table_ids else 'NONE'}-{table_ids[-1] if table_ids else 'NONE'}")
    print(f"NUMBER_ID_MAPPING = {'PASS' if id_pass else 'FAIL'}")
    print(f"FROZEN_NUMERICAL_VALIDATION = {'PASS' if frozen_validation_pass else 'FAIL'}")
    print(f"V1_5_5_SCIENTIFIC_IDENTITY = {'PASS' if not preservation_failures else 'FAIL'}")
    print(f"POST_SYNTHESIS_VALIDATION_V001 = {'PASS' if v001_register_pass else 'FAIL'}")
    print(f"V001_EVIDENCE_PATHS = {'PASS' if v001_evidence_pass else 'FAIL'}")
    print(f"SECOND_IMPLEMENTATION_CODE_HASH = {'PASS' if code_hash_pass else 'FAIL'}")
    print(f"TDCOSMO_STRUCTURE_RESULT = {'13/13' if structural_pass else 'FAIL'}")
    print(f"TDCOSMO_QUANTILE_RESULT = {'39/39' if numerical_pass else f'{quantile_pass_count}/39'}")
    print(f"TDCOSMO_TABLE6_RESULT = {'12/12' if table6_pass else 'FAIL'}")
    print(f"TDCOSMO_FINAL_SUMMARY = {'PASS' if summary_pass else 'FAIL'}")

    failures = (
        hash_failures or missing_checksum_members or extra_checksum_members
        or missing_manifest_members or extra_manifest_members or duplicate_manifest_paths
        or manifest_failures or local_failures or missing_local or extra_local
        or not id_pass or not frozen_validation_pass or not historical_pass
        or preservation_failures or evidence_failures or not v001_register_pass or not v001_evidence_pass or not summary_pass
        or not structural_pass or not numerical_pass or not table6_pass or not code_hash_pass
    )
    if failures:
        for item in hash_failures:
            print("HASH_FAILURE", *item, sep="\t")
        for item in missing_checksum_members:
            print("MISSING_CHECKSUM", item, sep="\t")
        for item in extra_checksum_members:
            print("EXTRA_CHECKSUM", item, sep="\t")
        for item in missing_manifest_members:
            print("MISSING_MANIFEST", item, sep="\t")
        for item in extra_manifest_members:
            print("EXTRA_MANIFEST", item, sep="\t")
        for item in duplicate_manifest_paths:
            print("DUPLICATE_MANIFEST", item, sep="\t")
        for item in manifest_failures:
            print("MANIFEST_FAILURE", *item, sep="\t")
        for item in local_failures:
            print("V001_LOCAL_HASH_FAILURE", *item, sep="\t")
        for item in missing_local:
            print("V001_LOCAL_MISSING", item, sep="\t")
        for item in extra_local:
            print("V001_LOCAL_EXTRA", item, sep="\t")
        for item in preservation_failures:
            print("PRESERVATION_FAILURE", item, sep="\t")
        for item in evidence_failures:
            print("V001_EVIDENCE_FAILURE", item, sep="\t")
        return 1

    print("PUBLICATION_PACKAGE_INTEGRITY = PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
