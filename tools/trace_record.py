#!/usr/bin/env python3
"""Print a publication statement (Cxxx), numerical result (Nxxx), or source (Sxxx)."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REGISTERS = {
    "C": (ROOT / "PROVENANCE/STATEMENT_TO_EVIDENCE_REGISTER.tsv", "STATEMENT_ID"),
    "N": (ROOT / "PROVENANCE/PRINCIPAL_NUMERICAL_RESULTS_VALIDATION.tsv", "NUMBER_ID"),
    "S": (ROOT / "PROVENANCE/SOURCE_AND_VERSION_RECORDS.tsv", "SOURCE_ID"),
}


def load_record(path: Path, key_field: str, identifier: str) -> dict[str, str] | None:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if not reader.fieldnames or key_field not in reader.fieldnames:
            raise RuntimeError(f"{path} does not contain required field {key_field}")
        for row in reader:
            if row.get(key_field, "").strip().upper() == identifier:
                return row
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("identifier", help="Stable identifier such as C002, N001, or S001")
    args = parser.parse_args()

    identifier = args.identifier.strip().upper()
    if len(identifier) < 2 or identifier[0] not in REGISTERS:
        parser.error("identifier must begin with C, N, or S")

    path, key_field = REGISTERS[identifier[0]]
    try:
        record = load_record(path, key_field, identifier)
    except (OSError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if record is None:
        print(f"No record found for {identifier}", file=sys.stderr)
        return 1

    print(f"[{identifier}] {path.relative_to(ROOT)}")
    for field, value in record.items():
        if value and value.strip():
            print(f"\n{field}\n{'-' * len(field)}\n{value.strip()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
