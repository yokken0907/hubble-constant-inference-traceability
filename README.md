# Dependency and Numerical Traceability in Public Hubble-Constant Inference

[日本語版 README](README_JA.md)

This repository is the manuscript-associated public traceability archive for:

> **Dependency and Numerical Traceability in Public Hubble-Constant Inference: An Integrated Audit of the Local Distance Ladder, Supernova Processing, BAO, CMB, Posterior Geometry, and Other Distance Methods**  
> Keiji Yoshimura, Independent Researcher (2026)

## Claim boundary

This repository does **not** claim:

- resolution of the Hubble tension;
- identification of a unique cause or uniquely justified correction;
- a new independent measurement of the Hubble constant;
- validation of the original collaborations' complete pipelines; or
- evidence for new physics.

Its purpose is narrower: to make the manuscript's publication statements, numerical values, source versions, author-generated outputs, later bounded validation records, and stated limitations inspectable and cross-referenced.

## Repository status

```text
PUBLICATION_PACKAGE_VERSION = 1.6.0
BASE_PUBLIC_VERSION          = 1.5.5
PUBLICATION_CORE_MEMBER_SET  = 102 files
REPOSITORY_RELEASE_FILES     = 155 files
HASHED_RELEASE_FILES         = 154 / 154 VERIFIED
ORIGINAL_STATEMENT_COUNT     = 30
ORIGINAL_NUMBER_COUNT        = 46
POST_SYNTHESIS_VALIDATIONS   = 1
PACKAGE_BUILD_STATUS         = FINAL_CANDIDATE_FOR_V1.6.0
TAG_V1_6_0_STATUS_AT_PACKAGE_BUILD = NOT_ASSIGNED
PERSISTENT_IDENTIFIER        = NOT_ASSIGNED
REPOSITORY_PUBLIC_URL        = https://github.com/yokken0907/hubble-constant-inference-traceability
```

Version 1.5.5 remains the immutable historical public release preceding formal integration of the later TDCOSMO second-implementation evidence. Version 1.6.0 is a new release candidate and does not repoint or rewrite the `v1.5.5` tag or release.

At package-build time, no `v1.6.0` tag URL, Jxiv DOI, Jxiv URL, release URL, or persistent identifier had been assigned. Only identifiers that actually exist should be recorded later.

## Version 1.6.0 scope

Version 1.6.0 adds a public evidence chain for a later bounded, project-internal second-implementation check of released TDCOSMO HDF5 sample summaries:

- 13/13 structural comparisons passed;
- 39/39 q16/q50/q84 comparisons passed within the frozen project tolerance;
- 12/12 Table 6 rows matched at published precision.

The implementation, quantile method, source manifest, tolerance, and stopping rule were fixed before the unchanged-code 13-file extension.

This addition does not change:

- any original statement `C001`–`C030`;
- any principal numerical result `N001`–`N046`;
- any stored numerical value, unit, scope, or claim status in Table 2;
- the historical `NOT_DONE` and HOLD records for the earlier C026/C027 stage.

The later result is recorded separately as `V001 = COMPLETE_WITH_SCOPE`. `NOT_DONE` and `COMPLETE_WITH_SCOPE` refer to different historical stages and are not contradictory.

## Source archive identity

```text
FROZEN_CORE_SOURCE_ARCHIVE_FILENAME = Yoshimura_2026_Dependency_and_Numerical_Traceability_in_Public_Hubble_Constant_Inference_Data.zip
FROZEN_CORE_SOURCE_ARCHIVE_SHA256   = e7074403b3fc4ddce1b11c05696cc3735b1f39c52fc5cb0e71ce517ebb949bce
FROZEN_CORE_SOURCE_ARCHIVE_INCLUDED = NO
```

This hash identifies the internal source archive used to assemble the original public core; it is not the hash of the current repository ZIP. See [`SOURCE_ARCHIVE_RECORD.md`](SOURCE_ARCHIVE_RECORD.md).

## Start here

| Question | File |
|---|---|
| Which manuscript statement is supported by which evidence? | [`PROVENANCE/STATEMENT_TO_EVIDENCE_REGISTER.tsv`](PROVENANCE/STATEMENT_TO_EVIDENCE_REGISTER.tsv) |
| Where do the 46 principal numerical results come from? | [`PROVENANCE/PRINCIPAL_NUMERICAL_RESULTS_VALIDATION.tsv`](PROVENANCE/PRINCIPAL_NUMERICAL_RESULTS_VALIDATION.tsv) |
| How do Table 2 rows map directly to `N001`–`N046`? | [`PROVENANCE/TABLE2_NUMBER_ID_VALIDATION.tsv`](PROVENANCE/TABLE2_NUMBER_ID_VALIDATION.tsv) |
| Which public source and version was used? | [`PROVENANCE/SOURCE_AND_VERSION_RECORDS.tsv`](PROVENANCE/SOURCE_AND_VERSION_RECORDS.tsv) |
| Which later bounded validation was added after synthesis? | [`PROVENANCE/POST_SYNTHESIS_VALIDATION_REGISTER.tsv`](PROVENANCE/POST_SYNTHESIS_VALIDATION_REGISTER.tsv) |
| How are the earlier `NOT_DONE` and later `COMPLETE_WITH_SCOPE` states reconciled? | [`POST_SYNTHESIS_VALIDATION/tdcosmo_second_implementation/HISTORICAL_SEQUENCE.md`](POST_SYNTHESIS_VALIDATION/tdcosmo_second_implementation/HISTORICAL_SEQUENCE.md) |
| Was v1.5.5 scientific content preserved? | [`PROVENANCE/V1_5_5_PRESERVATION_RECORD.tsv`](PROVENANCE/V1_5_5_PRESERVATION_RECORD.tsv) |
| What are the release file sizes and hashes? | [`MANIFEST.tsv`](MANIFEST.tsv) and [`SHA256SUMS.txt`](SHA256SUMS.txt) |
| What can and cannot be reproduced? | [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) |

## Quick verification

Python 3.9 or later is sufficient; no third-party Python package is required for the repository integrity verifier.

```bash
python tools/verify_publication_package.py
```

Trace a publication statement, numerical result, public source, or post-synthesis validation:

```bash
python tools/trace_record.py C026
python tools/trace_record.py N001
python tools/trace_record.py S001
python tools/trace_record.py V001
```

## Structure

```text
TABLES/                    publication-facing machine-readable tables
FIGURE_SOURCE_DATA/        source data for the four principal figures
PROVENANCE/                statement, number, source, validation, path, and hash registers
ANALYSIS_OUTPUTS/          selected author-generated historical summaries and audit records
POST_SYNTHESIS_VALIDATION/ later bounded validation evidence integrated after the original audit
tools/                     repository navigation and integrity utilities
.github/FUNDING.yml        GitHub Sponsors configuration
MANIFEST.tsv               release path, byte-size, category, and SHA-256 inventory
SHA256SUMS.txt              checksums for every release file except the checksum file itself
```

## TDCOSMO post-synthesis validation boundary

The V001 evidence is a project-internal implementation-diversity check of released-sample summaries. It does not redistribute third-party HDF5 files and does not reconstruct the original likelihood, sampler, burn-in, thinning, convergence diagnostics, posterior weights, log probabilities, or posterior-generation pipeline.

It is not external independent replication. See [`POST_SYNTHESIS_VALIDATION/tdcosmo_second_implementation/README.md`](POST_SYNTHESIS_VALIDATION/tdcosmo_second_implementation/README.md).

## Reproducibility boundary

The repository supports:

1. statement-to-evidence traceability;
2. direct `Nxxx` mapping from the public numerical table to the numerical register;
3. checking manuscript rounding and stored numerical values;
4. checking the identity and integrity of included author-generated outputs;
5. identifying the public source and version used for each analysis;
6. distinguishing re-executed results, archived-output checks, within-source robustness, and project-internal implementation diversity; and
7. tracing the later V001 result without rewriting the historical C026/C027 state.

It does not redistribute large third-party posterior archives, likelihood products, or raw observational releases. Full reconstruction from raw observations through the original collaboration pipelines is outside the repository's scope.

## Third-party material

Only author-generated tables, summaries, registers, audit records, figure-source data, and limited author-written code or patches are included. Third-party HDF5 files, raw data, and paper PDFs are omitted. Obtain cited data and software from their original providers under their respective terms.

## AI assistance

This project was conducted by a non-specialist independent researcher with extensive general-purpose AI assistance. The role and limits of that assistance are described in [`AI_DISCLOSURE.md`](AI_DISCLOSURE.md).

## Citation

Use [`CITATION.cff`](CITATION.cff). The public repository URL is recorded there. If a `v1.6.0` release URL or Jxiv metadata is later issued, record only the actual public identifiers. The manuscript should remain the primary scientific source and this repository its associated traceability archive.

## License

Unless otherwise noted, documentation, tables, data files, figure-source data, provenance registers, and audit records are licensed under CC BY 4.0. Python source files under `tools/` and the designated V001 implementation file are licensed under the MIT License. Third-party identifiers and citations do not change the terms imposed by their original providers. See [`LICENSE`](LICENSE).
