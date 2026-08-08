# Reproducibility and Traceability Guide

## 1. What this repository is designed to reproduce

This repository is designed primarily for **publication-level numerical traceability**, not for full raw-data-to-posterior reconstruction.

It supports four distinct verification layers.

### Layer A — File integrity

`SHA256SUMS.txt` records every release file except the checksum file itself. `MANIFEST.tsv` records every ordinary release member except the manifest and checksum files, whose integrity is covered by `SHA256SUMS.txt`. Run:

```bash
python tools/verify_publication_package.py
```

A successful run verifies hashes, manifest coverage, Table 2 ID coverage, and the existing frozen numerical-validation statuses.

### Layer B — Statement-to-evidence traceability

`PROVENANCE/STATEMENT_TO_EVIDENCE_REGISTER.tsv` links 30 publication statements to evidence assessments, interpretation limits, designated author-generated outputs, package-relative paths and SHA-256 values, source datasets or chains, versions, and manuscript locations.

```bash
python tools/trace_record.py C002
```

### Layer C — Numerical traceability

`TABLES/TABLE2_NUMERICAL_RESULTS.tsv` now carries `NUMBER_ID` values `N001`–`N046` directly. `PROVENANCE/PRINCIPAL_NUMERICAL_RESULTS_VALIDATION.tsv` links those identifiers to stored precision, manuscript rounding, units, canonical artifacts, field or row locators, hashes, source versions, and two frozen consistency checks. `PROVENANCE/TABLE2_NUMBER_ID_VALIDATION.tsv` records the explicit table-to-register crosswalk.

```bash
python tools/trace_record.py N001
```

### Layer D — Public-source reconstruction boundary

`PROVENANCE/SOURCE_AND_VERSION_RECORDS.tsv` identifies public datasets, papers, code repositories, versions, acquisition methods, processing scope, and redistribution limits.

Some analyses were re-executed from specified public inputs; others were checked against preserved machine-readable outputs. The limited TDCOSMO second-implementation check tested source integrity, HDF5 structure, and equal-weight quantiles. These categories are not treated as equivalent.

## 2. What is not reproduced here

This repository does not contain large third-party posterior archives, full external likelihood products, raw observational releases, private or collaboration-internal pipeline material, unavailable cross-experiment covariance, unavailable simulation-reference products, or the complete internal development archive of intermediate HTV/HTS stages.

Accordingly, it does not reproduce the original collaborations' full likelihood, sampling, convergence, calibration, or posterior-generation pipelines.

## 3. Recommended audit sequence

1. Run the integrity verifier.
2. Read `TABLES/TABLE1_EVIDENCE_DOMAINS.tsv` and `TABLES/TABLE3_CAUSAL_INTERPRETATION_LIMITS.tsv`.
3. Select a claim ID in `STATEMENT_TO_EVIDENCE_REGISTER.tsv`.
4. Inspect the designated `ANALYSIS_OUTPUTS/` files and confirm their hashes.
5. For numerical claims, use the `NUMBER_ID` in Table 2 and follow the corresponding record in `PRINCIPAL_NUMERICAL_RESULTS_VALIDATION.tsv`.
6. Check the direct mapping record in `TABLE2_NUMBER_ID_VALIDATION.tsv`.
7. Check the source identity and version in `SOURCE_AND_VERSION_RECORDS.tsv`.
8. Apply the recorded interpretation limit before drawing a scientific conclusion.

## 4. Stable identifiers

- `C001`–`C030`: publication statement identifiers.
- `N001`–`N046`: principal numerical-result identifiers.
- `HTVxx` and `HTSxx`: archival stage locators.
- `Sxxx`: public-source records.
- `Vxxx`: post-synthesis validation identifiers. `V001` identifies the later bounded TDCOSMO second-implementation record.

These identifiers are locators only. They do not encode evidential strength or scientific priority.

## 5. Source-archive boundary

The source archive named in `SOURCE_ARCHIVE_RECORD.md` is not included. Its SHA-256 identifies the internal assembly source and must not be cited as the hash of the current repository ZIP.

## 6. Version freezing

## Public versioning and source identity

The fixed scientific archive for the associated study is GitHub Release `v1.7.1` (tag `v1.7.1`; commit `8ada39da3c712923b70bae0c060388180e0f3a82`). Repository version `v1.7.3` updates reader-facing disclosure and publication metadata without changing that scientific baseline. Version `v1.7.2` remains an unchanged historical metadata release.

The local package verifier validates the recorded local tree and its registered scientific and provenance relationships. GitHub-generated ZIP and tar archives are separate transport artifacts; complete byte identity with a separately assembled local ZIP is not claimed unless explicitly checked against a published hash.

## Publication model for the v1.7.3 repository edition

The publication metadata is platform-neutral until an actual manuscript or preprint record exists. This repository remains the associated scientific traceability archive. Public evidence locations are repository-relative paths in `PROVENANCE/STATEMENT_TO_EVIDENCE_REGISTER.tsv`, and analysis-level reproduction status is recorded in `PROVENANCE/REPRODUCTION_STATUS.tsv`.

Numerical traceability does not imply re-executability. Re-execution does not imply implementation independence. Project-internal implementation diversity does not imply external independent replication. A report URL, DOI, or other persistent identifier is recorded only after it actually exists and only in a later repository version.

## Integrity commands

```bash
python tools/finalize_publication_package.py --check
python tools/verify_publication_package.py --final-package
sha256sum -c SHA256SUMS.txt
```

Independent domain-expert review remains pending.
