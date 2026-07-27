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

After the public repository exists and the manuscript points to it consistently, cite a fixed Git tag or release rather than the moving `main` branch. Do not record a release URL before it actually exists. Version 1.6.0 is the current release candidate. Version 1.5.5 remains the preserved historical public version preceding integration of the V001 post-synthesis validation evidence.


## 7. Post-synthesis V001 validation

Version 1.6.0 adds a later project-internal second-implementation check of released TDCOSMO HDF5 sample summaries. The evidence is stored under `POST_SYNTHESIS_VALIDATION/tdcosmo_second_implementation/` and indexed by `PROVENANCE/POST_SYNTHESIS_VALIDATION_REGISTER.tsv`.

This validation was performed after the original 30-statement and 46-number audit. It does not alter `C001–C030` or `N001–N046`.

The implementation, source manifest, Type-7 quantile definition, comparison tolerance, and stopping rule were fixed before the unchanged-code 13-file extension. The retained result is 13/13 structural comparisons, 39/39 q16/q50/q84 comparisons within the frozen tolerance, and 12/12 Table 6 rows at published precision.

The evidence does not include or reproduce the third-party HDF5 bytes, original likelihood, sampler, burn-in, thinning, convergence diagnostics, posterior weights, log probabilities, or posterior-generation pipeline. It is a project-internal implementation-diversity check, not external independent replication.
