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

Its purpose is narrower: to make the manuscript's publication statements, numerical values, source versions, author-generated outputs, and stated limitations inspectable and cross-referenced.

## Repository status

```text
PUBLICATION_PACKAGE_VERSION = 1.5.5
PUBLICATION_CORE_MEMBER_SET = 102 files
REPOSITORY_RELEASE_FILES    = 121 files
HASHED_RELEASE_FILES        = 120 / 120 VERIFIED
MANUSCRIPT_STATUS           = PREPARED_FOR_JXIV_SUBMISSION
PERSISTENT_IDENTIFIER       = NOT_ASSIGNED
REPOSITORY_PUBLIC_URL       = [https://github.com/yokken0907/hubble-constant-inference-traceability]
```

No Jxiv DOI, Jxiv URL, public repository URL, release URL, or publication status is asserted in this pre-publication package. Follow [`PUBLICATION_UPDATE_GUIDE.md`](PUBLICATION_UPDATE_GUIDE.md) only after the relevant identifiers actually exist.

## Source archive identity

```text
FROZEN_CORE_SOURCE_ARCHIVE_FILENAME = Yoshimura_2026_Dependency_and_Numerical_Traceability_in_Public_Hubble_Constant_Inference_Data.zip
FROZEN_CORE_SOURCE_ARCHIVE_SHA256   = e7074403b3fc4ddce1b11c05696cc3735b1f39c52fc5cb0e71ce517ebb949bce
FROZEN_CORE_SOURCE_ARCHIVE_INCLUDED = NO
```

This hash identifies the internal source archive used to assemble the original public core; it is not the hash of the current repository ZIP. See [`SOURCE_ARCHIVE_RECORD.md`](SOURCE_ARCHIVE_RECORD.md).

## Version 1.5.5 revision scope

Version 1.5.5 adds stable `NUMBER_ID` values (`N001`–`N046`) directly to `TABLES/TABLE2_NUMERICAL_RESULTS.tsv`. No scientific value, unit, scope, interpretation, or claim status was changed. See [`CHANGELOG.md`](CHANGELOG.md) and [`PROVENANCE/TABLE2_NUMBER_ID_VALIDATION.tsv`](PROVENANCE/TABLE2_NUMBER_ID_VALIDATION.tsv).

## Start here

| Question | File |
|---|---|
| Which manuscript statement is supported by which evidence? | [`PROVENANCE/STATEMENT_TO_EVIDENCE_REGISTER.tsv`](PROVENANCE/STATEMENT_TO_EVIDENCE_REGISTER.tsv) |
| Where do the 46 principal numerical results come from? | [`PROVENANCE/PRINCIPAL_NUMERICAL_RESULTS_VALIDATION.tsv`](PROVENANCE/PRINCIPAL_NUMERICAL_RESULTS_VALIDATION.tsv) |
| How do Table 2 rows map directly to `N001`–`N046`? | [`PROVENANCE/TABLE2_NUMBER_ID_VALIDATION.tsv`](PROVENANCE/TABLE2_NUMBER_ID_VALIDATION.tsv) |
| Which public source and version was used? | [`PROVENANCE/SOURCE_AND_VERSION_RECORDS.tsv`](PROVENANCE/SOURCE_AND_VERSION_RECORDS.tsv) |
| Which archived output corresponds to each included public file? | [`PROVENANCE/ARCHIVED_OUTPUT_INDEX.tsv`](PROVENANCE/ARCHIVED_OUTPUT_INDEX.tsv) |
| What are the release file sizes and hashes? | [`MANIFEST.tsv`](MANIFEST.tsv) and [`SHA256SUMS.txt`](SHA256SUMS.txt) |
| What can and cannot be reproduced from this repository? | [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) |

## Quick verification

Python 3.9 or later is sufficient; no third-party Python package is required.

```bash
python tools/verify_publication_package.py
```

Trace a publication statement, numerical result, or source by stable identifier:

```bash
python tools/trace_record.py C002
python tools/trace_record.py N001
python tools/trace_record.py S001
```

## Structure

```text
TABLES/               publication-facing machine-readable tables
FIGURE_SOURCE_DATA/   source data for the four principal figures
PROVENANCE/           statement, number, source, path, hash, and ID-mapping registers
ANALYSIS_OUTPUTS/     selected author-generated summaries and audit records
tools/                small repository navigation and integrity utilities
MANIFEST.tsv          release path, byte-size, category, and SHA-256 inventory
SHA256SUMS.txt         checksums for every release file except the checksum file itself
```

The original publication-core member set was selectively retained. Version 1.5.5 changes only the Table 2 identifier column and repository/publication metadata described in the changelog; it does not reinterpret the scientific evidence.

## Reproducibility boundary

The repository supports:

1. statement-to-evidence traceability;
2. direct `Nxxx` mapping from the public numerical table to the numerical register;
3. checking manuscript rounding and stored numerical values;
4. checking the identity and integrity of included author-generated outputs;
5. identifying the public source and version used for each analysis; and
6. distinguishing re-executed results, archived-output checks, and limited second-implementation checks.

It does not redistribute large third-party posterior archives, likelihood products, or raw observational releases. Full reconstruction from raw observations through the original collaboration pipelines is outside the repository's scope. See [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md).

## Third-party material

Only author-generated tables, summaries, registers, audit records, figure-source data, and limited author-written code or patches are included. Third-party raw files are omitted. Obtain cited data and software from their original providers under their respective terms.

## AI assistance

This project was conducted by a non-specialist independent researcher with extensive general-purpose AI assistance. The role and limits of that assistance are described in [`AI_DISCLOSURE.md`](AI_DISCLOSURE.md).

## Citation

Use [`CITATION.cff`](CITATION.cff). The public repository URL and Jxiv record must be added only after they actually exist. The manuscript should remain the primary scientific source and this repository its associated traceability archive.

## License

Unless otherwise noted, documentation, tables, data files, figure-source data, provenance registers, and audit records are licensed under CC BY 4.0. Python source files under `tools/` are licensed under the MIT License; see [`tools/LICENSE`](tools/LICENSE). Third-party identifiers and citations do not change the terms imposed by their original providers. See [`LICENSE`](LICENSE).
