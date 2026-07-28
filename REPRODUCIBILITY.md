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

After the public repository exists and the manuscript points to it consistently, cite a fixed Git tag or release rather than the moving `main` branch. Do not record a release URL before it actually exists. The local version 1.7.0 package is assembled and verified, while creation or independent verification of the public tag and Release remains an external action. Version 1.5.5 remains the preserved historical public version preceding integration of the V001 post-synthesis validation evidence.


## 7. Post-synthesis V001 validation

Version 1.6.1 adds a later project-internal second-implementation check of released TDCOSMO HDF5 sample summaries. The evidence is stored under `POST_SYNTHESIS_VALIDATION/tdcosmo_second_implementation/` and indexed by `PROVENANCE/POST_SYNTHESIS_VALIDATION_REGISTER.tsv`.

This validation was performed after the original 30-statement and 46-number audit. It does not alter `C001–C030` or `N001–N046`.

The implementation, source manifest, Type-7 quantile definition, comparison tolerance, and stopping rule were fixed before the unchanged-code 13-file extension. The retained result is 13/13 structural comparisons, 39/39 q16/q50/q84 comparisons within the frozen tolerance, and 12/12 Table 6 rows at published precision.

The evidence does not include or reproduce the third-party HDF5 bytes, original likelihood, sampler, burn-in, thinning, convergence diagnostics, posterior weights, log probabilities, or posterior-generation pipeline. It is a project-internal implementation-diversity check, not external independent replication.

## Publication model for the v1.7.0 package

No supplementary ZIP archive is submitted with the manuscript. Public evidence locations are repository-relative paths in `PROVENANCE/STATEMENT_TO_EVIDENCE_REGISTER.tsv`, and analysis-level reproduction status is recorded in `PROVENANCE/REPRODUCTION_STATUS.tsv`. Numerical traceability does not imply re-executability; the DESI BAO fit is separately classified as re-executable with fixed external inputs.

## v1.7.0 replay evidence

- `E001` replays N025-N026 from included frozen Gaussian posterior moments with NumPy `default_rng`, seed 10199, and 1,000 draws.
- `E002` replays N029-N035 through a two-layer HTS59-HTS67 workflow. HTS59-HTS65 are re-executed from 51 hash-fixed posterior-export members. HTS66 uses verified path-sanitized portable replicas of the historical intermediate inputs required by its fixed gates. The canonical current acceptance lineage is the Phase2C official empty-cache run. Its eight designated HTS67 substantive tables are byte-identical to the preserved historical substantive reference, as generated directly from the retained Phase2C result ZIP in `HTS67_HISTORICAL_VS_FRESH_COMPARISON.tsv`. Path- and packaging-dependent records are checked separately and are not claimed to be byte-identical.

Both records are `COMPLETE_WITH_SCOPE`. Neither reconstructs the originating likelihoods, samplers, convergence assessment, or posterior-generation environment, and neither is external independent validation.

## v1.7.0 reproducibility-repair status

E001 has a clean fixed-input replay. E002 now validates fresh HTS59-HTS67 outputs directly rather than accepting a retained historical PASS table. The public wrapper creates an HTS67 compatibility cache view with `ORIGINAL_FACTORIAL_SELECTED/` and `FIXED_FULL_SELECTED/` roots while preserving the historical HTS67 root-discovery logic. Each HTS stage retains `HISTORICAL_SHA256SUMS.txt` and verifies the portable release files through `CURRENT_SHA256SUMS.txt`.

The intended online command is:

```bash
python REPRODUCTION/posterior_attribution/run_all.py --fetch-inputs --cache ./_external_cache --work ./_work/posterior_attribution --output ./_outputs/posterior_attribution --verify
```

For controlled offline audit only, `--import-selected-from` may import an already materialized selected cache; all 51 files are still required to match `SELECTED_CHAIN_MANIFEST.tsv`, and the resulting scientific stages and fresh-output verifier are unchanged. Online official-source acquisition remains a separate gate when the execution environment has network access.

### Fresh replay and official acquisition records

The repaired E002 verifier reads a generated HTS59–HTS67 output directory directly. The global `HISTORY_SOURCE_REGISTER.tsv` is regenerated from the nine stage-local registers, and current and historical checksum identities are checked against the packaged files. Earlier replay audit records remain under `REPRODUCTION/posterior_attribution/fresh_replay_records/` and `historical_earlier_replay/`; they are not the current Phase2C acceptance lineage.

Phase2C subsequently executed the replay in a network-enabled WSL environment from a newly empty external cache. This run is the sole current E002 acceptance lineage. The FIXED archive matched its full-archive SHA-256; the ORIGINAL archive was accessed by HTTP Range and all 40 selected ORIGINAL members, together with 11 selected FIXED members, matched their registered byte sizes and SHA-256 values. E002 completed successfully. The retained Phase2C HTS67 result ZIP has SHA-256 `8254503a8a18d6ca3cfcc6dfb0104458982e19bd13bf89b9c81d3e8f34a31353`; its eight designated substantive scientific tables are byte-for-byte identical to the historical substantive reference. The full 6.19 GB ORIGINAL archive was not materialized and no full-archive SHA-256 is claimed. The recorded and observed ORIGINAL ETags differ; this is retained as HTTP metadata and is not the scientific input-identity gate. Remote publication actions were not performed.

HTS59–HTS65 use a wrapper-level preverified selected-cache materialization view to avoid repeatedly expanding multi-gigabyte upstream archives. `HISTORICAL_SHA256SUMS.txt` preserves each original RUN_PACKAGE checksum set, while `CURRENT_SHA256SUMS.txt` verifies the portable release files. The scientific calculations remain unchanged; portability and fresh-output verification edits are recorded in each `HISTORY_SOURCE_REGISTER.tsv`.
