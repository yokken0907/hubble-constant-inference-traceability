#!/usr/bin/env python3
"""Independent publication-package verifier for v1.7.1.

Checkpoint mode validates scientific/provenance closure (CAP001-CAP012) while
explicitly deferring only the root MANIFEST/SHA256SUMS closure.  Final-package
mode additionally validates the complete root inventory and hashes (CAP013).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
BASELINE_REL = Path("REPRODUCTION/posterior_attribution/PHASE1_BASELINE_MANIFEST.tsv")
BASELINE_SHA256 = "6fd4a1982dc59b3caceebe44ae29055031047eec1fda49452cd81a8a6a1bdf7d"
BASELINE_BYTES = 3743
SELECTED_MEMBER_TABLE_SHA256 = "eb7fadce8184cc52af05a82868360d6b23824979b72e1f2795bfd16a74069b09"
FIXED_ARCHIVE_SHA256 = "47c7e6ebe8df320cc4b9c81b180bd10025f194cab588e71ea71a515d7d2236a0"
PHASE2C_HTS67_ZIP_SHA256 = "8254503a8a18d6ca3cfcc6dfb0104458982e19bd13bf89b9c81d3e8f34a31353"
EARLIER_HTS67_COMPARISON_SHA256 = "29f2c9f5443557692b1283e9bf04f9013c7fca293326451ce384060a1dd54738"
E002_STAGE_COMPARISON_TOLERANCE = 1e-8
# C027 retains the frozen pre-selective-repository evidence hash in the claim
# register.  The public package copy has one documented non-scientific wording
# edit (the historical utility is not redistributed).  Both identities are
# independently registered: the historical hash in the claim/history records
# and the current hash in the root package inventory.
C027_HISTORICAL_HASH = "9a5f53c131f83796a8efe689d158a7d2e79b3b05df09720ea7b859ee435ce759"
C027_CURRENT_HASH = "00f395659a457afb43249f7c8ae62415b9200e441df223880e4f8e64b0aafaf8"
C027_PATH = "ANALYSIS_OUTPUTS/tdcosmo/corr2/HTS68_CORR2_PATCH_VALIDATION_REPORT.md"
MAX_PUBLIC_FILE_BYTES = 300_000_000
HEX64 = re.compile(r"^[0-9a-f]{64}$")

HISTORICAL_PREFIXES = (
    "REPRODUCTION/posterior_attribution/official_fetch_records/historical_dns_blocked_attempt/",
    "REPRODUCTION/posterior_attribution/official_fetch_records/historical_failed_attempt_phase2b/",
    "REPRODUCTION/posterior_attribution/official_fetch_records/phase2c_network_execution/",
    "REPRODUCTION/posterior_attribution/historical_substantive_reference/",
    "REPRODUCTION/posterior_attribution/portable_reference/",
)
STALE_TOKENS = (
    "HTS67_HISTORICAL_VS_PORTABLE_COMPARISON.tsv",
    "NOT_VERIFIED_RUNTIME_DNS_UNAVAILABLE",
    "DNS unavailable",
)
FORBIDDEN_ORIGINAL_FULL_HASH_CLAIMS = (
    "ORIGINAL_FULL_ARCHIVE_SHA256=PASS",
    "fully downloaded and hash-verified the complete original archive",
    "complete original archive was downloaded and verified by a full-archive SHA-256",
)

CAP_NAMES = {
    "CAP001": "Release inventory",
    "CAP002": "Original claims",
    "CAP003": "Original numbers",
    "CAP004": "V001 bounded validation",
    "CAP005": "E001 fresh replay",
    "CAP006": "E002 fresh replay",
    "CAP007": "HTS67 history",
    "CAP008": "Phase 2C evidence",
    "CAP009": "Official fetch boundary",
    "CAP010": "History register",
    "CAP011": "Active-state hygiene",
    "CAP012": "Historical immutability",
    "CAP013": "Final-package mode",
}


class Audit:
    def __init__(self) -> None:
        self.errors: dict[str, list[str]] = {cap: [] for cap in CAP_NAMES}
        self.metrics: dict[str, str | int] = {}

    def fail(self, cap: str, message: str) -> None:
        self.errors[cap].append(message)

    def require(self, cap: str, condition: bool, message: str) -> None:
        if not condition:
            self.fail(cap, message)

    def result(self, cap: str) -> str:
        return "PASS" if not self.errors[cap] else "FAIL"

    def all_ok(self, include_final: bool) -> bool:
        caps = list(CAP_NAMES) if include_final else [f"CAP{i:03d}" for i in range(1, 13)]
        return all(not self.errors[c] for c in caps)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def safe_relative(value: str) -> bool:
    if not value or "\\" in value:
        return False
    p = PurePosixPath(value)
    return not p.is_absolute() and ".." not in p.parts and "." not in p.parts


def split_semicolon(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def load_tsv(audit: Audit, cap: str, rel: str, required_columns: Iterable[str]) -> list[dict[str, str]]:
    path = ROOT / rel
    if not path.is_file():
        audit.fail(cap, f"MISSING_FILE:{rel}")
        return []
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            if reader.fieldnames is None:
                audit.fail(cap, f"EMPTY_SCHEMA:{rel}")
                return []
            missing = [c for c in required_columns if c not in reader.fieldnames]
            if missing:
                audit.fail(cap, f"SCHEMA_MISSING:{rel}:{','.join(missing)}")
                return []
            rows = list(reader)
    except Exception as exc:
        audit.fail(cap, f"PARSE_ERROR:{rel}:{type(exc).__name__}")
        return []
    return rows


def parse_key_values(audit: Audit, cap: str, rel: str) -> dict[str, str]:
    path = ROOT / rel
    if not path.is_file():
        audit.fail(cap, f"MISSING_FILE:{rel}")
        return {}
    values: dict[str, str] = {}
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            if "=" not in line:
                audit.fail(cap, f"MALFORMED_KEY_VALUE:{rel}:{line[:80]}")
                continue
            key, value = line.split("=", 1)
            key, value = key.strip(), value.strip()
            if not key or key in values:
                audit.fail(cap, f"DUPLICATE_OR_EMPTY_KEY:{rel}:{key}")
            values[key] = value
    except Exception as exc:
        audit.fail(cap, f"READ_ERROR:{rel}:{type(exc).__name__}")
    return values


def parse_hash_pairs(audit: Audit, cap: str, value: str, context: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in split_semicolon(value):
        if "=" not in item:
            audit.fail(cap, f"MALFORMED_HASH_PAIR:{context}:{item}")
            continue
        name, digest = (x.strip() for x in item.split("=", 1))
        if not name or name in result or not HEX64.fullmatch(digest):
            audit.fail(cap, f"INVALID_HASH_PAIR:{context}:{item}")
            continue
        result[name] = digest
    return result


def parse_checksum_file(audit: Audit, cap: str, rel: str) -> dict[str, str]:
    path = ROOT / rel
    if not path.is_file():
        audit.fail(cap, f"MISSING_FILE:{rel}")
        return {}
    result: dict[str, str] = {}
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            parts = line.split(None, 1)
            if len(parts) != 2:
                audit.fail(cap, f"MALFORMED_CHECKSUM:{rel}:{line[:80]}")
                continue
            digest, name = parts[0], parts[1].lstrip("* ")
            if not HEX64.fullmatch(digest) or not name or name in result:
                audit.fail(cap, f"INVALID_CHECKSUM:{rel}:{line[:80]}")
                continue
            result[name] = digest
    except Exception as exc:
        audit.fail(cap, f"READ_ERROR:{rel}:{type(exc).__name__}")
    return result


def require_exact_ids(audit: Audit, cap: str, rows: list[dict[str, str]], field: str, expected: list[str], rel: str) -> None:
    observed = [r.get(field, "") for r in rows]
    audit.require(cap, observed == expected, f"ID_SEQUENCE:{rel}:expected={len(expected)}:observed={len(observed)}")
    audit.require(cap, len(observed) == len(set(observed)), f"DUPLICATE_IDS:{rel}:{field}")


def finite_text(value: str) -> bool:
    return not re.search(r"(^|[^a-z])(nan|inf|infinity)([^a-z]|$)", value.lower())


def normalized_display(value: str) -> str:
    """Normalize typography only; never change digits, signs, or units."""
    return re.sub(r"\s+", " ", value.replace("–", "-").replace("—", "-")).strip()


def actual_repository_files() -> set[str]:
    files: set[str] = set()
    for path in ROOT.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            files.add(path.relative_to(ROOT).as_posix())
    return files


def cap001_release_inventory(audit: Audit, final_mode: bool) -> None:
    cap = "CAP001"
    required = {
        "VERSION", "README.md", "README_JA.md", "REPRODUCIBILITY.md", "RELEASE_CHECKLIST.md",
        "MANIFEST.tsv", "SHA256SUMS.txt", "PROVENANCE/STATEMENT_TO_EVIDENCE_REGISTER.tsv",
        "TABLES/TABLE2_NUMERICAL_RESULTS.tsv", "PROVENANCE/V001_EVIDENCE_PATHS.tsv",
        "PROVENANCE/REEXECUTION_EVIDENCE_REGISTER.tsv", "PROVENANCE/PRETAG_REPRODUCIBILITY_GATE.tsv",
        "REPRODUCTION/cmb_fixed_seed_bootstrap/EXPECTED_OUTPUT.tsv",
        "REPRODUCTION/posterior_attribution/EXPECTED_OUTPUT.tsv",
        "REPRODUCTION/posterior_attribution/HISTORY_SOURCE_REGISTER.tsv",
        "REPRODUCTION/posterior_attribution/HTS67_HISTORICAL_VS_FRESH_COMPARISON.tsv",
        "tools/trace_record.py", "tools/verify_publication_package.py",
    }
    files = actual_repository_files()
    for rel in sorted(required - files):
        audit.fail(cap, f"REQUIRED_PATH_MISSING:{rel}")
    version = ROOT / "VERSION"
    if version.is_file():
        audit.require(cap, version.read_text(encoding="utf-8").strip() == "1.7.1", "VERSION_NOT_1.7.1")
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT).as_posix()
        if path.is_symlink():
            audit.fail(cap, f"SYMLINK_FORBIDDEN:{rel}")
        if "__pycache__" in path.parts or (path.is_file() and path.suffix == ".pyc"):
            audit.fail(cap, f"CACHE_OR_PYC:{rel}")
        if path.is_file() and (rel.endswith(":Zone.Identifier") or "Zone.Identifier" in path.name):
            audit.fail(cap, f"ZONE_IDENTIFIER:{rel}")
        if path.is_file() and path.stat().st_size > MAX_PUBLIC_FILE_BYTES:
            audit.fail(cap, f"LARGE_THIRD_PARTY_FILE:{rel}:{path.stat().st_size}")
    audit.metrics["RELEASE_FILE_COUNT"] = len(files)
    audit.metrics["ROOT_CLOSURE"] = "VALIDATED" if final_mode else "DEFERRED_FINAL_ASSEMBLY"


def cap002_original_claims(audit: Audit) -> None:
    cap = "CAP002"
    rel = "PROVENANCE/STATEMENT_TO_EVIDENCE_REGISTER.tsv"
    columns = ["STATEMENT_ID", "PRIMARY_OUTPUTS", "OUTPUT_PACKAGE_RELATIVE_PATHS", "OUTPUT_PACKAGE_SHA256", "OUTPUT_SHA256", "PUBLIC_EVIDENCE_LOCATION"]
    rows = load_tsv(audit, cap, rel, columns)
    expected_ids = [f"C{i:03d}" for i in range(1, 31)]
    require_exact_ids(audit, cap, rows, "STATEMENT_ID", expected_ids, rel)
    for row in rows:
        ident = row.get("STATEMENT_ID", "UNKNOWN")
        paths = split_semicolon(row.get("OUTPUT_PACKAGE_RELATIVE_PATHS", ""))
        public_paths = set(split_semicolon(row.get("PUBLIC_EVIDENCE_LOCATION", "")))
        primary = set(split_semicolon(row.get("PRIMARY_OUTPUTS", "")))
        hash_map = parse_hash_pairs(audit, cap, row.get("OUTPUT_PACKAGE_SHA256", ""), ident)
        raw_hash_map = parse_hash_pairs(audit, cap, row.get("OUTPUT_SHA256", ""), ident + ":OUTPUT_SHA256")
        audit.require(cap, bool(paths), f"EMPTY_EVIDENCE_PATHS:{ident}")
        audit.require(cap, len(paths) == len(set(paths)), f"DUPLICATE_EVIDENCE_PATHS:{ident}")
        audit.require(cap, hash_map == raw_hash_map, f"HASH_REGISTERS_DISAGREE:{ident}")
        audit.require(cap, {Path(p).name for p in paths} == set(hash_map), f"PATH_HASH_SET_MISMATCH:{ident}")
        audit.require(cap, {Path(p).name for p in paths} == primary, f"PRIMARY_OUTPUT_SET_MISMATCH:{ident}")
        audit.require(cap, set(paths).issubset(public_paths), f"PUBLIC_EVIDENCE_MAPPING_MISMATCH:{ident}")
        for item in paths:
            if not safe_relative(item):
                audit.fail(cap, f"UNSAFE_EVIDENCE_PATH:{ident}:{item}")
                continue
            path = ROOT / item
            if not path.is_file():
                audit.fail(cap, f"EVIDENCE_MISSING:{ident}:{item}")
                continue
            expected_hash = hash_map.get(path.name)
            if expected_hash:
                observed_hash = sha256(path)
                if ident == "C027" and item == C027_PATH and expected_hash == C027_HISTORICAL_HASH:
                    # Narrow documented historical-to-current correspondence.
                    audit.require(cap, observed_hash == C027_CURRENT_HASH, f"C027_CURRENT_HASH:{item}")
                    current_manifest = load_tsv(audit, cap, "MANIFEST.tsv", ["PATH", "SHA256"])
                    current_rows = [r for r in current_manifest if r.get("PATH") == C027_PATH]
                    audit.require(cap, len(current_rows) == 1 and current_rows[0].get("SHA256") == C027_CURRENT_HASH, "C027_CURRENT_MANIFEST_CORRESPONDENCE")
                    history = load_tsv(audit, cap, "POST_SYNTHESIS_VALIDATION/tdcosmo_second_implementation/HISTORICAL_SOURCE_RECORDS.tsv", ["REPOSITORY_PATH", "SHA256"])
                    history_rows = [r for r in history if r.get("REPOSITORY_PATH") == C027_PATH]
                    audit.require(cap, len(history_rows) == 1 and history_rows[0].get("SHA256") == C027_HISTORICAL_HASH, "C027_HISTORICAL_RECORD_CORRESPONDENCE")
                elif observed_hash != expected_hash:
                    audit.fail(cap, f"EVIDENCE_HASH_MISMATCH:{ident}:{item}")
    audit.metrics["ORIGINAL_CLAIM_COUNT"] = len(rows)


def cap003_original_numbers(audit: Audit) -> None:
    cap = "CAP003"
    table_rel = "TABLES/TABLE2_NUMERICAL_RESULTS.tsv"
    principal_rel = "PROVENANCE/PRINCIPAL_NUMERICAL_RESULTS_VALIDATION.tsv"
    mapping_rel = "PROVENANCE/TABLE2_NUMBER_ID_VALIDATION.tsv"
    direct_rel = "PROVENANCE/DIRECT_NUMERICAL_VALIDATION_REPORT.tsv"
    table = load_tsv(audit, cap, table_rel, ["NUMBER_ID", "QUANTITY", "VALUE", "UNIT"])
    principal = load_tsv(audit, cap, principal_rel, ["NUMBER_ID", "MANUSCRIPT_LABEL", "RAW_VALUE", "MANUSCRIPT_VALUE", "UNIT", "PUBLICATION_TABLE_ROW", "ARTIFACT_PACKAGE_RELATIVE_PATH", "ARTIFACT_PACKAGE_SHA256", "ARTIFACT_SHA256", "CHECK_1_MANUSCRIPT_TO_TABLE", "CHECK_2_TABLE_TO_ARTIFACT", "CANONICALITY"])
    mapping = load_tsv(audit, cap, mapping_rel, ["NUMBER_ID", "TABLE_QUANTITY", "TABLE_VALUE", "TABLE_UNIT", "REGISTER_NUMBER_ID", "REGISTER_PUBLICATION_TABLE_ROW", "REGISTER_MANUSCRIPT_LABEL", "REGISTER_MANUSCRIPT_VALUE", "REGISTER_UNIT", "REGISTER_CHECK_1_MANUSCRIPT_TO_TABLE", "REGISTER_CHECK_2_TABLE_TO_ARTIFACT", "DIRECT_VALIDATION_RESULT", "NUMBER_ID_MAPPING_STATUS", "SCIENTIFIC_VALUE_CHANGED"])
    direct = load_tsv(audit, cap, direct_rel, ["NUMBER_ID", "PUBLICATION_TABLE_MATCH", "ARTIFACT_SHA256_MATCH", "LEDGER_RAW_VALUE", "EXTRACTED_VALUE", "VALUE_MATCH", "LEDGER_RAW_VALUE_2", "EXTRACTED_VALUE_2", "VALUE_2_MATCH", "LEDGER_RAW_VALUE_3", "EXTRACTED_VALUE_3", "VALUE_3_MATCH", "FINAL_RESULT"])
    expected = [f"N{i:03d}" for i in range(1, 47)]
    for rows, rel in ((table, table_rel), (principal, principal_rel), (mapping, mapping_rel), (direct, direct_rel)):
        require_exact_ids(audit, cap, rows, "NUMBER_ID", expected, rel)
    maps = [{r.get("NUMBER_ID", ""): r for r in rows} for rows in (table, principal, mapping, direct)]
    for ident in expected:
        if any(ident not in m for m in maps):
            continue
        t, p, m, d = (x[ident] for x in maps)
        # Table wording and principal-register wording are intentionally distinct
        # for some rows.  TABLE2_NUMBER_ID_VALIDATION is the canonical bridge.
        audit.require(cap, p["PUBLICATION_TABLE_ROW"] == ident, f"PUBLICATION_ROW_MISMATCH:{ident}")
        audit.require(cap, p["CHECK_1_MANUSCRIPT_TO_TABLE"] == "PASS" and p["CHECK_2_TABLE_TO_ARTIFACT"] == "PASS", f"PRINCIPAL_STATUS:{ident}")
        audit.require(cap, p["CANONICALITY"] == "CURRENT_CANONICAL", f"NONCANONICAL:{ident}")
        audit.require(cap, m["REGISTER_NUMBER_ID"] == ident and m["REGISTER_PUBLICATION_TABLE_ROW"] == ident, f"MAPPING_ID:{ident}")
        audit.require(cap, (m["TABLE_QUANTITY"], m["TABLE_VALUE"], m["TABLE_UNIT"]) == (t["QUANTITY"], t["VALUE"], t["UNIT"]), f"TABLE_MAPPING_VALUE:{ident}")
        audit.require(cap, (m["REGISTER_MANUSCRIPT_LABEL"], m["REGISTER_MANUSCRIPT_VALUE"], m["REGISTER_UNIT"]) == (p["MANUSCRIPT_LABEL"], p["MANUSCRIPT_VALUE"], p["UNIT"]), f"REGISTER_MAPPING_VALUE:{ident}")
        audit.require(cap, all(m[x] == "PASS" for x in ("REGISTER_CHECK_1_MANUSCRIPT_TO_TABLE", "REGISTER_CHECK_2_TABLE_TO_ARTIFACT", "DIRECT_VALIDATION_RESULT", "NUMBER_ID_MAPPING_STATUS")) and m["SCIENTIFIC_VALUE_CHANGED"] == "NO", f"MAPPING_STATUS:{ident}")
        audit.require(cap, all(d[x] == "PASS" for x in ("PUBLICATION_TABLE_MATCH", "ARTIFACT_SHA256_MATCH", "VALUE_MATCH", "VALUE_2_MATCH", "VALUE_3_MATCH", "FINAL_RESULT")), f"DIRECT_STATUS:{ident}")
        for suffix in ("", "_2", "_3"):
            audit.require(cap, d[f"LEDGER_RAW_VALUE{suffix}"] == p[f"RAW_VALUE{suffix}"], f"RAW_LEDGER_MISMATCH:{ident}:{suffix or '1'}")
            audit.require(cap, normalized_display(d[f"EXTRACTED_VALUE{suffix}"]) == normalized_display(p[f"RAW_VALUE{suffix}"]), f"RAW_EXTRACTION_MISMATCH:{ident}:{suffix or '1'}")
        for value in (t["VALUE"], p["RAW_VALUE"], p["MANUSCRIPT_VALUE"]):
            audit.require(cap, bool(value) and finite_text(value), f"NONFINITE_OR_EMPTY_VALUE:{ident}")
        artifact_rel = p["ARTIFACT_PACKAGE_RELATIVE_PATH"]
        if not safe_relative(artifact_rel):
            audit.fail(cap, f"UNSAFE_ARTIFACT_PATH:{ident}:{artifact_rel}")
        else:
            artifact = ROOT / artifact_rel
            if not artifact.is_file():
                audit.fail(cap, f"ARTIFACT_MISSING:{ident}:{artifact_rel}")
            else:
                observed = sha256(artifact)
                audit.require(cap, p["ARTIFACT_PACKAGE_SHA256"] == p["ARTIFACT_SHA256"] == observed, f"ARTIFACT_HASH:{ident}:{artifact_rel}")
    audit.metrics["ORIGINAL_NUMBER_COUNT"] = len(table)


def cap004_v001(audit: Audit) -> None:
    cap = "CAP004"
    register_rel = "PROVENANCE/POST_SYNTHESIS_VALIDATION_REGISTER.tsv"
    paths_rel = "PROVENANCE/V001_EVIDENCE_PATHS.tsv"
    register = load_tsv(audit, cap, register_rel, ["VALIDATION_ID", "RESULT", "EVIDENCE_PATHS", "EVIDENCE_SHA256", "INTERPRETATION_LIMIT"])
    paths = load_tsv(audit, cap, paths_rel, ["VALIDATION_ID", "EVIDENCE_PATH", "SHA256", "ROLE"])
    audit.require(cap, len(register) == 1 and register[0].get("VALIDATION_ID") == "V001", "V001_REGISTER_ROW")
    audit.require(cap, len(paths) == 15 and len({r.get("EVIDENCE_PATH") for r in paths}) == 15, "V001_PATH_COUNT_OR_DUPLICATE")
    if register:
        row = register[0]
        audit.require(cap, "COMPLETE_WITH_SCOPE" in row["RESULT"], "V001_BOUNDED_STATUS")
        reg_paths = split_semicolon(row["EVIDENCE_PATHS"])
        reg_hashes = parse_hash_pairs(audit, cap, row["EVIDENCE_SHA256"], "V001")
        audit.require(cap, set(reg_paths) == {r.get("EVIDENCE_PATH", "") for r in paths}, "V001_REGISTER_PATH_SET")
        audit.require(cap, {Path(x).name for x in reg_paths} == set(reg_hashes), "V001_REGISTER_HASH_SET")
        path_hashes = {Path(r.get("EVIDENCE_PATH", "")).name: r.get("SHA256", "") for r in paths}
        audit.require(cap, reg_hashes == path_hashes, "V001_REGISTER_PATH_HASH_AGREEMENT")
    for row in paths:
        rel = row.get("EVIDENCE_PATH", "")
        audit.require(cap, row.get("VALIDATION_ID") == "V001", f"V001_ID:{rel}")
        audit.require(cap, row.get("ROLE") in {"PRIMARY", "SUPPORTING"}, f"V001_ROLE:{rel}")
        if not safe_relative(rel):
            audit.fail(cap, f"V001_UNSAFE_PATH:{rel}")
            continue
        path = ROOT / rel
        if not path.is_file():
            audit.fail(cap, f"V001_MISSING:{rel}")
        elif sha256(path) != row.get("SHA256"):
            audit.fail(cap, f"V001_HASH:{rel}")
    audit.require(cap, any(r.get("ROLE") == "PRIMARY" for r in paths), "V001_NO_PRIMARY")
    final_json = ROOT / "POST_SYNTHESIS_VALIDATION/tdcosmo_second_implementation/FINAL_CLASSIFICATION.json"
    try:
        data = json.loads(final_json.read_text(encoding="utf-8"))
        audit.require(cap, data.get("branch_status") == "COMPLETE_WITH_SCOPE", "V001_FINAL_BRANCH_STATUS")
        audit.require(cap, str(data.get("final_classification", "")).startswith("PASS_"), "V001_FINAL_CLASSIFICATION")
        ext = data.get("extension", {})
        audit.require(cap, ext.get("files") == 13 and ext.get("structural_pass") == "13/13" and ext.get("quantile_tolerance_pass") == "39/39" and ext.get("table6_published_precision_pass") == "12/12", "V001_FINAL_METRICS")
    except Exception as exc:
        audit.fail(cap, f"V001_FINAL_JSON:{type(exc).__name__}")


def cap005_e001(audit: Audit) -> None:
    cap = "CAP005"
    base = Path("REPRODUCTION/cmb_fixed_seed_bootstrap")
    expected = load_tsv(audit, cap, (base / "EXPECTED_OUTPUT.tsv").as_posix(), ["ITEM_ID", "TEST", "SEED", "DRAWS", "EXCEEDANCE_COUNT", "BOOTSTRAP_P", "EQUIVALENT_SIGMA", "MANUSCRIPT_DISPLAY", "TOLERANCE"])
    acceptance = load_tsv(audit, cap, (base / "REPLAY_ACCEPTANCE_RESULTS.tsv").as_posix(), ["ITEM_ID", "expected", "observed", "absolute_difference", "tolerance", "status"])
    require_exact_ids(audit, cap, expected, "ITEM_ID", ["N025", "N026"], (base / "EXPECTED_OUTPUT.tsv").as_posix())
    require_exact_ids(audit, cap, acceptance, "ITEM_ID", ["N025", "N026"], (base / "REPLAY_ACCEPTANCE_RESULTS.tsv").as_posix())
    input_rows = load_tsv(audit, cap, (base / "INPUT_MANIFEST.tsv").as_posix(), ["PATH", "BYTES", "SHA256", "INPUT_MODE"])
    audit.require(cap, len(input_rows) == 1, "E001_INPUT_COUNT")
    for row in input_rows:
        rel = base / row["PATH"]
        path = ROOT / rel
        audit.require(cap, safe_relative(rel.as_posix()) and path.is_file(), f"E001_INPUT_MISSING:{rel}")
        if path.is_file():
            audit.require(cap, str(path.stat().st_size) == row["BYTES"] and sha256(path) == row["SHA256"], f"E001_INPUT_IDENTITY:{rel}")
    checksum_rel = (base / "fresh_replay_records/E001_SHA256SUMS.txt").as_posix()
    checks = parse_checksum_file(audit, cap, checksum_rel)
    expected_checksum_names = {"02_PROFILED_AMPLITUDE_MODELS.tsv", "03_MODEL_AMPLITUDES.tsv", "04_NESTED_MODEL_TESTS.tsv", "05_PROFILED_DIRECTION_STABILITY.tsv", "06_MACHINE_READABLE_RESULTS.json", "E001_CLASSIFICATION.txt", "E001_ENVIRONMENT.json"}
    audit.require(cap, set(checks) == expected_checksum_names, "E001_CHECKSUM_SET")
    for name, digest in checks.items():
        folder = base / ("fresh_replay_records" if name.startswith("E001_") else "verified_replay_outputs")
        path = ROOT / folder / name
        audit.require(cap, path.is_file(), f"E001_CHECKSUM_MISSING:{name}")
        if path.is_file():
            audit.require(cap, sha256(path) == digest, f"E001_CHECKSUM_HASH:{name}")
    try:
        environment = json.loads((ROOT / base / "fresh_replay_records/E001_ENVIRONMENT.json").read_text(encoding="utf-8"))
        audit.require(cap, environment.get("seed") == 10199 and environment.get("draws") == 1000, "E001_ENVIRONMENT_CONTRACT")
        output = json.loads((ROOT / base / "verified_replay_outputs/06_MACHINE_READABLE_RESULTS.json").read_text(encoding="utf-8"))
        tests = {r.get("test"): r for r in output.get("tests", [])}
        audit.require(cap, len(tests) == 3, "E001_TEST_COUNT")
    except Exception as exc:
        audit.fail(cap, f"E001_JSON_PARSE:{type(exc).__name__}")
        tests = {}
    acceptance_map = {r.get("ITEM_ID", ""): r for r in acceptance}
    for row in expected:
        ident, test_name = row["ITEM_ID"], row["TEST"]
        test = tests.get(test_name)
        if not test:
            audit.fail(cap, f"E001_TEST_MISSING:{ident}:{test_name}")
            continue
        try:
            draws = int(row["DRAWS"]); count = int(row["EXCEEDANCE_COUNT"])
            p_expected = float(row["BOOTSTRAP_P"]); sigma_expected = float(row["EQUIVALENT_SIGMA"])
            p_observed = float(test["bootstrap_p"]); sigma_observed = float(test["bootstrap_equivalent_sigma"])
            audit.require(cap, int(row["SEED"]) == 10199 and draws == 1000 and int(test["bootstrap_draws"]) == draws, f"E001_SEED_DRAW:{ident}")
            audit.require(cap, abs(p_observed - p_expected) <= 1e-15, f"E001_P_VALUE:{ident}")
            audit.require(cap, abs(sigma_observed - sigma_expected) <= 1e-10, f"E001_SIGMA:{ident}")
            derived_count = round(p_observed * (draws + 1) - 1)
            audit.require(cap, derived_count == count, f"E001_EXCEEDANCE_COUNT:{ident}")
            acc = acceptance_map.get(ident, {})
            audit.require(cap, acc.get("status") == "PASS" and acc.get("expected") == row["MANUSCRIPT_DISPLAY"], f"E001_ACCEPTANCE_STATUS:{ident}")
            audit.require(cap, abs(float(acc.get("observed", "nan")) - sigma_observed) <= 1e-15, f"E001_ACCEPTANCE_OBSERVED:{ident}")
        except Exception as exc:
            audit.fail(cap, f"E001_NUMERIC_PARSE:{ident}:{type(exc).__name__}")
    nested = load_tsv(audit, cap, (base / "verified_replay_outputs/04_NESTED_MODEL_TESTS.tsv").as_posix(), ["test", "bootstrap_draws", "bootstrap_p", "bootstrap_equivalent_sigma"])
    nested_map = {r.get("test", ""): r for r in nested}
    for name, test in tests.items():
        row = nested_map.get(name)
        audit.require(cap, row is not None, f"E001_NESTED_ROW:{name}")
        if row:
            try:
                audit.require(cap, int(row["bootstrap_draws"]) == int(test["bootstrap_draws"]), f"E001_NESTED_DRAWS:{name}")
                audit.require(cap, abs(float(row["bootstrap_p"]) - float(test["bootstrap_p"])) <= 1e-15, f"E001_NESTED_P:{name}")
                audit.require(cap, abs(float(row["bootstrap_equivalent_sigma"]) - float(test["bootstrap_equivalent_sigma"])) <= 1e-15, f"E001_NESTED_SIGMA:{name}")
            except Exception as exc:
                audit.fail(cap, f"E001_NESTED_PARSE:{name}:{type(exc).__name__}")
    classification = parse_key_values(audit, cap, (base / "fresh_replay_records/E001_CLASSIFICATION.txt").as_posix())
    verify_path = ROOT / base / "fresh_replay_records/E001_FRESH_VERIFY.txt"
    audit.require(cap, classification.get("E001_CLASSIFICATION") == "COMPLETE_WITH_SCOPE" and classification.get("FRESH_REPLAY_VERIFICATION") == "PASS", "E001_CLASSIFICATION")
    audit.require(cap, verify_path.is_file() and verify_path.read_text(encoding="utf-8").strip() == "E001_VERIFY=PASS", "E001_FRESH_VERIFY")


def evaluate_e002_row(audit: Audit, cap: str, ident: str, expected: dict[str, str], observed: dict[str, str], context: str) -> None:
    for key in ("EXPECTED_RAW", "EXPECTED_DISPLAY", "COMPARISON_RULE", "SOURCE_PATH"):
        audit.require(cap, observed.get(key) == expected.get(key), f"{context}_CONTRACT:{ident}:{key}")
    audit.require(cap, observed.get("STATUS") == "PASS", f"{context}_STATUS:{ident}")
    rule = expected.get("COMPARISON_RULE", "")
    try:
        if rule == "EXACT":
            audit.require(cap, observed.get("OBSERVED_RAW") == expected.get("EXPECTED_RAW"), f"{context}_EXACT_RAW:{ident}")
            audit.require(cap, observed.get("OBSERVED_DISPLAY") == expected.get("EXPECTED_DISPLAY"), f"{context}_EXACT_DISPLAY:{ident}")
        elif rule.startswith("ABS<="):
            tolerance = float(rule.split("<=", 1)[1])
            exp = float(expected["EXPECTED_RAW"]); obs = float(observed["OBSERVED_RAW"])
            diff = abs(obs - exp)
            audit.require(cap, math.isfinite(exp) and math.isfinite(obs) and diff <= tolerance, f"{context}_TOLERANCE:{ident}:{diff}")
            reported = float(observed.get("ABS_DIFFERENCE_OR_NOTE", "nan"))
            audit.require(cap, math.isfinite(reported) and abs(reported - diff) <= max(1e-30, tolerance * 1e-6), f"{context}_REPORTED_DIFF:{ident}")
            audit.require(cap, observed.get("OBSERVED_DISPLAY") == expected.get("EXPECTED_DISPLAY"), f"{context}_DISPLAY:{ident}")
        else:
            audit.fail(cap, f"{context}_UNKNOWN_RULE:{ident}:{rule}")
    except Exception as exc:
        audit.fail(cap, f"{context}_NUMERIC_PARSE:{ident}:{type(exc).__name__}")


def cap006_e002(audit: Audit) -> None:
    cap = "CAP006"
    base = Path("REPRODUCTION/posterior_attribution")
    p2c = base / "official_fetch_records/phase2c_network_execution/evidence"
    expected = load_tsv(audit, cap, (base / "EXPECTED_OUTPUT.tsv").as_posix(), ["ITEM_ID", "EXPECTED_RAW", "EXPECTED_DISPLAY", "COMPARISON_RULE", "SOURCE_PATH"])
    phase2c = load_tsv(audit, cap, (p2c / "E002_FRESH_OUTPUT_COMPARISON.tsv").as_posix(), ["ITEM_ID", "EXPECTED_RAW", "OBSERVED_RAW", "COMPARISON_RULE", "ABS_DIFFERENCE_OR_NOTE", "EXPECTED_DISPLAY", "OBSERVED_DISPLAY", "STATUS", "SOURCE_PATH"])
    expected_ids = [f"N{i:03d}" for i in range(29, 36)] + ["HTS66_CLASSIFICATION", "HTS67_CLASSIFICATION"]
    for rows, rel in ((expected, (base / "EXPECTED_OUTPUT.tsv").as_posix()), (phase2c, (p2c / "E002_FRESH_OUTPUT_COMPARISON.tsv").as_posix())):
        require_exact_ids(audit, cap, rows, "ITEM_ID", expected_ids, rel)
    exp_map = {r.get("ITEM_ID", ""): r for r in expected}
    p2_map = {r.get("ITEM_ID", ""): r for r in phase2c}
    for ident in expected_ids:
        if ident in exp_map and ident in p2_map:
            evaluate_e002_row(audit, cap, ident, exp_map[ident], p2_map[ident], "PHASE2C")
    table2 = {r.get("NUMBER_ID", ""): r for r in load_tsv(audit, cap, "TABLES/TABLE2_NUMERICAL_RESULTS.tsv", ["NUMBER_ID", "VALUE"])}
    for ident in [f"N{i:03d}" for i in range(29, 36)]:
        if ident in exp_map and ident in table2:
            audit.require(cap, table2[ident]["VALUE"] == exp_map[ident]["EXPECTED_DISPLAY"], f"TABLE2_E002_DISPLAY:{ident}")
    stages = load_tsv(audit, cap, (p2c / "E002_STAGE_STATUS.tsv").as_posix(), ["STAGE", "EXECUTION_STATUS", "OUTPUT_PATH"])
    audit.require(cap, [r.get("STAGE") for r in stages] == [f"HTS{i}" for i in range(59, 68)] and all(r.get("EXECUTION_STATUS") == "PASS" for r in stages), "PHASE2C_E002_STAGE_STATUS")
    stage_compare = load_tsv(audit, cap, (p2c / "E002_FRESH_STAGE_COMPARISON.tsv").as_posix(), ["STAGE", "FILE", "REFERENCE_KIND", "STATUS", "MAX_ABS_NUMERIC_DIFFERENCE", "TEXT_DIFFERENCE_COUNT"])
    audit.require(cap, len(stage_compare) == 67 and all(r.get("STATUS") == "PASS" for r in stage_compare), "E002_STAGE_COMPARISON")
    audit.require(cap, Counter(r.get("STAGE") for r in stage_compare)["HTS67"] == 8, "E002_HTS67_STAGE_ROWS")
    for row in stage_compare:
        try:
            difference = float(row.get("MAX_ABS_NUMERIC_DIFFERENCE", "nan"))
            audit.require(
                cap,
                math.isfinite(difference)
                and difference <= E002_STAGE_COMPARISON_TOLERANCE
                and row.get("TEXT_DIFFERENCE_COUNT") == "0",
                f"E002_STAGE_ROW:{row.get('STAGE')}:{row.get('FILE')}:{difference}",
            )
        except Exception:
            audit.fail(cap, f"E002_STAGE_ROW_PARSE:{row.get('STAGE')}:{row.get('FILE')}")
    class_rows = load_tsv(audit, cap, (p2c / "E002_STAGE_CLASSIFICATION_VERIFICATION.tsv").as_posix(), ["STAGE", "EXPECTED_CLASSIFICATION", "OBSERVED_CLASSIFICATION", "STATUS"])
    audit.require(cap, [r.get("STAGE") for r in class_rows] == [f"HTS{i}" for i in range(59, 68)], "E002_CLASSIFICATION_STAGE_SET")
    audit.require(cap, all(r.get("STATUS") == "PASS" and r.get("EXPECTED_CLASSIFICATION") == r.get("OBSERVED_CLASSIFICATION") for r in class_rows), "E002_CLASSIFICATION_MATCH")
    phase2c_class = parse_key_values(audit, cap, (p2c / "E002_CLASSIFICATION.txt").as_posix())
    audit.require(cap, phase2c_class == {"E002_CLASSIFICATION": "COMPLETE_WITH_SCOPE", "FRESH_OUTPUT_VERIFICATION": "PASS", "HTS67_PORTABLE_REPLAY": "PASS"}, "PHASE2C_E002_CLASSIFICATION")
    phase2c_result = parse_key_values(audit, cap, (p2c / "PHASE2C_RESULT.txt").as_posix())
    audit.require(cap, phase2c_result.get("OFFICIAL_FETCH_EMPTY_CACHE") == "PASS" and phase2c_result.get("E002_FROM_OFFICIAL_EMPTY_CACHE") == "PASS", "PHASE2C_E002_OFFICIAL_EMPTY_CACHE")
    lineage = load_tsv(audit, cap, "PROVENANCE/PHASE3B_RUN_LINEAGE_REGISTER.tsv", ["RUN_ID", "ROLE", "CURRENT_E002_ACCEPTANCE_EVIDENCE", "STATUS"])
    current = [r for r in lineage if r.get("CURRENT_E002_ACCEPTANCE_EVIDENCE") == "YES"]
    audit.require(cap, len(current) == 1 and current[0].get("RUN_ID") == "PHASE2C-OFFICIAL-EMPTY-CACHE-20260728T122933Z" and current[0].get("ROLE") == "CURRENT_E002_OFFICIAL_EMPTY_CACHE_ACCEPTANCE_RUN" and current[0].get("STATUS") == "PASS", "E002_CURRENT_LINEAGE")
    e_register = load_tsv(audit, cap, "PROVENANCE/REEXECUTION_EVIDENCE_REGISTER.tsv", ["EVIDENCE_ID", "RESULT", "COVERS"])
    e_map = {r.get("EVIDENCE_ID", ""): r for r in e_register}
    audit.require(cap, set(e_map) == {"E001", "E002"} and e_map.get("E002", {}).get("RESULT") == "COMPLETE_WITH_SCOPE" and e_map.get("E002", {}).get("COVERS") == "N029-N035", "E002_REGISTER")


def cap007_hts67_history(audit: Audit) -> None:
    cap = "CAP007"
    base = Path("REPRODUCTION/posterior_attribution")
    hist_dir = base / "historical_substantive_reference/hts67"
    phase2c_zip_rel = base / "official_fetch_records/phase2c_network_execution/outputs/HTS67_RESULTS_FOR_REVIEW.zip"
    phase2c_sums_rel = base / "official_fetch_records/phase2c_network_execution/evidence/E002_SHA256SUMS.txt"
    manifest = load_tsv(audit, cap, (hist_dir / "HISTORICAL_REFERENCE_MANIFEST.tsv").as_posix(), ["PATH", "SOURCE_MEMBER_PATH", "SOURCE_MEMBER_BYTE_SIZE", "SOURCE_MEMBER_SHA256", "COPIED_FILE_BYTE_SIZE", "COPIED_FILE_SHA256", "BYTE_IDENTITY_STATUS"])
    comparison = load_tsv(audit, cap, (base / "HTS67_HISTORICAL_VS_FRESH_COMPARISON.tsv").as_posix(), ["PATH", "REFERENCE_KIND", "HISTORICAL_SHA256", "FRESH_SHA256", "BYTE_IDENTICAL", "COMPARISON_TYPE", "MAX_ABS_NUMERIC_DIFFERENCE", "TEXT_DIFFERENCE_COUNT", "CLASSIFICATION_MATCH", "PUBLICATION_PRECISION_MATCH", "STATUS"])
    expected_names = {
        "HTS67_CLASSIFICATION.tsv", "HTS67_BURNIN_SENSITIVITY.tsv", "HTS67_DIRECTED_BASELINE_COMPARISON.tsv",
        "HTS67_ENDPOINT_6D_SUMMARY.tsv", "HTS67_INDEPENDENT_AUDIT_CHECKS.tsv", "HTS67_LOO_STABILITY.tsv",
        "HTS67_SYMMETRIC_METRIC_RESULTS.tsv", "HTS67_SYMMETRIC_POOLING_SENSITIVITY.tsv",
    }
    audit.require(cap, len(manifest) == 8 and {r.get("SOURCE_MEMBER_PATH") for r in manifest} == expected_names, "HTS67_MANIFEST_SET")
    phase2c_zip = ROOT / phase2c_zip_rel
    audit.require(cap, phase2c_zip.is_file() and sha256(phase2c_zip) == PHASE2C_HTS67_ZIP_SHA256, "PHASE2C_HTS67_ZIP_IDENTITY")
    phase2c_members: dict[str, str] = {}
    if phase2c_zip.is_file():
        try:
            with zipfile.ZipFile(phase2c_zip) as archive:
                audit.require(cap, archive.testzip() is None, "PHASE2C_HTS67_ZIP_CRC")
                names = [info.filename for info in archive.infolist() if not info.is_dir()]
                for name in expected_names:
                    audit.require(cap, names.count(name) == 1, f"PHASE2C_HTS67_MEMBER_COUNT:{name}")
                    if names.count(name) == 1:
                        phase2c_members[name] = hashlib.sha256(archive.read(name)).hexdigest()
        except Exception as exc:
            audit.fail(cap, f"PHASE2C_HTS67_ZIP_READ:{type(exc).__name__}")
    phase2c_sums = parse_checksum_file(audit, cap, phase2c_sums_rel.as_posix())
    audit.require(cap, phase2c_sums.get("HTS67_RESULTS_FOR_REVIEW.zip") == PHASE2C_HTS67_ZIP_SHA256, "PHASE2C_E002_SUMS_ZIP")
    for name in expected_names:
        audit.require(cap, phase2c_sums.get(f"HTS67_RESULTS_FOR_REVIEW/{name}") == phase2c_members.get(name), f"PHASE2C_E002_SUMS_MEMBER:{name}")
    manifest_by_name: dict[str, dict[str, str]] = {}
    for row in manifest:
        name = row.get("SOURCE_MEMBER_PATH", "")
        manifest_by_name[name] = row
        rel = base / row.get("PATH", "")
        path = ROOT / rel
        audit.require(cap, safe_relative(rel.as_posix()) and path.is_file(), f"HTS67_HISTORICAL_MISSING:{name}")
        if path.is_file():
            observed = sha256(path); size = str(path.stat().st_size)
            audit.require(cap, row.get("SOURCE_MEMBER_BYTE_SIZE") == row.get("COPIED_FILE_BYTE_SIZE") == size, f"HTS67_HISTORICAL_SIZE:{name}")
            audit.require(cap, row.get("SOURCE_MEMBER_SHA256") == row.get("COPIED_FILE_SHA256") == observed, f"HTS67_HISTORICAL_HASH:{name}")
            audit.require(cap, row.get("BYTE_IDENTITY_STATUS") == "PASS", f"HTS67_HISTORICAL_IDENTITY:{name}")
    audit.require(cap, len(comparison) == 8 and {r.get("PATH") for r in comparison} == expected_names, "HTS67_COMPARISON_SET")
    for row in comparison:
        name = row.get("PATH", "")
        m = manifest_by_name.get(name, {})
        historical_hash = m.get("COPIED_FILE_SHA256")
        fresh_hash = phase2c_members.get(name)
        audit.require(cap, row.get("REFERENCE_KIND") == "PHASE2C_OFFICIAL_EMPTY_CACHE_FRESH_OUTPUT", f"HTS67_REFERENCE_KIND:{name}")
        audit.require(cap, row.get("HISTORICAL_SHA256") == historical_hash and row.get("FRESH_SHA256") == fresh_hash, f"HTS67_COMPARISON_HASH:{name}")
        audit.require(cap, historical_hash == fresh_hash, f"HTS67_PHASE2C_MEMBER_BYTE_IDENTITY:{name}")
        audit.require(cap, row.get("BYTE_IDENTICAL") == "YES", f"HTS67_BYTE_BOUNDARY:{name}")
        audit.require(cap, row.get("COMPARISON_TYPE") == "BYTE_IDENTITY_AND_NUMERIC_EQUALITY", f"HTS67_COMPARISON_TYPE:{name}")
        audit.require(cap, row.get("TEXT_DIFFERENCE_COUNT") == "0" and row.get("CLASSIFICATION_MATCH") == "YES" and row.get("PUBLICATION_PRECISION_MATCH") == "YES", f"HTS67_SEMANTIC_MATCH:{name}")
        audit.require(cap, row.get("STATUS") == "PASS_BYTE_IDENTICAL", f"HTS67_STATUS:{name}")
        try:
            diff = float(row.get("MAX_ABS_NUMERIC_DIFFERENCE", "nan"))
            audit.require(cap, math.isfinite(diff) and diff == 0.0, f"HTS67_ZERO_DIFFERENCE:{name}:{diff}")
        except Exception:
            audit.fail(cap, f"HTS67_DIFFERENCE_PARSE:{name}")
    earlier_rel = base / "historical_earlier_replay/HTS67_HISTORICAL_VS_EARLIER_FRESH_COMPARISON.tsv"
    raw_rel = base / "official_fetch_records/phase2c_network_execution/evidence/HTS67_HISTORICAL_VS_FRESH_COMPARISON.tsv"
    for rel in (earlier_rel, raw_rel):
        path = ROOT / rel
        audit.require(cap, path.is_file() and sha256(path) == EARLIER_HTS67_COMPARISON_SHA256, f"EARLIER_HTS67_COMPARISON_IDENTITY:{rel}")
    origin = load_tsv(audit, cap, "PROVENANCE/PHASE2C_EVIDENCE_ORIGIN_CORRECTION.tsv", ["RAW_PHASE2C_PATH", "SHA256", "ACTUAL_ORIGIN_CLASS", "PHASE2C_GENERATED", "CURRENT_ACCEPTANCE_ROLE", "STATUS"])
    audit.require(cap, len(origin) == 1 and origin[0].get("RAW_PHASE2C_PATH") == raw_rel.as_posix() and origin[0].get("SHA256") == EARLIER_HTS67_COMPARISON_SHA256 and origin[0].get("ACTUAL_ORIGIN_CLASS") == "HISTORICAL_EARLIER_FRESH_REPLAY_STATIC_COPY" and origin[0].get("PHASE2C_GENERATED") == "NO" and origin[0].get("CURRENT_ACCEPTANCE_ROLE") == "NO" and origin[0].get("STATUS") == "PASS_PROVENANCE_CORRECTED", "PHASE2C_RAW_EVIDENCE_ORIGIN_CORRECTION")


def cap008_phase2c_evidence(audit: Audit) -> None:
    cap = "CAP008"
    base = Path("REPRODUCTION/posterior_attribution/official_fetch_records/phase2c_network_execution")
    manifest_rel = (base / "PHASE2C_EVIDENCE_MANIFEST.tsv").as_posix()
    manifest = load_tsv(audit, cap, manifest_rel, ["PATH", "BYTE_SIZE", "SHA256", "ROLE", "GENERATED_BY", "STATUS"])
    expected_paths = {
        "evidence/E002_CLASSIFICATION.txt", "evidence/E002_ENVIRONMENT.json", "evidence/E002_FRESH_OUTPUT_COMPARISON.tsv",
        "evidence/E002_FRESH_STAGE_COMPARISON.tsv", "evidence/E002_INPUT_VERIFICATION.tsv", "evidence/E002_SHA256SUMS.txt",
        "evidence/E002_STAGE_CLASSIFICATION_VERIFICATION.tsv", "evidence/E002_STAGE_STATUS.tsv", "evidence/HTS67_HISTORICAL_VS_FRESH_COMPARISON.tsv",
        "evidence/OFFICIAL_ARCHIVE_ACQUISITION.tsv", "evidence/OFFICIAL_HTTP_HEADERS/FIXED_RANGE_0_0_HEADERS.txt",
        "evidence/OFFICIAL_HTTP_HEADERS/ORIGINAL_RANGE_0_0_HEADERS.txt", "evidence/OFFICIAL_SELECTED_MEMBER_VERIFICATION.tsv",
        "evidence/PHASE2C_ENVIRONMENT.json", "evidence/PHASE2C_EVIDENCE_SHA256SUMS.txt", "evidence/PHASE2C_NETWORK_PREFLIGHT.tsv",
        "evidence/PHASE2C_NETWORK_PROBE.json", "evidence/PHASE2C_RESULT.txt", "evidence/PHASE2C_STARTING_TREE.tsv",
        "logs/PHASE2C_BUNDLE_AND_CHECKPOINT_VERIFY.txt", "logs/PHASE2C_EXIT_CODE.txt", "logs/PHASE2C_PHASE1_LOCAL_VERIFIER.txt",
        "logs/PHASE2C_RUN_STDERR.txt", "logs/PHASE2C_RUN_STDOUT.txt",
    }
    audit.require(cap, len(manifest) == 24 and {r.get("PATH") for r in manifest} == expected_paths, "PHASE2C_MANIFEST_24_SET")
    sidecar = ROOT / base / "PHASE2C_EVIDENCE_MANIFEST.tsv.sha256"
    if not sidecar.is_file():
        audit.fail(cap, "PHASE2C_MANIFEST_SIDECAR_MISSING")
    else:
        parts = sidecar.read_text(encoding="utf-8").strip().split(None, 1)
        audit.require(cap, len(parts) == 2 and parts[0] == sha256(ROOT / manifest_rel) and Path(parts[1].lstrip("* ")).name == "PHASE2C_EVIDENCE_MANIFEST.tsv", "PHASE2C_MANIFEST_DETACHED_HASH")
    manifest_map = {r.get("PATH", ""): r for r in manifest}
    for rel, row in manifest_map.items():
        path = ROOT / base / rel
        audit.require(cap, safe_relative(rel) and path.is_file(), f"PHASE2C_EVIDENCE_MISSING:{rel}")
        if path.is_file():
            audit.require(cap, str(path.stat().st_size) == row.get("BYTE_SIZE") and sha256(path) == row.get("SHA256"), f"PHASE2C_EVIDENCE_IDENTITY:{rel}")
            audit.require(cap, row.get("STATUS") == "PRESERVED", f"PHASE2C_EVIDENCE_STATUS:{rel}")
    checksum_rel = (base / "evidence/PHASE2C_EVIDENCE_SHA256SUMS.txt").as_posix()
    checks = parse_checksum_file(audit, cap, checksum_rel)
    audit.require(cap, len(checks) == 23, "PHASE2C_CHECKSUM_COUNT_23")
    manifest_without_self = {p for p in expected_paths if p != "evidence/PHASE2C_EVIDENCE_SHA256SUMS.txt"}
    by_name = {Path(p).name: p for p in manifest_without_self}
    audit.require(cap, len(by_name) == 23 and {Path(name).name for name in checks} == set(by_name), "PHASE2C_CHECKSUM_MEMBER_SET")
    for recorded_name, digest in checks.items():
        name = Path(recorded_name).name
        rel = by_name.get(name)
        if rel:
            path = ROOT / base / rel
            audit.require(cap, path.is_file() and sha256(path) == digest and manifest_map.get(rel, {}).get("SHA256") == digest, f"PHASE2C_CHECKSUM_IDENTITY:{name}")
    selected_rel = (base / "evidence/OFFICIAL_SELECTED_MEMBER_VERIFICATION.tsv").as_posix()
    selected = load_tsv(audit, cap, selected_rel, ["SOURCE", "CONTRACT", "MATERIALIZED_PATH", "EXPECTED_BYTES", "OBSERVED_BYTES", "EXPECTED_SHA256", "OBSERVED_SHA256", "STATUS"])
    audit.require(cap, len(selected) == 51 and sha256(ROOT / selected_rel) == SELECTED_MEMBER_TABLE_SHA256, "PHASE2C_SELECTED_TABLE_IDENTITY")
    audit.require(cap, len({(r.get("SOURCE"), r.get("MATERIALIZED_PATH")) for r in selected}) == 51, "PHASE2C_SELECTED_DUPLICATE")
    counts = Counter(r.get("SOURCE") for r in selected)
    audit.require(cap, counts == Counter({"ORIGINAL": 40, "FIXED": 11}), f"PHASE2C_SELECTED_COUNTS:{dict(counts)}")
    for row in selected:
        audit.require(cap, row.get("STATUS") == "PASS" and row.get("EXPECTED_BYTES") == row.get("OBSERVED_BYTES") and row.get("EXPECTED_SHA256") == row.get("OBSERVED_SHA256") and HEX64.fullmatch(row.get("EXPECTED_SHA256", "")) is not None, f"PHASE2C_SELECTED_ROW:{row.get('SOURCE')}:{row.get('MATERIALIZED_PATH')}")
    result = parse_key_values(audit, cap, (base / "evidence/PHASE2C_RESULT.txt").as_posix())
    audit.require(cap, result == {"CLASSIFICATION": "PASS", "OFFICIAL_FETCH_EMPTY_CACHE": "PASS", "E002_FROM_OFFICIAL_EMPTY_CACHE": "PASS", "REPOSITORY_UNCHANGED": "YES"}, "PHASE2C_RESULT_CONTENT")
    exit_path = ROOT / base / "logs/PHASE2C_EXIT_CODE.txt"
    stderr_path = ROOT / base / "logs/PHASE2C_RUN_STDERR.txt"
    audit.require(cap, exit_path.is_file() and exit_path.read_text(encoding="utf-8").strip() == "0", "PHASE2C_EXIT_CODE")
    audit.require(cap, stderr_path.is_file() and stderr_path.stat().st_size == 0, "PHASE2C_STDERR_NOT_EMPTY")


def cap009_official_fetch(audit: Audit) -> None:
    cap = "CAP009"
    base = Path("REPRODUCTION/posterior_attribution/official_fetch_records")
    raw_rel = base / "phase2c_network_execution/evidence/OFFICIAL_ARCHIVE_ACQUISITION.tsv"
    raw = load_tsv(audit, cap, raw_rel.as_posix(), ["SOURCE", "OFFICIAL_URL", "FINAL_URL", "EXPECTED_BYTES", "OBSERVED_BYTES", "EXPECTED_SHA256", "OBSERVED_SHA256", "ACQUISITION_MODE", "STATUS"])
    raw_map = {r.get("SOURCE", ""): r for r in raw}
    audit.require(cap, set(raw_map) == {"ORIGINAL", "FIXED"}, "OFFICIAL_RAW_SOURCE_SET")
    original = raw_map.get("ORIGINAL", {})
    fixed = raw_map.get("FIXED", {})
    audit.require(cap, original.get("OFFICIAL_URL", "").startswith("https://lambda.gsfc.nasa.gov/") and original.get("FINAL_URL") == original.get("OFFICIAL_URL"), "ORIGINAL_OFFICIAL_URL")
    audit.require(cap, original.get("EXPECTED_BYTES") == original.get("OBSERVED_BYTES") == "6194573499", "ORIGINAL_ARCHIVE_SIZE")
    audit.require(cap, original.get("EXPECTED_SHA256") == "NOT_MATERIALIZED_RANGE_ACCESS" and original.get("OBSERVED_SHA256") == "" and original.get("ACQUISITION_MODE") == "OFFICIAL_HTTP_RANGE_AND_SELECTED_MEMBER_SHA256" and original.get("STATUS") == "NOT_RUN", "ORIGINAL_RANGE_BOUNDARY")
    audit.require(cap, fixed.get("OFFICIAL_URL", "").startswith("https://lambda.gsfc.nasa.gov/") and fixed.get("FINAL_URL") == fixed.get("OFFICIAL_URL"), "FIXED_OFFICIAL_URL")
    audit.require(cap, fixed.get("EXPECTED_BYTES") == fixed.get("OBSERVED_BYTES") == "828322572", "FIXED_ARCHIVE_SIZE")
    audit.require(cap, fixed.get("EXPECTED_SHA256") == fixed.get("OBSERVED_SHA256") == FIXED_ARCHIVE_SHA256 and fixed.get("ACQUISITION_MODE") == "OFFICIAL_FULL_ARCHIVE_SHA256" and fixed.get("STATUS") == "PASS", "FIXED_ARCHIVE_IDENTITY")
    normalized = load_tsv(audit, cap, (base / "OFFICIAL_ARCHIVE_VERIFICATION.tsv").as_posix(), ["SOURCE", "ACQUISITION_MODE", "BYTES_MATCH", "FULL_ARCHIVE_SHA256_STATUS", "SELECTED_MEMBER_COUNT", "SELECTED_MEMBER_STATUS", "OVERALL_STATUS", "LIMITATION"])
    norm = {r.get("SOURCE", ""): r for r in normalized}
    audit.require(cap, set(norm) == {"ORIGINAL", "FIXED"}, "OFFICIAL_NORMALIZED_SOURCE_SET")
    no = norm.get("ORIGINAL", {}); nf = norm.get("FIXED", {})
    audit.require(cap, no.get("ACQUISITION_MODE") == "OFFICIAL_HTTP_RANGE_AND_SELECTED_MEMBER_SHA256" and no.get("BYTES_MATCH") == "PASS" and no.get("FULL_ARCHIVE_SHA256_STATUS") == "NOT_MATERIALIZED_NOT_CLAIMED" and no.get("SELECTED_MEMBER_COUNT") == "40/40" and no.get("SELECTED_MEMBER_STATUS") == "PASS" and no.get("OVERALL_STATUS") == "PASS_WITH_SCOPE_RANGE_SELECTED_MEMBER_IDENTITY", "ORIGINAL_NORMALIZED_BOUNDARY")
    audit.require(cap, "not materialized" in no.get("LIMITATION", "").lower(), "ORIGINAL_LIMITATION_TEXT")
    audit.require(cap, nf.get("ACQUISITION_MODE") == "OFFICIAL_FULL_ARCHIVE_SHA256" and nf.get("BYTES_MATCH") == "PASS" and nf.get("FULL_ARCHIVE_SHA256_STATUS") == "PASS" and nf.get("SELECTED_MEMBER_COUNT") == "11/11" and nf.get("SELECTED_MEMBER_STATUS") == "PASS" and nf.get("OVERALL_STATUS") == "PASS", "FIXED_NORMALIZED_BOUNDARY")
    selected_rel = base / "phase2c_network_execution/evidence/OFFICIAL_SELECTED_MEMBER_VERIFICATION.tsv"
    selected = load_tsv(audit, cap, selected_rel.as_posix(), ["SOURCE", "STATUS", "EXPECTED_BYTES", "OBSERVED_BYTES", "EXPECTED_SHA256", "OBSERVED_SHA256"])
    counts = Counter(r.get("SOURCE") for r in selected if r.get("STATUS") == "PASS" and r.get("EXPECTED_BYTES") == r.get("OBSERVED_BYTES") and r.get("EXPECTED_SHA256") == r.get("OBSERVED_SHA256"))
    audit.require(cap, counts == Counter({"ORIGINAL": 40, "FIXED": 11}), f"OFFICIAL_SELECTED_IDENTITY:{dict(counts)}")
    result = parse_key_values(audit, cap, (base / "OFFICIAL_FETCH_RESULT.txt").as_posix())
    expected_result = {
        "OFFICIAL_FETCH_EMPTY_CACHE": "PASS_WITH_SCOPE", "ORIGINAL_ARCHIVE_RANGE_ACCESS": "PASS",
        "ORIGINAL_ARCHIVE_SIZE_MATCH": "PASS", "ORIGINAL_FULL_ARCHIVE_MATERIALIZATION": "NOT_PERFORMED",
        "ORIGINAL_FULL_ARCHIVE_SHA256": "NOT_AVAILABLE_NOT_CLAIMED", "ORIGINAL_ETAG_ROLE": "HTTP_METADATA_ONLY_NOT_SCIENTIFIC_IDENTITY_GATE",
        "ORIGINAL_SELECTED_MEMBER_VERIFY": "40/40_PASS", "FIXED_FULL_ARCHIVE_SHA256": "PASS",
        "FIXED_SELECTED_MEMBER_VERIFY": "11/11_PASS", "TOTAL_SELECTED_MEMBER_VERIFY": "51/51_PASS",
        "E002_FROM_OFFICIAL_EMPTY_CACHE": "PASS",
    }
    for key, value in expected_result.items():
        audit.require(cap, result.get(key) == value, f"OFFICIAL_RESULT:{key}")
    gates = load_tsv(audit, cap, "PROVENANCE/PRETAG_REPRODUCIBILITY_GATE.tsv", ["GATE_ID", "STATUS", "EVIDENCE_PATH"])
    gate = {r.get("GATE_ID", ""): r for r in gates}.get("OFFICIAL_FETCH_EMPTY_CACHE", {})
    audit.require(cap, gate.get("STATUS") == "PASS_WITH_SCOPE_RANGE_SELECTED_MEMBER_IDENTITY", "OFFICIAL_GATE_STATUS")
    active_text = "\n".join((ROOT / rel).read_text(encoding="utf-8", errors="ignore") for rel in ("README.md", "README_JA.md", "REPRODUCIBILITY.md", "RELEASE_CHECKLIST.md", "RELEASE_NOTES_v1.7.1.md", "PROVENANCE/REEXECUTION_EVIDENCE_REGISTER.tsv") if (ROOT / rel).is_file())
    for phrase in FORBIDDEN_ORIGINAL_FULL_HASH_CLAIMS:
        audit.require(cap, phrase.lower() not in active_text.lower(), f"FORBIDDEN_ORIGINAL_FULL_HASH_CLAIM:{phrase}")


def cap010_history_register(audit: Audit) -> None:
    cap = "CAP010"
    base = Path("REPRODUCTION/posterior_attribution")
    allowed = {"BYTE_IDENTICAL_TO_HISTORICAL_SOURCE", "NON_SCIENTIFIC_PORTABILITY_EDIT", "NON_SCIENTIFIC_INPUT_MATERIALIZATION_EDIT", "NON_SCIENTIFIC_PATH_EDIT"}
    local_aggregate: set[tuple[str, str, str, str, str, str]] = set()
    total_local_rows = 0
    for stage_number in range(59, 68):
        stage = f"HTS{stage_number}"
        stage_dir = base / f"stages/hts{stage_number}"
        hist_rel = (stage_dir / "HISTORICAL_SHA256SUMS.txt").as_posix()
        current_rel = (stage_dir / "CURRENT_SHA256SUMS.txt").as_posix()
        register_rel = (stage_dir / "HISTORY_SOURCE_REGISTER.tsv").as_posix()
        for rel in (hist_rel, current_rel, register_rel):
            audit.require(cap, (ROOT / rel).is_file(), f"{stage}_MISSING:{Path(rel).name}")
        local = load_tsv(audit, cap, register_rel, ["HISTORICAL_FILE", "HISTORICAL_SHA256", "CURRENT_FILE", "CURRENT_SHA256", "CHANGE_CLASSIFICATION", "SCIENTIFIC_CODE_CHANGE"])
        total_local_rows += len(local)
        audit.require(cap, len({r.get("CURRENT_FILE") for r in local}) == len(local), f"{stage}_DUPLICATE_CURRENT_FILE")
        historical_checks = parse_checksum_file(audit, cap, hist_rel)
        historical_by_name = {r.get("HISTORICAL_FILE", ""): r.get("HISTORICAL_SHA256", "") for r in local}
        audit.require(cap, set(historical_checks) == set(historical_by_name), f"{stage}_HISTORICAL_CHECKSUM_SET")
        for name, digest in historical_checks.items():
            audit.require(cap, digest == historical_by_name.get(name), f"{stage}_HISTORICAL_CHECKSUM:{name}")
        for row in local:
            current_file = row.get("CURRENT_FILE", "")
            rel = stage_dir / current_file
            path = ROOT / rel
            audit.require(cap, safe_relative(rel.as_posix()) and path.is_file(), f"{stage}_CURRENT_MISSING:{current_file}")
            if path.is_file():
                audit.require(cap, sha256(path) == row.get("CURRENT_SHA256"), f"{stage}_CURRENT_HASH:{current_file}")
            audit.require(cap, HEX64.fullmatch(row.get("HISTORICAL_SHA256", "")) is not None and HEX64.fullmatch(row.get("CURRENT_SHA256", "")) is not None, f"{stage}_REGISTER_HASH_FORMAT:{current_file}")
            audit.require(cap, row.get("CHANGE_CLASSIFICATION") in allowed and row.get("SCIENTIFIC_CODE_CHANGE") == "NO", f"{stage}_CHANGE_BOUNDARY:{current_file}")
            local_aggregate.add((stage, f"stages/hts{stage_number}/{current_file}", row.get("HISTORICAL_SHA256", ""), row.get("CURRENT_SHA256", ""), row.get("CHANGE_CLASSIFICATION", ""), row.get("SCIENTIFIC_CODE_CHANGE", "")))
        current_checks = parse_checksum_file(audit, cap, current_rel)
        expected_names = {r.get("CURRENT_FILE", "") for r in local} | {"HISTORICAL_SHA256SUMS.txt", "HISTORY_SOURCE_REGISTER.tsv"}
        audit.require(cap, set(current_checks) == expected_names, f"{stage}_CURRENT_CHECKSUM_SET")
        for name, digest in current_checks.items():
            path = ROOT / stage_dir / name
            audit.require(cap, path.is_file() and sha256(path) == digest, f"{stage}_CURRENT_CHECKSUM:{name}")
    global_rel = (base / "HISTORY_SOURCE_REGISTER.tsv").as_posix()
    global_rows = load_tsv(audit, cap, global_rel, ["STAGE", "PATH", "HISTORICAL_SHA256", "CURRENT_SHA256", "BYTE_IDENTICAL", "CHANGE_CLASS", "SCIENTIFIC_LOGIC_CHANGED", "SOURCE_REGISTER"])
    global_set = {(r.get("STAGE", ""), r.get("PATH", ""), r.get("HISTORICAL_SHA256", ""), r.get("CURRENT_SHA256", ""), r.get("CHANGE_CLASS", ""), r.get("SCIENTIFIC_LOGIC_CHANGED", "")) for r in global_rows}
    audit.require(cap, len(global_rows) == len(global_set) == total_local_rows and global_set == local_aggregate, f"GLOBAL_HISTORY_ROW_SET:global={len(global_rows)}:local={total_local_rows}")
    for row in global_rows:
        rel = base / row.get("PATH", "")
        path = ROOT / rel
        audit.require(cap, safe_relative(rel.as_posix()) and path.is_file(), f"GLOBAL_HISTORY_MISSING:{row.get('PATH')}")
        if path.is_file():
            audit.require(cap, sha256(path) == row.get("CURRENT_SHA256"), f"GLOBAL_HISTORY_HASH:{row.get('PATH')}")
        expected_byte_flag = "YES" if row.get("HISTORICAL_SHA256") == row.get("CURRENT_SHA256") else "NO"
        audit.require(cap, row.get("BYTE_IDENTICAL") == expected_byte_flag, f"GLOBAL_HISTORY_BYTE_FLAG:{row.get('PATH')}")
        audit.require(cap, row.get("CHANGE_CLASS") in allowed and row.get("SCIENTIFIC_LOGIC_CHANGED") == "NO", f"GLOBAL_HISTORY_BOUNDARY:{row.get('PATH')}")
        audit.require(cap, row.get("SOURCE_REGISTER") == f"stages/{row.get('STAGE','').lower()}/HISTORY_SOURCE_REGISTER.tsv", f"GLOBAL_HISTORY_SOURCE_REGISTER:{row.get('PATH')}")
    audit.metrics["GLOBAL_HISTORY_ROWS"] = len(global_rows)


def is_active_search_file(rel: Path) -> bool:
    posix = rel.as_posix()
    if rel == BASELINE_REL or posix in {"MANIFEST.tsv", "SHA256SUMS.txt", "tools/verify_publication_package.py"}:
        return False
    if any(posix.startswith(prefix) for prefix in HISTORICAL_PREFIXES):
        return False
    if rel.suffix.lower() in {".zip", ".docx", ".pdf", ".png", ".jpg", ".jpeg", ".h5", ".pyc"}:
        return False
    return True


def cap011_active_state(audit: Audit) -> None:
    cap = "CAP011"
    hits: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if not is_active_search_file(rel):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        for token in STALE_TOKENS:
            if token in text:
                hits.append(f"{rel.as_posix()}:{token}")
    for hit in hits:
        audit.fail(cap, f"ACTIVE_STALE_REFERENCE:{hit}")
    audit.metrics["ACTIVE_STALE_REFERENCE_HITS"] = len(hits)


def cap012_historical_baseline(audit: Audit) -> None:
    cap = "CAP012"
    path = ROOT / BASELINE_REL
    audit.require(cap, path.is_file(), "PHASE1_BASELINE_MISSING")
    if path.is_file():
        audit.require(cap, path.stat().st_size == BASELINE_BYTES, f"PHASE1_BASELINE_SIZE:{path.stat().st_size}")
        audit.require(cap, sha256(path) == BASELINE_SHA256, f"PHASE1_BASELINE_SHA256:{sha256(path)}")


def cap013_final_package(audit: Audit, enabled: bool) -> None:
    cap = "CAP013"
    if not enabled:
        audit.metrics["CAP013_MODE"] = "DEFERRED_FINAL_ASSEMBLY"
        return
    files = actual_repository_files()
    checksum_rel = "SHA256SUMS.txt"
    manifest_rel = "MANIFEST.tsv"
    sums = parse_checksum_file(audit, cap, checksum_rel)
    expected_sum_set = files - {checksum_rel}
    audit.require(cap, set(sums) == expected_sum_set, f"FINAL_CHECKSUM_MEMBER_SET:expected={len(expected_sum_set)}:observed={len(sums)}")
    for rel, digest in sums.items():
        if not safe_relative(rel):
            audit.fail(cap, f"FINAL_CHECKSUM_UNSAFE_PATH:{rel}")
            continue
        path = ROOT / rel
        audit.require(cap, path.is_file() and sha256(path) == digest, f"FINAL_CHECKSUM_IDENTITY:{rel}")
    manifest = load_tsv(audit, cap, manifest_rel, ["PATH", "BYTES", "SHA256", "CATEGORY"])
    manifest_paths = [r.get("PATH", "") for r in manifest]
    expected_manifest_set = files - {manifest_rel, checksum_rel}
    audit.require(cap, len(manifest_paths) == len(set(manifest_paths)), "FINAL_MANIFEST_DUPLICATE")
    audit.require(cap, set(manifest_paths) == expected_manifest_set, f"FINAL_MANIFEST_MEMBER_SET:expected={len(expected_manifest_set)}:observed={len(manifest_paths)}")
    for row in manifest:
        rel = row.get("PATH", "")
        if not safe_relative(rel):
            audit.fail(cap, f"FINAL_MANIFEST_UNSAFE_PATH:{rel}")
            continue
        path = ROOT / rel
        audit.require(cap, path.is_file(), f"FINAL_MANIFEST_MISSING:{rel}")
        if path.is_file():
            audit.require(cap, str(path.stat().st_size) == row.get("BYTES") and sha256(path) == row.get("SHA256"), f"FINAL_MANIFEST_IDENTITY:{rel}")
    audit.metrics["FINAL_CHECKSUM_RECORD_COUNT"] = len(sums)
    audit.metrics["FINAL_MANIFEST_RECORD_COUNT"] = len(manifest)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--final-package", action="store_true", help="require complete root MANIFEST/SHA256SUMS closure")
    args = parser.parse_args()
    audit = Audit()
    cap001_release_inventory(audit, args.final_package)
    cap002_original_claims(audit)
    cap003_original_numbers(audit)
    cap004_v001(audit)
    cap005_e001(audit)
    cap006_e002(audit)
    cap007_hts67_history(audit)
    cap008_phase2c_evidence(audit)
    cap009_official_fetch(audit)
    cap010_history_register(audit)
    cap011_active_state(audit)
    cap012_historical_baseline(audit)
    cap013_final_package(audit, args.final_package)

    mode = "FINAL_PACKAGE" if args.final_package else "PHASE2E_CORRECTED_CHECKPOINT"
    print(f"VERIFIER_MODE = {mode}")
    for cap, name in CAP_NAMES.items():
        if cap == "CAP013" and not args.final_package:
            print(f"{cap}_{name.upper().replace(' ', '_').replace('-', '_')} = DEFERRED_FINAL_ASSEMBLY")
        else:
            print(f"{cap}_{name.upper().replace(' ', '_').replace('-', '_')} = {audit.result(cap)}")
    for key in sorted(audit.metrics):
        print(f"{key} = {audit.metrics[key]}")
    required_caps = 13 if args.final_package else 12
    passed_caps = sum(audit.result(f"CAP{i:03d}") == "PASS" for i in range(1, required_caps + 1))
    print(f"REQUIRED_CAPABILITIES = {required_caps}")
    print(f"CAPABILITIES_PASS = {passed_caps}")
    print(f"CAPABILITIES_FAIL = {required_caps - passed_caps}")
    integrity = audit.all_ok(args.final_package)
    print(f"PUBLIC_PACKAGE_VERIFIER_RUNTIME = {'PASS' if integrity else 'FAIL'}")
    print(f"PUBLICATION_PACKAGE_INTEGRITY = {'PASS' if args.final_package and integrity else ('DEFERRED_FINAL_ASSEMBLY' if integrity else 'FAIL')}")
    if args.final_package and integrity:
        print("LOCAL_PUBLICATION_PACKAGE_READY = PASS")
        print("REMOTE_PUBLICATION_ACTIONS = NOT_PERFORMED")
    else:
        print("PRETAG_PUBLICATION_READY = HOLD_DOCUMENT_SYNC_AND_FINAL_ASSEMBLY")
    if not integrity:
        for cap in CAP_NAMES:
            if cap == "CAP013" and not args.final_package:
                continue
            for message in audit.errors[cap]:
                print(f"{cap}_{CAP_NAMES[cap].upper().replace(' ', '_').replace('-', '_')}: {message}", file=sys.stderr)
    return 0 if integrity else 1


if __name__ == "__main__":
    raise SystemExit(main())
